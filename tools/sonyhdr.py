# coding=gb2312

'''
背景介绍：
    正常的相片文件都会有EXIF，里面的三个重要信息是相机牌子、型号和拍照日期。此备份系统主要是
    依靠相片的时间，其次是相片文件大小、MD5来区分照片和排序的。照片有时间信息和能够备份是充要
    条件。对于没有日期的，用户可以补充 metadata文件。详细可以看_getinfo代码。
    视频文件没有EXIF，完全根据文件修改日期或者metadata名称。
    如下说明对相片和是是相同的。
    
第一步：使用 tj 0来统计一下待备份目录的照片的情况。会统计出如下一些信息：
    1）"No Exif"：文件中没有Exif，这些主要是一些非相机来源的照片或者是经过编辑后的照片。
    2）"No MMDT"：有Exif，但是里面没有Datetime，没有Make/Model；这种情况比较罕见。
    3）"No MM": EXIF中没有Make/Model，但是有Datetime。相片经过Photoshop等编辑后就如此了。
    4）"Zero DT": EXIF中的DateTime为全零（olympus某款相机没有设置时间就会变成如此；
    5）"MM No DateTime"：有Make/Model，但是没有DateTime，罕见。
    6）"DateTime"：会统计有时间的照片的年月日分布情况。
    7）"Make Models"：照片的相机牌子型号分布情况。
    8）"No MM Paths"： "No MM"类型照片的路径列表。
    9）"Zero DT Paths"："Zero DT"照片的路径列表。
    A）Funny文件: size,datetime相同，但是MD5不同
    B）重复文件: size,MD5相同，但是DateTime不同
    C）同一个文件：size,md5,DateTime都相同的情况

    情况1、2、4、5必须处理，否则无法这些照片无法被备份。
    实践中会出现有些照片的时间明显不对，猜测是某些相机没有设置时间后，会从出厂时间开始。
    通过看DateTime列表就可以看出这些情况。
    情况B、C可以手工删除多余文件。如果不修正，则情况B的文件会被冗余备份。情况C只会备份一个。
    
    如果照片文件有.adjust、.datetime或者文件名是归档统一类型的，则统计中会使用这些信息。
    可以对归档后的文件夹进行统计，看看是否有重复的情况。详细可以看_getinfo函数。
    
第二步：[sc 0/1] 对照片日期的人工修正、半自动、全自动修正 
    会对 'noexif', 'nodt', 'outdt', 'zeordts', 'errordt'等情况进行修正。
    全自动修正：会根据这些文件的文件名、目录名进行分析，猜测出日期，对相同日期的，按照步进固定
    秒数去设置不同的时分秒。如果要使用这个功能，则将需要修正或者补充日期的文件的目录名称修改为
    YYYY-MM-DD的形式即可。
    半自动修正：如果猜测不出日期，则会根据传入的BASE，按照步进去设置不同的时分秒。
    人工修正：补充日期Meta文件后缀为 .dtadjust。
    自动或半自动修正：补充日期meta文件后缀为.datetime
    因为人工修正结果比较珍贵，因此必须手工删除才可以。而datatime文件会被程序覆盖。
   
    在生成日期时，会校验MD5，保证相同文件如果在多个目录里面有的话，会生成同一个MD5
    sc 0/1只支持全自动修正，不支持起止日期检查。'noexif':True,'zeordts':True,'outdt':True
    0与1的区别在于如何判断照片是  noexif/zerodts。详细可以看 _DateTimeGen 函数。
    
第三步：[jc 0/1] 对照片日期进行检查。
    datetime.datetime(1900,1,1), datetime.datetime(2100,1,1)
    可以统计出'noexif', 'nodt', 'outdt', 'zeordts', 'errordt'的各种情况。
    对日期不对的情况，会打印出猜测的日期。
    对于日期正确的，也会打印出猜测的日期。
    检查和生成是一个程序。

第四步：[sm] 预览照片说明
    在归档后，每个照片都可以有一段说明文字。这些文字也是在备份的时候从文件名、目录名中猜测出来的。
    详细可以看_genname函数。
    如果希望归档后的文件不只是段数字，则可以在归档前修改目录名称。如果既有日期又有名称的，日期要在
    名称的前面。如yyyy-mm-dd 啥

第五步：[bk] 将当前目录备份到archive目录下
    1) 会检查已有文件和新文件，保证不会有重复的导入进来。会使用Size+MD5的方式。
       如果新文件中有重复的，会备份哪个，完全是随机的，但是会选择最长的那个note。
    2) 目录和文件会以时间排序来分组，每个组的文件不超过200个。
    3) 新增文件会自动选择合适的目录。
    4）每个目录的名称都是最小的那个文件的时间。
    
第六步：[jcbk] 检查是否已经全部备份
    使用MD5校验，所以会比较慢。

第七步：[jca] 检查备份目录是否有时间错误


如果备份视频，则会比较简单。因为视频文件没有EXIF，只能根据修改日期。
'''   

import os, time, datetime, bisect, shutil, collections,re,inspect,sys,functools,itertools, random,stat
import hashlib
from collections import defaultdict

import Image, pyexiv2

import gpylib.misc

from gpylib.misc import GREEN,RED,BLUE,YELLOW,BWHITE,DIM
from gpylib.future import gprint

__RUN_CURRENT_FILE__ = __name__=="__main__"

'''**************************************************************'''
'''第一部分：工具函数 *******************************************'''   

def globphotoes(path):
    def isphoto(x):
        photonames = ('^CIMG','^IMG','^IMAG','^DSC[ \da-z]{5,}',
                 '^P[a-z]*[ \d]{5,}','^A[ \d]{5,}','^S[ \d]{5,}','^L[ \d]{5,}',)
                 
        return x.lower().endswith(".jpg") and any( re.match(pn, x, re.I) for pn in photonames)

    for f in gpylib.misc.walkfiles(path, isphoto, debug=False):
        print f

def globphotoescurrentdir():
    globphotoes(os.getcwdu())
    
if __RUN_CURRENT_FILE__:        
    pass
    #globphotoes(ur"D:\\")
    
def CLAIM_PROCESS_PIC():
    global _WALK_CONDITION
    _WALK_CONDITION = lambda x: x.lower().endswith(".jpg")
    
def CLAIM_PROCESS_MOV():
    global _WALK_CONDITION
    _WALK_CONDITION = lambda x: os.path.splitext(x)[1].lower() in (".mov",
                                        ".mts",".mp4",".avi",".mpg",".dat",".vob")
    

