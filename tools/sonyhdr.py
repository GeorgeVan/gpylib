# coding=gb2312

'''
�������ܣ�
    ��������Ƭ�ļ�������EXIF�������������Ҫ��Ϣ��������ӡ��ͺź��������ڡ��˱���ϵͳ��Ҫ��
    ������Ƭ��ʱ�䣬�������Ƭ�ļ���С��MD5��������Ƭ������ġ���Ƭ��ʱ����Ϣ���ܹ������ǳ�Ҫ
    ����������û�����ڵģ��û����Բ��� metadata�ļ�����ϸ���Կ�_getinfo���롣
    ��Ƶ�ļ�û��EXIF����ȫ�����ļ��޸����ڻ���metadata���ơ�
    ����˵������Ƭ��������ͬ�ġ�
    
��һ����ʹ�� tj 0��ͳ��һ�´�����Ŀ¼����Ƭ���������ͳ�Ƴ�����һЩ��Ϣ��
    1��"No Exif"���ļ���û��Exif����Щ��Ҫ��һЩ�������Դ����Ƭ�����Ǿ����༭�����Ƭ��
    2��"No MMDT"����Exif����������û��Datetime��û��Make/Model����������ȽϺ�����
    3��"No MM": EXIF��û��Make/Model��������Datetime����Ƭ����Photoshop�ȱ༭�������ˡ�
    4��"Zero DT": EXIF�е�DateTimeΪȫ�㣨olympusĳ�����û������ʱ��ͻ�����ˣ�
    5��"MM No DateTime"����Make/Model������û��DateTime��������
    6��"DateTime"����ͳ����ʱ�����Ƭ�������շֲ������
    7��"Make Models"����Ƭ����������ͺŷֲ������
    8��"No MM Paths"�� "No MM"������Ƭ��·���б�
    9��"Zero DT Paths"��"Zero DT"��Ƭ��·���б�
    A��Funny�ļ�: size,datetime��ͬ������MD5��ͬ
    B���ظ��ļ�: size,MD5��ͬ������DateTime��ͬ
    C��ͬһ���ļ���size,md5,DateTime����ͬ�����

    ���1��2��4��5���봦�������޷���Щ��Ƭ�޷������ݡ�
    ʵ���л������Щ��Ƭ��ʱ�����Բ��ԣ��²���ĳЩ���û������ʱ��󣬻�ӳ���ʱ�俪ʼ��
    ͨ����DateTime�б�Ϳ��Կ�����Щ�����
    ���B��C�����ֹ�ɾ�������ļ�������������������B���ļ��ᱻ���౸�ݡ����Cֻ�ᱸ��һ����
    
    �����Ƭ�ļ���.adjust��.datetime�����ļ����ǹ鵵ͳһ���͵ģ���ͳ���л�ʹ����Щ��Ϣ��
    ���ԶԹ鵵����ļ��н���ͳ�ƣ������Ƿ����ظ����������ϸ���Կ�_getinfo������
    
�ڶ�����[sc 0/1] ����Ƭ���ڵ��˹����������Զ���ȫ�Զ����� 
    ��� 'noexif', 'nodt', 'outdt', 'zeordts', 'errordt'���������������
    ȫ�Զ��������������Щ�ļ����ļ�����Ŀ¼�����з������²�����ڣ�����ͬ���ڵģ����ղ����̶�
    ����ȥ���ò�ͬ��ʱ���롣���Ҫʹ��������ܣ�����Ҫ�������߲������ڵ��ļ���Ŀ¼�����޸�Ϊ
    YYYY-MM-DD����ʽ���ɡ�
    ���Զ�����������²ⲻ�����ڣ������ݴ����BASE�����ղ���ȥ���ò�ͬ��ʱ���롣
    �˹���������������Meta�ļ���׺Ϊ .dtadjust��
    �Զ�����Զ���������������meta�ļ���׺Ϊ.datetime
    ��Ϊ�˹���������Ƚ������˱����ֹ�ɾ���ſ��ԡ���datatime�ļ��ᱻ���򸲸ǡ�
   
    ����������ʱ����У��MD5����֤��ͬ�ļ�����ڶ��Ŀ¼�����еĻ���������ͬһ��MD5
    sc 0/1ֻ֧��ȫ�Զ���������֧����ֹ���ڼ�顣'noexif':True,'zeordts':True,'outdt':True
    0��1��������������ж���Ƭ��  noexif/zerodts����ϸ���Կ� _DateTimeGen ������
    
��������[jc 0/1] ����Ƭ���ڽ��м�顣
    datetime.datetime(1900,1,1), datetime.datetime(2100,1,1)
    ����ͳ�Ƴ�'noexif', 'nodt', 'outdt', 'zeordts', 'errordt'�ĸ��������
    �����ڲ��Ե���������ӡ���²�����ڡ�
    ����������ȷ�ģ�Ҳ���ӡ���²�����ڡ�
    ����������һ������

���Ĳ���[sm] Ԥ����Ƭ˵��
    �ڹ鵵��ÿ����Ƭ��������һ��˵�����֡���Щ����Ҳ���ڱ��ݵ�ʱ����ļ�����Ŀ¼���в²�����ġ�
    ��ϸ���Կ�_genname������
    ���ϣ���鵵����ļ���ֻ�Ƕ����֣�������ڹ鵵ǰ�޸�Ŀ¼���ơ�������������������Ƶģ�����Ҫ��
    ���Ƶ�ǰ�档��yyyy-mm-dd ɶ

���岽��[bk] ����ǰĿ¼���ݵ�archiveĿ¼��
    1) ���������ļ������ļ�����֤�������ظ��ĵ����������ʹ��Size+MD5�ķ�ʽ��
       ������ļ������ظ��ģ��ᱸ���ĸ�����ȫ������ģ����ǻ�ѡ������Ǹ�note��
    2) Ŀ¼���ļ�����ʱ�����������飬ÿ������ļ�������200����
    3) �����ļ����Զ�ѡ����ʵ�Ŀ¼��
    4��ÿ��Ŀ¼�����ƶ�����С���Ǹ��ļ���ʱ�䡣
    
��������[jcbk] ����Ƿ��Ѿ�ȫ������
    ʹ��MD5У�飬���Ի�Ƚ�����

���߲���[jca] ��鱸��Ŀ¼�Ƿ���ʱ�����


���������Ƶ�����Ƚϼ򵥡���Ϊ��Ƶ�ļ�û��EXIF��ֻ�ܸ����޸����ڡ�
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
'''��һ���֣����ߺ��� *******************************************'''   

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
    '''����ǹ淶����ļ������򷵻�(DateTime,note,size)'''
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
             u'2004-09-26_000001(Yunnan ����� �����İ�)_B50F9.jpg',
             u'2004-09-26_000001(Yunnan ����� �����İ�).jpg',
             u'2004-09-26_000001(Yunnan ����� �����İ�)_B50F9.mov',
             u'2004-04-03_192941_12DD1D.jpg',
             u'2004-04-03_192941-7.jpg',
            ur'2004-09-27_010027(Yunnan ����� ȥ������·�� ����������� ���뵺).jpg',]
        for f in fns:
            print u"{}, {}, {}".format(*_trygeninfofromname(f))
             
    #_testgetinfofromname()

def _getarchiveinfodtonly(fn):
    '''���ټ��ع鵵�ļ�'''
    (dt,note,size) = _trygeninfofromname(fn)
    if dt is not None:
        tags={}
        tags["DateTime"] = dt
        return tags,note if note else ""
    else:
        return None,None
        
def _getinfo(fn,allowmeta=False,shortmakemodel=True, forceraw=False):
    '''������ļ��ڲ���EXIF���ļ������ļ���.dtadjust �ļ���.datetime �ļ��޸����ںͲ���
    ������Ϣ��
    
    ���fn����û��exif���򷵻�None
    �����make/model����򻯺�����ֵ�
    �����datetime����ֶΣ�������ֵ�
    ���forceraw����ֻ��ԭʼ�ļ��ж�ȡ����ʱallowmetaʵ���ϲ���������
    forceraw�����ϲ��ã��������ڵ���Ŀ��
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
        #ȥ��make��useless������easyname
        m = make if make else ''
        return '-'.join( [(easyname.get(w.lower(),None) or w) for w in longmodel.split() \
                                if (useless.lower().find(w.lower())==-1 \
                                    and m.lower()!=w.lower())] )
    
    tags={}
    exif=None
    if os.path.splitext(fn)[1].lower() == ".jpg":
        #����MOV��MTS���ļ�û��Exif
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
                tags['Model'] = model.replace(",","-") #�е��ͺ�������,
        except Exception: pass
        
        dt = exif.get("Exif.Photo.DateTimeOriginal",None) or \
             exif.get("Exif.Image.DateTime",None) or \
             exif.get("Exif.Photo.DateTimeDigitized",None)
        #��Щ��Ƭ��ǰ������ͬ���ڶ������Բ��ԡ�
        if dt is not None:                   
            tags["DateTime"]= dt.raw_value
        
        if (not tags) and (not forceraw):
            tags["DateTime"]=time.strftime("%Y:%m:%d %H:%M:%S",time.localtime(os.stat(fn).st_mtime))
        #��ЩIPHONE�������Ƭ����EXIF������û��Model/Make/DateTime�������ǵ��빤�ߵ����⡣
        #��Щ����ͨ���ļ��޸��������Ʋ����Ŀǰֻ��IPHONE��Ƭ��������⡣��Щ������Ӧ�ô���IPHONE�ġ�
        
    if not forceraw:
        #����ǹ�������ļ�������ʹ���ļ����е�����
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
        #�ֹ������ģ��������������أ������˹��ı����ֹ�ɾ��
        try:
            with open(fn[:-3]+"dtadjust","r") as f:
                tags["DateTime"]=f.readline()
        except Exception:
            pass
        
    return tags if (len(tags)>0 or exif) else None

    