class PicException(Exception):pass

def _trygeninfofromname(fn):
    '''如果是规范后的文件名，则返回(DateTime,note,size)'''
    fn = os.path.split(fn)[1]
    m = re.match(ur'^(\d{4}\-\d\d-\d\d_\d{6})(\([^\(\)]+\))?_?([0-9a-z]*)-?([0-9a-z]*)\.[a-z0-9]{3}$',fn,re.U|re.I)
    try:
        return( datetime.datetime.strptime(m.group(1), "%Y-%m-%d_%H%M%S").strftime("%Y:%m:%d %H:%M:%S"),
                m.group(2) if m.group(2) else None,
                int(m.group(3),16) if m.group(3) else None )
    except Exception:
        return (None,None,None)

if __RUN_CURRENT_FILE__: 
    def _testgetinfofromname():
        fns=[u'2004-04-03_192941(SUDAN)_12DD1D-55.jpg',
             u'2004-09-26_000001(Yunnan 泸沽湖 扎西聊吧)_B50F9.jpg',
             u'2004-09-26_000001(Yunnan 泸沽湖 扎西聊吧).jpg',
             u'2004-09-26_000001(Yunnan 泸沽湖 扎西聊吧)_B50F9.mov',
             u'2004-04-03_192941_12DD1D.jpg',
             u'2004-04-03_192941-7.jpg',
            ur'2004-09-27_010027(Yunnan 泸沽湖 去尼塞的路上 美丽的泸沽湖 里格半岛).jpg',]
        for f in fns:
            print u"{}, {}, {}".format(*_trygeninfofromname(f))
             
    #_testgetinfofromname()

def _getarchiveinfodtonly(fn):
    '''快速加载归档文件'''
    (dt,note,size) = _trygeninfofromname(fn)
    if dt is not None:
        tags={}
        tags["DateTime"] = dt
        return tags,note if note else ""
    else:
        return None,None
        
def _getinfo(fn,allowmeta=False,shortmakemodel=True, forceraw=False):
    '''会根据文件内部的EXIF、文件名、文件名.dtadjust 文件名.datetime 文件修改日期和参数
    返回信息。
    
    如果fn里面没有exif，则返回None
    如果有make/model，则简化后放入字典
    如果有datetime相关字段，则放入字典
    如果forceraw，则只从原始文件中读取，此时allowmeta实际上不起作用了
    forceraw基本上不用，仅仅用于调试目的
    '''
    def _getmake(longmake):#longmake!=None
        if not shortmakemodel:
            return longmake
        easyname={'EASTMAN KODAK COMPANY':'KODAK', }
        longmake = easyname.get(longmake.upper(),None) or longmake
        name=longmake.split()
        return name[0] if len(name)>0 else ''
            
    def _getmodel(longmodel, make): #longmodel!=None
        if not shortmakemodel:
            return longmodel
        useless='ZOOM DIGITAL CAMERA'
        easyname={'powershot':'PS', 'finepix':'FP',}
        #去掉make和useless，换掉easyname
        m = make if make else ''
        return '-'.join( [(easyname.get(w.lower(),None) or w) for w in longmodel.split() \
                                if (useless.lower().find(w.lower())==-1 \
                                    and m.lower()!=w.lower())] )
    
    tags={}
    exif=None
    if os.path.splitext(fn)[1].lower() == ".jpg":
        #好像MOV、MTS等文件没有Exif
        try:
            exif = pyexiv2.ImageMetadata(fn)
            exif.read()
        except Exception:
            pass
    else:
        tags["DateTime"]=time.strftime("%Y:%m:%d %H:%M:%S",time.localtime(os.stat(fn).st_mtime))
        
    if exif:
        try:
            make=_getmake(exif['Exif.Image.Make'].raw_value)
            if make is not None:
                tags['Make'] = make
        except Exception: pass
        
        try:
            model= _getmodel(exif['Exif.Image.Model'].raw_value, make)
            if model is not None:
                tags['Model'] = model.replace(",","-") #有的型号里面有,
        except Exception: pass
        
        dt = exif.get("Exif.Photo.DateTimeOriginal",None) or \
             exif.get("Exif.Image.DateTime",None) or \
             exif.get("Exif.Photo.DateTimeDigitized",None)
        #有些照片的前两个不同，第二个明显不对。
        if dt is not None:                   
            tags["DateTime"]= dt.raw_value
        
        if (not tags) and (not forceraw):
            tags["DateTime"]=time.strftime("%Y:%m:%d %H:%M:%S",time.localtime(os.stat(fn).st_mtime))
        #有些IPHONE拍摄的相片，有EXIF，但是没有Model/Make/DateTime。可能是导入工具的问题。
        #这些可以通过文件修改日期来推测出。目前只有IPHONE相片有这个问题。有些是其他应用存入IPHONE的。
        
    if not forceraw:
        #如果是规整后的文件，则用使用文件名中的日期
        (dt,note,size) = _trygeninfofromname(fn)
        if dt is not None:
            tags["DateTime"] = dt
            
    if allowmeta and (not forceraw):
        try:
            with open(fn[:-3]+"datetime","r") as f:
                tags["DateTime"]=f.readline()
        except Exception:
            pass
            
    if not forceraw:
        #手工调整的，必须无条件加载，所以人工的必须手工删除
        try:
            with open(fn[:-3]+"dtadjust","r") as f:
                tags["DateTime"]=f.readline()
        except Exception:
            pass
        
    return tags if (len(tags)>0 or exif) else None

    
def _trygetnote(fn,root,pcache=False, cache={}):
    '''根据文件名、根目录去生成文件Note'''
    if pcache: #只是用来打印字典的
        #这里展现的是缺省参数只创建一次的Python机制
        print len(cache)
        print u"\n".join([u"{}:{}".format(k,v) for (k,v) in cache.iteritems()])
        return None
        
    (dt,note,size)=_trygeninfofromname(fn)
    if root is None:
        return note if note else ""
        
    if note:
        #如果是规范后的，则取note备用，只分析路径
        fn=os.path.split(fn)[0]
        note=note[1:-1] #删除前后括弧，因为后面要添加
    
    def removeall(n, usecache):
        replacefns=((ur"[_－，&\-\.\[\]]+"," "),(ur'([^a-z])[a-z]([^a-z])',ur'\1\2'), )
        uselessfns=('CIMG','IMG','IMAG','DSC[ \da-z]{5,}',
                    '^P[a-z]*[ \d]{5,}','^A[ \d]{5,}','^S[ \d]{5,}','^L[ \d]{5,}',
                    ur"新建文件夹",ur'图像',ur'小图',ur'副本',ur'复件',ur'复制',ur'旋转',ur'pic',
                    ur'image',ur'mov',ur'未标题',ur'照片',
                    ur'数码',ur'Olympus',ur'Olyms',ur'iphone',ur'AVSEQ',ur"vts",ur"msdcf",
                    ur'ip4.g',ur'sony hz',ur'2bb',ur'OLYMP','Delia X',ur"DCIM",ur'XX',ur'New Folder',
                    ur'PRIVATE',ur'AVCHD', ur'BDMV', ur'STREAM',
                    ur'\d张',ur'\d寸',ur'\d册',
                    ur'[~\d\(\)]',ur'^[ ]+',ur'[ ]+$',ur'^[a-z]$')
        if usecache:           
            c = cache.get(n,None)
            if c is not None:
                return c
            key=n
        
        for (a,b) in replacefns:
            n=re.sub(a,b,n,0,re.U|re.I)
        for u in uselessfns:
            n=re.sub(u,'',n,0,re.U|re.I)
        
        if usecache:
            cache[key]=n
        return n
    
    r=root.replace(u"/",u" ").replace(u"\\",u" ").split()
    names=os.path.splitext(fn)[0].replace(u"/",u" ").replace(u"\\",u" ").split()[len(r):]
    
    if note is not None:
        names=[removeall(n, True) for n in names]
        names.append(note)
    else:
        names1=[removeall(n, True) for n in names[:-1]]
        names1.append(removeall(names[-1], False))
        names=names1
        #只有对路径才在cache里面去找，文件名不需要
        
    names=[n for (i,n) in enumerate(names) \
            if len(n)>0 and (i==len(names) or (not (any(son.find(n)!=-1 for son in names[i+1:])))) ]
    #如果前面的目录名在后面出现过来，就去掉
    
    return u'({})'.format(u' '.join(names)) if names else u""
    #加上括弧

def printgennote(path,root):
    lastnote=None
    for fn in gpylib.misc.walkfiles(path, _WALK_CONDITION, False):
        note = _trygetnote(fn,root)
        if note!=lastnote:
            print note
            lastnote=note    

def printgennotecurrentdir():
    printgennote(os.getcwdu(),os.getcwdu())      
    
if __RUN_CURRENT_FILE__: 
    pass
    
    #_testgennote(ur'C:\Temp\2004.1000 Yunnan',"C:\Temp")
    #printgennote(ur'I:\Pics\071108',ur"I:\Pics\071108",ur".jpg")
    #print _trygetnote(ur'C:\Temp\2004.1000 Yunnan\5.丽江\9.28丽江过中秋\DSC100_1635.jpg', ur'C:\Temp')
    #print _trygetnote(ur'C:\Temp\2004.1000 Yunnan\1.泸沽湖\9.26~9.28泸沽湖-扎西聊吧\100_1635.jpg', ur'C:\Temp')
    #print _trygetnote(ur'C:\Temp\2004.1000 Yunnan\5.丽江\9.28丽江过中秋\2004-09-26_000001(Yunnan 泸沽湖 扎西聊吧)_B50F9.jpg', ur'C:\Temp')
    
def _genname(fn, exifs=None, allowmeta=False, shortmakemodel=True, root=None, size=0, note=None, id=None):
    '''规范名字: size=0意味着要本函数去取文件大小，size=None意味着不需要这个字段,size>0，则用此size'''
    exifs=exifs or _getinfo(fn, allowmeta, shortmakemodel)
    
    try:
        return u"{}{}{}{}{}".format(
              time.strftime("%Y-%m-%d_%H%M%S", time.strptime(exifs['DateTime'], "%Y:%m:%d %H:%M:%S")),
              note if note else _trygetnote(fn,root),
              "" if size is None else "_{:X}".format(size if size>0 else os.stat(fn).st_size),
              "" if id is None else "-{:X}".format(id),
              os.path.splitext(fn)[1]
              )  
    except Exception as e: #exif为None，或者DateTime或者没有DateTime不合法
        return None
        
def _gennamelong(fn, exifs=None, allowmeta=False, shortmakemodel=True, root=None, size=0):
    #此函数没有用了
    exifs=exifs or _getinfo(fn, allowmeta, shortmakemodel)
    
    try:
        return u"{}{}{}{}{}{}".format(
              time.strftime("%Y-%m-%d_%H%M%S", time.strptime(exifs['DateTime'], "%Y:%m:%d %H:%M:%S")),
              _trygetnote(fn,root) if root else "",
              "_"+exifs['Make'] if exifs.get('Make', None) else "",
              "-"+exifs['Model'] if exifs.get('Model',None) else "",
              "_{:X}".format(size if size else os.stat(fn).st_size) if size>=0 else "",
              os.path.splitext(fn)[1])  
    except Exception as e: #exif为None，或者DateTime或者没有DateTime不合法
        return None

def printgenname(path,root):
    for fn in gpylib.misc.walkfiles(path, _WALK_CONDITION, False):
        name = _genname(fn, exifs=None, allowmeta=True, shortmakemodel=True, root=root)
        print fn
        print "\t", RED+fn if not name else name          
        
def printgennamecurrentdir():
    printgenname(os.getcwdu(),os.getcwdu())      
            
if __RUN_CURRENT_FILE__: 
    pass
            
    #_testgenname(ur'I:\Pics\071108',"I:\Pics\071108")
    #print _genname(ur"C:\Temp\2004.1000 Yunnan\4.虎跳峡\10.4虎跳峡-中峡探险\IMG_1780.JPG",True,True,True,'云南')



'''**************************************************************'''
'''第二部分：统计************************************************'''
        