def _trygetnote(fn,root,pcache=False, cache={}):
    '''�����ļ�������Ŀ¼ȥ�����ļ�Note'''
    if pcache: #ֻ��������ӡ�ֵ��
        #����չ�ֵ���ȱʡ����ֻ����һ�ε�Python����
        print len(cache)
        print u"\n".join([u"{}:{}".format(k,v) for (k,v) in cache.iteritems()])
        return None
        
    (dt,note,size)=_trygeninfofromname(fn)
    if root is None:
        return note if note else ""
        
    if note:
        #����ǹ淶��ģ���ȡnote���ã�ֻ����·��
        fn=os.path.split(fn)[0]
        note=note[1:-1] #ɾ��ǰ����������Ϊ����Ҫ���
    
    def removeall(n, usecache):
        replacefns=((ur"[_����&\-\.\[\]]+"," "),(ur'([^a-z])[a-z]([^a-z])',ur'\1\2'), )
        uselessfns=('CIMG','IMG','IMAG','DSC[ \da-z]{5,}',
                    '^P[a-z]*[ \d]{5,}','^A[ \d]{5,}','^S[ \d]{5,}','^L[ \d]{5,}',
                    ur"�½��ļ���",ur'ͼ��',ur'Сͼ',ur'����',ur'����',ur'����',ur'��ת',ur'pic',
                    ur'image',ur'mov',ur'δ����',ur'��Ƭ',
                    ur'����',ur'Olympus',ur'Olyms',ur'iphone',ur'AVSEQ',ur"vts",ur"msdcf",
                    ur'ip4.g',ur'sony hz',ur'2bb',ur'OLYMP','Delia X',ur"DCIM",ur'XX',ur'New Folder',
                    ur'PRIVATE',ur'AVCHD', ur'BDMV', ur'STREAM',
                    ur'\d��',ur'\d��',ur'\d��',
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
        #ֻ�ж�·������cache����ȥ�ң��ļ�������Ҫ
        
    names=[n for (i,n) in enumerate(names) \
            if len(n)>0 and (i==len(names) or (not (any(son.find(n)!=-1 for son in names[i+1:])))) ]
    #���ǰ���Ŀ¼���ں�����ֹ�������ȥ��
    
    return u'({})'.format(u' '.join(names)) if names else u""
    #��������

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
    #print _trygetnote(ur'C:\Temp\2004.1000 Yunnan\5.����\9.28����������\DSC100_1635.jpg', ur'C:\Temp')
    #print _trygetnote(ur'C:\Temp\2004.1000 Yunnan\1.�����\9.26~9.28�����-�����İ�\100_1635.jpg', ur'C:\Temp')
    #print _trygetnote(ur'C:\Temp\2004.1000 Yunnan\5.����\9.28����������\2004-09-26_000001(Yunnan ����� �����İ�)_B50F9.jpg', ur'C:\Temp')
    
def _genname(fn, exifs=None, allowmeta=False, shortmakemodel=True, root=None, size=0, note=None, id=None):
    '''�淶����: size=0��ζ��Ҫ������ȥȡ�ļ���С��size=None��ζ�Ų���Ҫ����ֶ�,size>0�����ô�size'''
    exifs=exifs or _getinfo(fn, allowmeta, shortmakemodel)
    
    try:
        return u"{}{}{}{}{}".format(
              time.strftime("%Y-%m-%d_%H%M%S", time.strptime(exifs['DateTime'], "%Y:%m:%d %H:%M:%S")),
              note if note else _trygetnote(fn,root),
              "" if size is None else "_{:X}".format(size if size>0 else os.stat(fn).st_size),
              "" if id is None else "-{:X}".format(id),
              os.path.splitext(fn)[1]
              )  
    except Exception as e: #exifΪNone������DateTime����û��DateTime���Ϸ�
        return None
        
def _gennamelong(fn, exifs=None, allowmeta=False, shortmakemodel=True, root=None, size=0):
    #�˺���û������
    exifs=exifs or _getinfo(fn, allowmeta, shortmakemodel)
    
    try:
        return u"{}{}{}{}{}{}".format(
              time.strftime("%Y-%m-%d_%H%M%S", time.strptime(exifs['DateTime'], "%Y:%m:%d %H:%M:%S")),
              _trygetnote(fn,root) if root else "",
              "_"+exifs['Make'] if exifs.get('Make', None) else "",
              "-"+exifs['Model'] if exifs.get('Model',None) else "",
              "_{:X}".format(size if size else os.stat(fn).st_size) if size>=0 else "",
              os.path.splitext(fn)[1])  
    except Exception as e: #exifΪNone������DateTime����û��DateTime���Ϸ�
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
    #print _genname(ur"C:\Temp\2004.1000 Yunnan\4.����Ͽ\10.4����Ͽ-��Ͽ̽��\IMG_1780.JPG",True,True,True,'����')



'''**************************************************************'''
'''�ڶ����֣�ͳ��************************************************'''
        
class _PicCensus(object):
    def __init__(self, allowmeta=False):
        self.noexifs, self.mmnodts, self.nomms, self.nommdts, self.zeordts = [], [], [], [], []
        self.models, self.ymds=collections.defaultdict(int),collections.defaultdict(int)
        self.count, self.allowmeta = 0, allowmeta
        self.sizes = collections.defaultdict(list)
        
    def add(self,fn): #fn��unicode����Ϊ��ЩĿ¼�������ļ��������unicode�����
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
        
        #��ͬsize����ͬMD5 ����Datatime��ͬ�ģ��������ݺ���ظ���
        #��ͬsize����ͬDatetime����ͬMD5�ģ������Ƚ�Funny
        #��������ͬ�ģ����ڱ��ݵ�ʱ����Ȼֻ��ѡ��һ��
        
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
                #Funny: size,datetime��ͬ������MD5��ͬ
                gprint("\n<> [<>] [<>]\n",BLUE+"Funny",size, dt)
                gpylib.misc.ppdict(md5s,u"    [",u"]", u"        ",u"")
                #���item�� key/list
                
            for (md5, dts) in THOSE_VALUE_MORE_THAN_ONE( md5_dts): 
                #�ظ�: size,MD5��ͬ������DateTime��ͬ
                gprint("\n<> [<>] [<>]\n",YELLOW+"Duplicate",size, md5)
                gpylib.misc.ppdict(dts,u"    [",u"]", u"        ",u"")
            
            for ((dt,md5),fns) in THOSE_VALUE_MORE_THAN_ONE( dtmd5_fns):
                #��size,md5,DateTime����ͬ�����
                gprint("\n<> [<>] [<>] [<>]\n    ", GREEN+"Same File", size, dt, md5)
                print u"\n    ".join(fns)
               
def countthisdir(dir,allowmeta):
    print "Allow Meta [{}]".format(allowmeta)
    with gpylib.misc.gt("��ʼͳ��...\n", "{:.1f}��\n"):
        pa = _PicCensus(allowmeta)
        pa.adddir(dir)
        pa.printme()

def countcurrentdir(allowmeta):
    countthisdir(os.getcwdu(),allowmeta)
    #����ʹ��unicode����Ϊ��ЩĿ¼�������ļ�����Unicode�ģ�������ã���os.walk�в�����

if __RUN_CURRENT_FILE__: 
    pass
    #countthisdir(ur"C:\Temp\2004.1000 Yunnan",True)
    #countthisdir(ur"E:\Temp\091102\2008-11-25",False)
    #countthisdir(ur"C:\Temp\1.�����")

    
'''**************************************************************'''
'''�������֣���������********************************************'''

def _guessdate(fnn):
    fn = fnn if os.path.isdir(fnn) else os.path.split(fnn)[0]
    
    years1 = re.findall(ur'[/\\](\d{4})[_\-\.]',fn, re.U)  
    #Ŀ¼�����ĸ����ֿ�ʼ�����������. _ -�ģ��ҳ�����������
    years2 = re.findall(ur'[/\\](\d\d)\d{4}[_\-\./\\]',fn, re.U)
    #Ŀ¼�����������ֿ�ʼ���������. _ - / \��Ҳ�����һ��
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
                #����һ�¶���
                
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
    #�ֵ䱣֤�����Ҫ����ʱ����ļ����������ʱ���ܹ�����ͬһ������
    #����ͻ�����������ڣ�������ɱ��������ˡ�
    def __init__(self,base,skip, step):
        self.base, self.skip, self.step, self.i=base, skip, step, skip
        self.guessymds = {}
        
        
    def __call__(self,fn):
        print fn
        md5 = gpylib.misc.getmd5(fn)
        if _DateTimeGen.history[md5] == '':
            #����û�в²��ʱ��
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
            #�²������ʱ��None��Ҳ����
            result = _DateTimeGen.history[md5]
            print BLUE+"Duplicated file"
         
        print GREEN+result if result else RED+"NONE"
        return result

def checkthisdir(dir,dt1,dt2,allmeta,gen,option,manual=False):
    print "Allow Meta", allmeta
    with gpylib.misc.gt("��ʼ�������...\n", "{:.1f}��\n"):
        _PicDateTimeCheck(dir, dt1,dt2,allmeta,gen,option,manual).printme()

def gendtcurrentdir(allowmeta):
    checkthisdir(os.getcwdu(),
                datetime.datetime(1900,1,1), datetime.datetime(2100,1,1),
                allowmeta,
                _DateTimeGen(None,3601, 2), #�ӵڶ���Сʱ��ʼ������ֻ������
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
    #���ɸ���ʱ��� {'noexif':True, 'nodt':True, 'outdt':True, 'zeordts':True, 'errordt':True}
    #ÿ��ʹ��֮ǰ�������ֹ�ɾ��Ŀ¼�µ� dtadjust �ļ���
        checkthisdir(ur"E:\Temp\071108\2004.1000 Yunnan",
                datetime.datetime(2004,9,1), datetime.datetime(2004,11,1),
                False,
                _DateTimeGen(datetime.datetime(2004,9,25),0,2), #ż��
                {'outdt':True},True) #����ֻ��������ʱ�䷶Χ�ģ��������˹�����
    elif a==2:
    #���ʱ���
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
'''���Ĳ��֣��鵵************************************************'''
    
class _PicFile(object):
    totalsize=0
    totalfile=0
    totalmd5=0
    
    def __init__(self, fullname, rootdir):
        #���rootdir is none: ���Ѿ��鵵���ļ�
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
        #genname���ú��������
    
    @property
    def easyhash(self):
        path, fn = os.path.split(self.fullname)
        dir=os.path.split(path)[1]
        
        return u"{}{}{}".format(dir,fn,self.size)
        
    def genname(self,pre,idx):
        #��������������ļ�����Ӻú��ٵ��á���Ҫ����֮ǰ���Ǹ��ļ����ж��Ƿ���Ҫ��size��idx�����ļ���
        if self._newname is None:
            s= self.size if (pre is not None and pre.datetime == self.datetime and pre.size!=self.size) else None
            #���PRE�����ں͵�ǰ����ͬ�����Ǵ�С��ͬ������Ҫ�Ѵ�С�����ļ���
            i = idx if (pre is not None and pre.datetime == self.datetime and pre.size==self.size) else None
            #���PRE�͵�ǰ�����ڡ���С����ͬ������Ҫ��idx�����ļ���
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
        #path/bashpath����ȫ·���������һ�����飬��path��None
        self.path, self.basepath, self.pics, self.clean = path,basepath,pics,clean
    @staticmethod
    def mirror(path, md5dict):
        '''�ӹ鵵Ŀ¼��ȡ'''
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
        '''����һ���µ��飬pf�ǵ�һ����Ա'''
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
            #���ظ����ļ�����ΪPICArchive�����ǰ�Ѿ�����MD5�����ظ��ˣ�������ʵ���ϲ����ܷ�����
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
            #��ͬʱ����ļ����뱣����һ��Ŀ¼����
        
        if i<=0:
            return None
            #ǰһ��������ļ���ʱ�䶼��ͬ
        #i��Ӧ���ں�һ��
        
        if self.path is not None and os.path.split(self.path)[1] <= self.pics[i-1].datetime.replace(':','-'):
            #path�����ִ����ʱ�䴦�����ߣ����ӵ��Ұ��
            #��Ҫ��֤path���ִ����ʱ����Զ����path��pics����
            pg = _PicGroup(None,self.basepath,self.pics[i:],False)
            del self.pics[i:]
        else:
            #�ӵ�����
            pg = _PicGroup(None,self.basepath,self.pics[:i],False)
            del self.pics[:i]
        #gprint("\nSplited to <>:<>\n",self.count(),pg.count())
        return pg
        #Archive��������룬��˲��õ���
    
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
        #������Size��Index�ģ��˹����һ���Ƿ���ͬһʱ�̵���Ƭ��
        
    def printdebug(self, step=50):
        gprint("\nGroup [<>]\n\t", BLUE+str(len(self.pics)))
        print "\n\t".join(pf.name for pf in self.pics[::step])
        #ÿ���ٸ���Ƭ��ӡһ��
        
    def printse(self):
        gprint("\nGroup [<>]\n\t", BLUE+str(len(self.pics)))
        print "\n\t".join(pf.name for pf in [self.pics[0],self.pics[-1]])
        #ֻ��ӡͷβ

    def dumpstep2(self, fake, actions):
        '''Ҫ������������Ϊ��һ��Ҫmove�ļ������src��Ŀ¼���仯�ˣ���ô���޷��ƶ���'''
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
        if self.path is None: #��û�д�����
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
        #����MD5ȥ��
        if samefile:
            pf.exif=samefile.exif
            #���������ڶ���������������ҵ�

        if len(self.groups)==0:
            self.groups.append(_PicGroup.newone(self.path,pf))
            return
            
        for g in self.groups:
            if pf<=g:
            #���pf�ȵ�һ���黹ҪС����ô�ͼ��뵽��һ������
            #���pf���������м䣬����ӵ���һ��������
            #���pf���κ�һ���鶼Ҫ������ӵ����һ����
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
    with gpylib.misc.gt(BLUE+BWHITE+"Archiving...\n", "{:.1f}��\n"):
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
    with gpylib.misc.gt("Archive Self Check...\n", "{:.1f}��\n"):
        print "��ʼ���"
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
    #testarchiveiflost(ur"E:\Test\2004.1000 Yunnan\4.����Ͽ", ur"E:\PicArchive1")