class _PicCensus(object):
    def __init__(self, allowmeta=False):
        self.noexifs, self.mmnodts, self.nomms, self.nommdts, self.zeordts = [], [], [], [], []
        self.models, self.ymds=collections.defaultdict(int),collections.defaultdict(int)
        self.count, self.allowmeta = 0, allowmeta
        self.sizes = collections.defaultdict(list)
        
    def add(self,fn): #fn是unicode，因为有些目录名或者文件名真的是unicode编码的
        self.count +=1
        tags=_getinfo(fn,self.allowmeta)
        
        if tags is None:
            self.noexifs.append(fn)
        else:
            make,model,dt=tags.get('Make',None),tags.get('Model',None),tags.get('DateTime',None)

            if make==model==None:
                if dt is None:
                    self.nommdts.append(fn)
                else:
                    self.nomms.append((fn,dt))
            else:
                self.models[(make,model)] += 1
                
            if dt is None:
                if not(make==model==None):
                    self.mmnodts.append((fn,'No DateTime[{}]:[{}]'.format(make,model)))
            elif dt=='0000:00:00 00:00:00':
                self.zeordts.append(fn)
            elif re.match(r'\d{4}.\d\d.\d\d',dt):
                self.ymds[dt[:10]] += 1
                self.sizes[os.stat(fn).st_size].append( (fn,dt ) )
            else:
                self.mmnodts.append((fn,dt))
        return tags
    
    def adddir(self,path):
        for f in gpylib.misc.walkfiles(path, _WALK_CONDITION, True):
            self.add(f)
            
    def printme(self):
        print "Total ",self.count
        print "\n", RED+"No Exif", len(self.noexifs)
        print u"\n".join(self.noexifs)
        
        print "\n", RED+"No MMDT", len(self.nommdts)
        print u"\n".join(self.nommdts)
        
        print "\n", RED+"No MM", len(self.nomms)
        print u"\n".join([u"{}\n\t{}".format(*item) for item in self.nomms])
        
        print "\n", RED+"Zero DT", len(self.zeordts)
        print u"\n".join(self.zeordts)
        
        print "\n", RED+"MM No DateTime", len(self.mmnodts)
        print "\n".join([u"{}\n\t[{}]".format(f,d) for f,d in self.mmnodts])
        
        print "\n", BLUE+"Date Time", len(self.ymds)
        print "\n".join(["{}\t{}".format(d,c) for (d,c) in sorted(self.ymds.items())])
        
        print "\n", BLUE+"Make Models", len(self.models)
        print "\n".join(["{}\t\t{}".format(m,c) for (m,c) in self.models.iteritems()])
        
        print "\n", RED+"No MM Paths", len(self.nomms)
        print u"\n".join(sorted(set(os.path.split(fn)[0] for (fn,dt) in self.nomms)))
        
        print "\n", RED+"Zero DT Paths", len(self.zeordts)
        print u"\n".join(sorted(set(os.path.split(fn)[0] for fn in self.zeordts)))
        
        #相同size、相同MD5 但是Datatime不同的，这样备份后会重复。
        #相同size、相同Datetime，不同MD5的，这样比较Funny
        #三个都相同的，会在备份的时候自然只会选择一个
        
        def THOSE_VALUE_MORE_THAN_ONE(d):
            return filter(lambda x: len(x[1])>1, d.iteritems())
        
        for (size,fndts) in THOSE_VALUE_MORE_THAN_ONE(self.sizes):
            dt_md5s = defaultdict(lambda: defaultdict(list))
            md5_dts = defaultdict(lambda: defaultdict(list))
            dtmd5_fns = defaultdict(list)
            for (fn,dt) in fndts:
                md5=gpylib.misc.getmd5(fn)
                dt_md5s[dt][md5].append(fn)
                md5_dts[md5][dt].append(fn)
                dtmd5_fns[(dt,md5)].append(fn)
            
            for (dt,md5s) in THOSE_VALUE_MORE_THAN_ONE(dt_md5s): 
                #Funny: size,datetime相同，但是MD5不同
                gprint("\n<> [<>] [<>]\n",BLUE+"Funny",size, dt)
                gpylib.misc.ppdict(md5s,u"    [",u"]", u"        ",u"")
                #这个item是 key/list
                
            for (md5, dts) in THOSE_VALUE_MORE_THAN_ONE( md5_dts): 
                #重复: size,MD5相同，但是DateTime不同
                gprint("\n<> [<>] [<>]\n",YELLOW+"Duplicate",size, md5)
                gpylib.misc.ppdict(dts,u"    [",u"]", u"        ",u"")
            
            for ((dt,md5),fns) in THOSE_VALUE_MORE_THAN_ONE( dtmd5_fns):
                #有size,md5,DateTime都相同的情况
                gprint("\n<> [<>] [<>] [<>]\n    ", GREEN+"Same File", size, dt, md5)
                print u"\n    ".join(fns)
               
def countthisdir(dir,allowmeta):
    print "Allow Meta [{}]".format(allowmeta)
    with gpylib.misc.gt("开始统计...\n", "{:.1f}秒\n"):
        pa = _PicCensus(allowmeta)
        pa.adddir(dir)
        pa.printme()

def countcurrentdir(allowmeta):
    countthisdir(os.getcwdu(),allowmeta)
    #必须使用unicode，因为有些目录名或者文件名是Unicode的，如果不用，则os.walk列不出来

if __RUN_CURRENT_FILE__: 
    pass
    #countthisdir(ur"C:\Temp\2004.1000 Yunnan",True)
    #countthisdir(ur"E:\Temp\091102\2008-11-25",False)
    #countthisdir(ur"C:\Temp\1.泸沽湖")

    
'''**************************************************************'''
'''第三部分：更正日期********************************************'''

def _guessdate(fnn):
    fn = fnn if os.path.isdir(fnn) else os.path.split(fnn)[0]
    
    years1 = re.findall(ur'[/\\](\d{4})[_\-\.]',fn, re.U)  
    #目录名以四个数字开始，后面紧跟着. _ -的，找出现在最后面的
    years2 = re.findall(ur'[/\\](\d\d)\d{4}[_\-\./\\]',fn, re.U)
    #目录名以六个数字开始，后面紧跟. _ - / \，也找最后一个
    y = years1[-1] if years1 else ("20"+years2[-1] if years2 else None )
    
    md1 = re.findall(ur'[^\d]\d{4}[_\-\.](\d{1,2})[_\-\.]{0,1}(\d{0,2})',fn, re.U) 
    #2003.1001 2009.01.29 2008.1.2 2008.1
    
    md2 = re.findall(ur'[^\d]\d\d(\d\d)(\d\d)[_\-\./\\]',fn, re.U) #091102
    md3 = re.findall(ur'[^\d](\d{1,2})\.(\d{1,2})[^\d]',fn,re.U) #\10.1
    (m,d)=md3[0] if md3 else (md1[-1] if md1 else ( md2[-1] if md2 else (None,None)))
    
    y,m,d = int(y if y else 0),int(m if m else 0),int(d if d else 0)
    d= 1 if (y and m and not d) else d
    
    return y,m,d

def _guessdatetime(fn):
    y,m,d =_guessdate(fn)
    try:
        return datetime.datetime(y,m,d)
    except Exception:
        return None
    
class _PicDateTimeCheck(object):
    def __init__(self,root,datebegin,dateend, allowmeta=False, datetimegener=None,
                genop={'noexif':True, 'nodt':True, 'outdt':True, 'zeordts':True, 'errordt':False},
                manualadjust=False):
        def _trygendatetime(t):
            self.result[t].append(fn)
            if datetimegener is None or not genop.get(t,None):
                return
            print "\n", t    
            dt= datetimegener(fn)
            if dt is None:
                return
            
            dtfn=fn[:-3]+ ("dtadjust" if manualadjust else "datetime")
            with open(dtfn,"wt") as f:
                f.write(dt)
                
        self.root, self.datebegin, self.dateend = root,datebegin,dateend
        self.datetimegener = datetimegener
        self.datetime0=self.datetime1=None
        self.result,self.pathdts = collections.defaultdict(list),collections.defaultdict(lambda:[None,None])
        self.guessdts={}
        
        for fn in gpylib.misc.walkfiles(root, _WALK_CONDITION, True):
            path = os.path.split(fn)[0]
            if self.guessdts.get(path,False) == False:
                self.guessdts[path] = _guessdatetime(path)
                #缓存一下而已
                
            tags=_getinfo(fn,allowmeta)
            if tags is None:
                _trygendatetime('noexif')
                continue
            dt=tags.get('DateTime',None)
            
            if dt is None:
                _trygendatetime('nodt')
            elif dt=='0000:00:00 00:00:00':
                _trygendatetime('zeordts')
            else:
                try:
                    dtdt = datetime.datetime.strptime(dt,"%Y:%m:%d %H:%M:%S")
                    if datebegin <= dtdt <= dateend:
                        self.datetime0 = dtdt if self.datetime0 is None else min(self.datetime0,dtdt)
                        self.datetime1 = dtdt if self.datetime1 is None else max(self.datetime1,dtdt)
                        
                        pathdtxy=self.pathdts[path]
                        pathdtxy[0] = dtdt if pathdtxy[0] is None else min(pathdtxy[0],dtdt)
                        pathdtxy[1] = dtdt if pathdtxy[1] is None else max(pathdtxy[1],dtdt)
                        
                        if self.guessdts[path] and abs((dtdt-self.guessdts[path]).days)>90:
                            self.result['dtmayerror'].append(fn)
                    else:
                        _trygendatetime('outdt')
                except Exception as e:
                    _trygendatetime('errordt')
        
    def printme(self):
        lastp=u''
        for t,fns in self.result.iteritems():
            print "\n\n", RED+t, len(fns)
            for fullpath in fns:
                p,fn= os.path.split(fullpath)
                if p!=lastp:
                    print p
                    lastp=p
                print "\t", fn
            
        for t,fns in self.result.iteritems():
            gprint("\n\n<> can be guessed as:",t)
            for p in sorted(set(os.path.split(fn)[0] for fn in fns)):
                dt0,dt1,guess=self.pathdts[p][0],self.pathdts[p][1],self.guessdts[p]
                c0,c1,color =  (guess is None) and ("","",RED) or\
                               (dt0 is None) and ("","",YELLOW) or\
                               {(True,True):("","",GREEN), (False,False):("","",RED), 
                                  (True,False):("",RED,""),  (False,True):(RED,"",""),
                               }[(abs( (dt0-guess).days )<90, abs( (dt1-guess).days )<90)]
                            
                gprint('\n\t<>\n\t\t[<>, <>] <>\n', p,
                       (c0 + dt0.strftime("%Y-%m%d")) if dt0 else '',
                       (c1 + dt1.strftime("%Y-%m%d")) if dt1 else '',
                       color + (guess.strftime("%Y-%m%d") if guess else "GUESSFAILED") )
        
        c=sum([len(fns) for (k,fns) in self.result.iteritems() if k !='dtmayerror'])
        print RED+"{} files cannot be archived.".format(c) if c else GREEN+"All files can be archived."
        if self.datetimegener is not None:
            print GREEN + "After gen, You can check again."
                
class _DateTimeGen(object):
    history = defaultdict(lambda: "")
    #字典保证如果需要更正时间的文件存在冗余的时候，能够返回同一个日期
    #否则就会产生两个日期，最终造成备份冗余了。
    def __init__(self,base,skip, step):
        self.base, self.skip, self.step, self.i=base, skip, step, skip
        self.guessymds = {}
        
        
    def __call__(self,fn):
        print fn
        md5 = gpylib.misc.getmd5(fn)
        if _DateTimeGen.history[md5] == '':
            #从来没有猜测过时间
            y,m,d=_guessdate(fn)
            if y and m and d:
                if self.guessymds.get((y,m,d),None) is None: 
                    self.guessymds[(y,m,d)]=self.skip
                else:
                    self.guessymds[(y,m,d)] += self.step
                result= (datetime.datetime(y,m,d)+datetime.timedelta(0,self.guessymds[(y,m,d)])).\
                        strftime("%Y:%m:%d %H:%M:%S")
            elif self.base:
                self.i += self.step
                result = (self.base+datetime.timedelta(0,self.i)).strftime("%Y:%m:%d %H:%M:%S")
            else:
                result=None
            _DateTimeGen.history[md5] = result
        else:
            #猜测过，及时是None，也返回
            result = _DateTimeGen.history[md5]
            print BLUE+"Duplicated file"
         
        print GREEN+result if result else RED+"NONE"
        return result

def checkthisdir(dir,dt1,dt2,allmeta,gen,option,manual=False):
    print "Allow Meta", allmeta
    with gpylib.misc.gt("开始检查日期...\n", "{:.1f}秒\n"):
        _PicDateTimeCheck(dir, dt1,dt2,allmeta,gen,option,manual).printme()

def gendtcurrentdir(allowmeta):
    checkthisdir(os.getcwdu(),
                datetime.datetime(1900,1,1), datetime.datetime(2100,1,1),
                allowmeta,
                _DateTimeGen(None,3601, 2), #从第二个小时开始，而且只是奇数
                {'noexif':True,'zeordts':True,'outdt':True})
    
def checkcurrentdir(allowmeta):
    checkthisdir(os.getcwdu(),
                datetime.datetime(1900,1,1), datetime.datetime(2100,1,1),
                allowmeta,
                None,
                {})
        
if __RUN_CURRENT_FILE__: 
    a=44
    if a==1:    
    #生成辅助时间戳 {'noexif':True, 'nodt':True, 'outdt':True, 'zeordts':True, 'errordt':True}
    #每次使用之前，必须手工删除目录下的 dtadjust 文件。
        checkthisdir(ur"E:\Temp\071108\2004.1000 Yunnan",
                datetime.datetime(2004,9,1), datetime.datetime(2004,11,1),
                False,
                _DateTimeGen(datetime.datetime(2004,9,25),0,2), #偶数
                {'outdt':True},True) #仅仅只修正超出时间范围的，并且是人工修正
    elif a==2:
    #检查时间戳
        checkthisdir(ur"E:\Temp\071108\2004.1000 Yunnan",
                datetime.datetime(2004,9,1), datetime.datetime(2004,11,1),
                True,
                None,
                {})
    elif a==3:
        checkthisdir(ur"E:\Temp\101107",
                datetime.datetime(2009,1,1), datetime.datetime(2011,1,1),
                True,
                None,
                {})
    

'''**************************************************************'''
'''第四部分：归档************************************************'''
    
class _PicFile(object):
    totalsize=0
    totalfile=0
    totalmd5=0
    
    def __init__(self, fullname, rootdir):
        #如果rootdir is none: 是已经归档的文件
        self.fullname, self.rootdir= fullname, rootdir
        self._size = self._md5 = self._newnote = self._newname = self._nameflag = None

        if rootdir is None:
            self.exif, self._note =_getarchiveinfodtonly(fullname)
        else:
            self.exif = _getinfo(fullname,allowmeta=True,shortmakemodel=True, forceraw=False)
            self._note= _trygetnote(self.fullname,self.rootdir)
            
        if self.exif is None:
            print RED+fullname
            raise PicException, "No Exif"
            
        _PicFile.totalfile +=1
        
    def dump(self,newdir,fake,movenewfile):
        newfullname = os.path.join(newdir,self.name)
        if newfullname.lower()==self.fullname.lower():
            return "File No Action"
            
        '''gprint("<>\n\t<>\n\t<>\n", 
                "move" if (movenewfile or self.rootdir is None) else "copy", 
                self.fullname,newfullname)
        '''
        (out,action,ret) =  (self.rootdir is None) and (GREEN+"M", shutil.move,  "Move Archive") or \
                                       movenewfile and (  RED+"M", shutil.move,  "Move New") or \
                                                       (      "C", shutil.copy2, "Copy New")
        gprint(out)
        if not fake:
            action(self.fullname, newfullname)
        self.fullname,self.rootdir=newfullname, None
        return ret
    
    @property
    def datetime(self):
        return self.exif['DateTime']
    
    @property
    def nameflag(self):
        return self._nameflag
    
    @property
    def name(self):
        return self._newname if self._newname else os.path.split(os.fullname)[1]
        #genname调用后才有意义
    
    @property
    def easyhash(self):
        path, fn = os.path.split(self.fullname)
        dir=os.path.split(path)[1]
        
        return u"{}{}{}".format(dir,fn,self.size)
        
    def genname(self,pre,idx):
        #这个必须在整个文件都添加好后再调用。需要根据之前的那个文件来判断是否需要把size、idx放入文件名
        if self._newname is None:
            s= self.size if (pre is not None and pre.datetime == self.datetime and pre.size!=self.size) else None
            #如果PRE的日期和当前的相同，但是大小不同，则需要把大小放入文件名
            i = idx if (pre is not None and pre.datetime == self.datetime and pre.size==self.size) else None
            #如果PRE和当前的日期、大小都相同，则需要把idx放入文件名
            self._newname = _genname(self.fullname, self.exif, allowmeta=True, shortmakemodel=True, 
                                     root=self.rootdir, size=s, note=self.note,id=i)
            self._nameflag = ("N" if self.note else"")+("S" if s else "")+("I" if i else "")
            
            if s or i:
                self._pre=pre
        return self._newname

    @property
    def size(self):
        if self._size is None:
            self._size= os.stat(self.fullname).st_size
            _PicFile.totalsize+=1
        return self._size
        
    @property
    def md5(self):
        if self._md5 is None:
            self._md5= gpylib.misc.getmd5(self.fullname)
            _PicFile.totalmd5+=1
        return self._md5
        
    @property
    def note(self):
        return self._newnote if self._newnote is not None else self._note
    
    def __cmp__(self,other):
        if not isinstance(other,_PicFile):
            return NotImplemented
            
        return cmp( self.exif['DateTime'], other.exif['DateTime']) or \
               cmp( self.size, other.size) or\
               cmp( self.md5, other.md5)
        
    def cmptime(self,other):
        return cmp(self.exif['DateTime'], other.exif['DateTime'])
    
    def updatenoteiflonger(self,pf):
        if len(pf.note)>len(self.note):
            self._newnote=pf.note
            return True
        else:
            return False
        
        
class _PicGroup(object):
    def __init__(self, path, basepath, pics, clean):
        #path/bashpath都是全路径；如果是一个新组，则path是None
        self.path, self.basepath, self.pics, self.clean = path,basepath,pics,clean
    @staticmethod
    def mirror(path, md5dict):
        '''从归档目录读取'''
        pg = _PicGroup(path, os.path.split(path)[0], [], True)
        print "Loading", path
        for f in os.listdir(path):
            fullname = os.path.join(path,f)
            if os.path.isfile(fullname) and _WALK_CONDITION(f):
                pf = _PicFile(fullname, None)
                bisect.insort_left(pg.pics, pf)
                md5dict[pf.size].append( pf )
        return pg
    
    @staticmethod
    def newone(basepath,pf):
        '''创建一个新的组，pf是第一个成员'''
        pg = _PicGroup(None, basepath, [], True)
        pg.add(pf)
        return pg
        
    def __cmp__(self,other):
        if isinstance(other,_PicGroup):
            return self.pics[0].cmptime(other.pics[0])
        elif isinstance(other,_PicFile):
            if self.pics[-1].cmptime(other)<0:
                return -1
            elif self.pics[0].cmptime(other)>0:
                return 1
            else:
                return 0
        else:
            return NotImplemented
            
    def add(self, pf):
        i=bisect.bisect_left(self.pics, pf)
        if i!=len(self.pics) and self.pics[i]==pf:
            #有重复的文件，因为PICArchive在添加前已经经过MD5检查过重复了，因此这个实际上不可能发生了
            #gprint("<>:\n\tOLD: <>\n\tNEW: <>\n",YELLOW+"Same File",self.pics[i].fullname, pf.fullname) 
            if not self.pics[i].updatenoteiflonger(pf):
                return "Old", self.pics[i]
            else:
                self.clean=False
                return "Overwrite", self.pics[i]
                
        self.pics.insert(i,pf)
        self.clean=False
        return 'New', None
    
    def count(self):
        return len(self.pics)
        
    def split(self):
        i=len(self.pics)/2
        while i>0 and self.pics[i].cmptime(self.pics[i-1])==0:
            i-=1
            #相同时间的文件必须保留在一个目录下面
        
        if i<=0:
            return None
            #前一半的所有文件的时间都相同
        #i对应的在后一半
        
        if self.path is not None and os.path.split(self.path)[1] <= self.pics[i-1].datetime.replace(':','-'):
            #path的名字代表的时间处于左半边，则扔掉右半边
            #需要保证path名字代表的时间永远都在path的pics区间
            pg = _PicGroup(None,self.basepath,self.pics[i:],False)
            del self.pics[i:]
        else:
            #扔掉左半边
            pg = _PicGroup(None,self.basepath,self.pics[:i],False)
            del self.pics[:i]
        #gprint("\nSplited to <>:<>\n",self.count(),pg.count())
        return pg
        #Archive会排序插入，因此不用担心
    
    def gennames(self):
        if self.clean:
            return
            
        lpf=None
        for i,pf in enumerate(self.pics):
            pf.genname(lpf,i)
            lpf=pf
    
    def printonlysi(self):
        gprint("\nGroup [<>]\n\t", BLUE+str(len(self.pics)))
        print "\n\t".join([u"{}\n\t\t{}\n\t\t{}".format(pf.name,pf.fullname,pf._pre.fullname) for pf in self.pics \
                    if re.match(ur"^N{0,1}[SI]+$",pf.nameflag,re.U)!=None])
        #对于有Size和Index的，人工检查一下是否有同一时刻的照片。
        
    def printdebug(self, step=50):
        gprint("\nGroup [<>]\n\t", BLUE+str(len(self.pics)))
        print "\n\t".join(pf.name for pf in self.pics[::step])
        #每多少个照片打印一个
        
    def printse(self):
        gprint("\nGroup [<>]\n\t", BLUE+str(len(self.pics)))
        print "\n\t".join(pf.name for pf in [self.pics[0],self.pics[-1]])
        #只打印头尾

    def dumpstep2(self, fake, actions):
        '''要分两步，是因为第一步要move文件。如果src的目录名变化了，那么就无法移动了'''
        if self.clean:
            return
            
        newpath=os.path.join(self.basepath, self.pics[0].datetime.replace(":","-"))    
        if self.path.lower()==newpath.lower():
            return
            
        print "\nren", self.path, newpath
        actions['Rename Dir']+=1
        if not fake:
            os.rename(self.path,newpath)
            self.path = newpath
            for p in self.pics:
                p.fullname=os.path.join(newpath,p.name)
                
        self.clean=True
        
    def dumpstep1(self, fake, movenewfile, actions):
        if self.clean or self.count()==0:
            actions['Dir No Action'] +=1
            return
        
        print "\n\n",
        if self.path is None: #还没有创建过
            self.path=os.path.join(self.basepath, self.pics[0].datetime.replace(':',"-"))
            
            actions['MkDir'] +=1
            print "mkdir",self.path
            if not fake:
                os.mkdir(self.path)
        else:
            print self.path
            
        gprint("[<>] Files\n", len(self.pics))
        for p in self.pics:
            actions[p.dump(self.path,fake,movenewfile)] +=1
        
class _PicArchive(object):
    def __init__(self, path, max=200):
        self.groups, self.path, self.max=[],path,max
        self.duplicatefiles, self.old, self.overwrite, self.failed = [],[],[],[]
        self.md5dict=defaultdict(list)
        
        print BLUE+BWHITE+"\nLoading archive ..."
        for d in os.listdir(path):
            fullpath = os.path.join(path,d)
            if os.path.isdir(fullpath) and \
                re.match(r"^\d{4}-\d\d-\d\d \d\d-\d\d-\d\d$",d) is not None:
                bisect.insort_left(self.groups,_PicGroup.mirror(fullpath,self.md5dict))
    
    def findsamefile(self,pf):
        pfmd5s = self.md5dict.get(pf.size,None)
        if pfmd5s is None:
            return None
        
        for pfmd5 in pfmd5s:
            if pfmd5.md5 == pf.md5:
                return pfmd5
        else:
            return None
        
    def selftest(self, verbose=False):
        lastpg=None
        errorcount=0
        
        md5 = hashlib.new('md5')
            
        print BLUE+BWHITE+"\n\nSelf Testing"
        for pg in self.groups:
            if verbose:
                gprint("[<>] - [<>] : <> Files.\n", pg.pics[0].datetime, pg.pics[-1].datetime, BLUE+"{:03d}".format(len(pg.pics)) )
                
            if lastpg is not None and lastpg.pics[-1].cmptime(pg.pics[0])>=0:
                errorcount+=1
                gprint("<>\n\t<>\n\t<>\n", RED+"Error Found: Group split", lastpg.path, pg.path)
            lastf=None
            for f in pg.pics:
                md5.update(f.easyhash.encode("gb2312"))
                if lastf is not None and lastf.cmptime(f)>0:
                    errorcount+=1
                    gprint("<>\n\t<>\n\t<>\n", RED+"Error Found: File Order", lastf.fullname, f.fullname)
                lastf=f
            lastpg=pg
            
        gprint("\nCheck end, [<>] errors found.\nDigest[<>]\n", 
                            (RED if errorcount else GREEN) + str(errorcount),
                            BLUE+md5.hexdigest() )

    def add(self, fn, rootdir):
        pf = _PicFile(fn,rootdir)
        samefile = self.findsamefile(pf)
        #根据MD5去找
        if samefile:
            pf.exif=samefile.exif
            #更新其日期而已这样后面才能找到

        if len(self.groups)==0:
            self.groups.append(_PicGroup.newone(self.path,pf))
            return
            
        for g in self.groups:
            if pf<=g:
            #如果pf比第一个组还要小，那么就加入到第一个组了
            #如果pf在两个组中间，则添加到后一个组里面
            #如果pf比任何一个组都要大，则添加到最后一个组
                break
        
        re, refpf = g.add(pf)
        if re=="Old":
            gprint(DIM+"O")
            self.old.append( (pf,refpf) )
        elif re=="Overwrite":
            gprint(YELLOW+"W")
            self.overwrite.append( (pf,refpf) )
        else: #'New'
            self.md5dict[pf.size].append( pf )
            gprint(GREEN+"N")
            if(g.count()>=self.max):
                ng=g.split()
                if ng is not None:
                    bisect.insort_left(self.groups,ng)
                
    def adddir(self, path, rootdir):
        gprint("\nAdding [<>] to archive\n", BLUE+BWHITE+path) 
        fns= [f for f in gpylib.misc.walkfiles(path, _WALK_CONDITION, True,"\n\n")]
        gprint(RED+"Randoming the files\n")
        random.shuffle(fns)
        for fn in fns:
        #for fn in gpylib.misc.walkfiles(path, _WALK_CONDITION, True,"\n\n"):
            try:
                self.add(fn, rootdir)
            except PicException as e:
                self.failed.append(fn )
        print "\n"
        
    def dump(self,fake,movenewfile):
        self._dumpactions=defaultdict(lambda:0)
        print BLUE+BWHITE+"\nDumping" + (" Fake" if fake else "")
        print (RED+BWHITE+"Moving files") if movenewfile else (BLUE+BWHITE+"Copying files")

        for g in self.groups:
            g.dumpstep1(fake, movenewfile,self._dumpactions)
        
        for g in self.groups:
            g.dumpstep2(fake,self._dumpactions)
        print "\n"
        
    def gennames(self):
        print BLUE+BWHITE+"Generating Names..."
        for gp in self.groups:
            gp.gennames()
        print "\n",
        
    def printdumpinfo(self):
        print BLUE+BWHITE+"Dump information\n"
        print "Old", BLUE+str(len(self.old))
        print u"".join([u"{}\n\t{}\n\n".format(new.fullname, old.fullname) for new,old in self.old])
        
        print "\n", YELLOW+"Overwrite", BLUE+str(len(self.overwrite))
        print u"".join([u"{}\n\t{}\n\n".format(new.fullname, old.fullname) for new,old in self.overwrite])

        print "\n", RED+"Failed", len(self.failed)
        print u"\n".join(self.failed)
    
        print "Actions:{"
        gpylib.misc.ppdict(self._dumpactions,prekey=u" "*4, prevalue=u" "*8)
        print "}"
        
        gprint("\nTotal file [<>], readsize [<>], readmd5 [<>]\n", _PicFile.totalfile,
                _PicFile.totalsize, _PicFile.totalmd5)
        gprint("MD5 Cache Size [<>], reachcount [<>]\n", *gpylib.misc.getmd5.status )        
        

def autobakpics(picdir,rootdir,archivedir,movenewfile):
    with gpylib.misc.gt(BLUE+BWHITE+"Archiving...\n", "{:.1f}秒\n"):
        pa = _PicArchive(archivedir)
        pa.adddir(picdir,rootdir)
        pa.gennames()
        pa.selftest(True)
        pa.dump(False,movenewfile)
        pa.printdumpinfo()
        
def autobakpiccurrentdir(archivedir, movenewfile):
    '''[t bk "I:\PicArchive"]'''
    autobakpics(os.getcwdu(), os.getcwdu(), archivedir, movenewfile)
    
def picarchiveselftest(archivedir):
    with gpylib.misc.gt("Archive Self Check...\n", "{:.1f}秒\n"):
        print "开始检查"
        pa = _PicArchive(archivedir)
        pa.selftest(True)
        
def picarchiveselftestcurrentdir():
    '''[t jca]'''
    picarchiveselftest(os.getcwdu())
        
if __RUN_CURRENT_FILE__:
    pass
    #autobakpics(ur"I:\Temp\071108\2004.1000 Yunnan", ur"I:\Temp", ur"I:\PicArchive1")
    #autobakpics(ur"E:\Test", ur"E:\Test", ur"E:\PicArchive")
    #autobakpics(ur"I:\Temp", ur"I:\Temp", ur"I:\PicArchive")
    
    #picarchiveselftest(ur"I:\PicArchive1")
    #picarchiveselftest(ur"I:\PicArchive") 
    #_trygetnote(None,None,True)

def testarchiveiflost(newdir,archivedir, verbose, del_ifok=False):
    gprint("Check [<>] in [<>], verbose[<>], del_ifok[<>]\n\n", newdir, archivedir, verbose, del_ifok)
    
    print BLUE+BWHITE+"Indexing archive dir.."
    verboselist=[]
    
    archivedict=defaultdict(list)
    for fn in gpylib.misc.walkfiles(archivedir, _WALK_CONDITION, True):
        archivedict[os.stat(fn).st_size].append( [fn,None] )
    
    print BLUE+"\nChecking..."
    lostcount, removecount=0,0
    
    for fn in gpylib.misc.walkfiles(newdir, _WALK_CONDITION, True,pre="\n"):
        size=os.stat(fn).st_size
        fnmd5s = archivedict.get(size,None)
        if fnmd5s is None:
            gprint("<>\n\t<>\n",RED+"Lost:",fn)
            lostcount +=1
            continue
        
        md5=gpylib.misc.getmd5(fn)
        for fnmd5 in fnmd5s:
            if fnmd5[1] is None:
                fnmd5[1]=gpylib.misc.getmd5(fnmd5[0])
            
            if fnmd5[1] == md5:
                if verbose == '1':
                    gprint("\n<>\n\t<>\n", fn, fnmd5[0])
                elif verbose != "0" and verbose is not False:
                    verboselist.append( (fn,fnmd5[0]) )
                
                if del_ifok == "del_ifok":
                    os.chmod(fn, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
                    os.remove( fn )
                    gprint(RED+"D")
                    removecount +=1
                break
        else:
            gprint("<>\n\t<>\n",RED+"Lost:",fn)
            lostcount +=1
    
    gprint("\nCheck ended.\n\t[<>] files lost.\n\t[<>]files deleted.", 
            YELLOW+str(lostcount), RED+str(removecount))
            
    if len(verboselist)!=0:
        with open(verbose,"w") as f:
            f.writelines("\n{}\n\t{}\n".format(*a) for a in verboselist)

def testarchiveiflostcurrentdir(archivedir, verbose=False, del_ifok=False):
    '''[t jcbk "I:\PicArchive"]'''
    testarchiveiflost(os.getcwdu(), archivedir, verbose, del_ifok)
        
if __RUN_CURRENT_FILE__:
    pass
    #testarchiveiflost(ur"E:\Test\2004.1000 Yunnan\4.虎跳峡", ur"E:\PicArchive1")

