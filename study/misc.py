# -*- coding: gb2312 -*-

import re, dis,copy,inspect,random,datetime,shutil,os
import colorama

"""George's sample code when studing.
    
testtry
    测试try/except/finally

testwith
    测试 with

teststrformat
    测试字符串的格式化
    
testunpackargs
    测试函数参数的解包

testdefaultval
    测试缺省参数的初始化问题

testforelse
    测试for/else

testlistdel
    测试list的删除'del'
    
testlist1
testlist2
    测试list的一些用法
testjoindictzipget
    测试这些函数
    
testarghz    
测试命令行参数的编码
    
"""

GREEN=colorama.Fore.GREEN+colorama.Style.BRIGHT
RED=colorama.Fore.RED+colorama.Style.BRIGHT

if __name__ == '__main__':
    colorama.init(autoreset=True)

def testshutil():
    os.mkdir(ur"c:\Temp\test")
    
if __name__ == '__main__':
	pass
    #testshutil()
    
def testfind():
    abc=ur"""E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\9.26~9.28泸沽湖-扎西聊吧
    E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\9.26去泸沽湖的路上-仙境-云海
    E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\9.26进入泸沽湖
    E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\9.26，9.28小凉山
    E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\9.27泸沽湖-去尼塞的路上
    E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\9.27泸沽湖-杨二车那姆家
    E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\9.27泸沽湖-泛舟，鸟岛
    E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\9.28泸沽湖的清晨
    E:\Temp\071108\2004.1000 Yunnan\1.泸沽湖\泸沽湖-小落水
    E:\Temp\071108\2004.1000 Yunnan\10.5白水河
    E:\Temp\071108\2004.1000 Yunnan\2.香格里拉\9.29去中甸的路上
    E:\Temp\071108\2004.1000 Yunnan\2.香格里拉\9.29小中甸
    E:\Temp\071108\2004.1000 Yunnan\2.香格里拉\9.29香格里拉-松赞林寺
    E:\Temp\071108\2004.1000 Yunnan\3.梅里\10.1去梅里的路上
    E:\Temp\071108\2004.1000 Yunnan\3.梅里\10.1白茫雪山
    E:\Temp\071108\2004.1000 Yunnan\3.梅里\10.1金沙江大拐弯
    E:\Temp\071108\2004.1000 Yunnan\4.虎跳峡\10.3~5虎跳峡
    E:\Temp\071108\2004.1000 Yunnan\4.虎跳峡\10.4~10.5虎跳峡-TINA'S
    E:\Temp\071108\2004.1000 Yunnan\4.虎跳峡\10.4虎跳峡-中峡探险
    E:\Temp\071108\2004.1000 Yunnan\5.丽江\10.5~6丽江
    E:\Temp\071108\2004.1000 Yunnan\5.丽江\9.28丽江过中秋
    E:\Temp\071108\2004.1000 Yunnan\5.丽江\9.28回丽江过中秋去
    E:\Temp\071108\2005.1000 龙六装修水路线路
    E:\Temp\071108\2006.0400 London-Pace
    E:\Temp\071108\2007.0128 曹辉手机欠费
    E:\Temp\081109\2003.0100 Euro
    E:\Temp\081109\2003.0900 Maldives\100OLYMP
    E:\Temp\081109\2003.0900 Maldives\Morning
    E:\Temp\081109\2003.1000 Urumqi\人物写真
    E:\Temp\081109\2003.1000 Urumqi\喀纳斯
    E:\Temp\081109\2003.1000 Urumqi\布尔津市郊
    E:\Temp\081109\2003.1000 Urumqi\荒野
    E:\Temp\081109\2003.1000 Urumqi\边疆河谷
    E:\Temp\081109\2003.1000 Urumqi\魔鬼城
    E:\Temp\081109\2004.0100 HZ
    E:\Temp\081109\2004.0100 HZ Marriage
    E:\Temp\081109\2004.0300 SUDAN Delia
    E:\Temp\081109\2004.0400 WuTai
    E:\Temp\081109\2004.0501 NB
    E:\Temp\081109\2004.1226 同学聚会
    E:\Temp\081109\2005.0800 葫芦岛 长城
    E:\Temp\081109\2007.0715 Baby
    E:\Temp\081109\2007.0818 Baby
    E:\Temp\081109\2007.0819 Baby
    E:\Temp\090314\2008-04XX杭州三亚
    E:\Temp\090314\2008-0611
    E:\Temp\090314\2008-0714
    E:\Temp\090314\2008-08XX 张家界
    E:\Temp\090314\2008-0900 Olympics
    E:\Temp\090314\2008.06XX
    E:\Temp\090314\2008.6.XX 桂林\100OLYMP
    E:\Temp\090314\2008_0814
    E:\Temp\090314\2009-0127
    E:\Temp\090314\2009-0129 Sister
    E:\Temp\090314\2009-0203 Sister
    E:\Temp\090314\2009.3.5 Snow
    E:\Temp\090314\Delia_X\郑灿
    E:\Temp\091102\2009.04XX USA
    E:\Temp\101107\2008.8XX 张家界候补
    E:\Temp\101107\2010-10-07 Olympus
    E:\Temp\101107\2007-XXXX 梅花\image012.JPG
    """
    
    def guessdate(fn):
        years1 = re.findall(ur'[^\d](\d{4})[_\-\.]',fn, re.U)  
        years2 = re.findall(ur'[^\d](\d\d)\d{4}[_\-\./\\]',fn, re.U)  
        y = years1[-1] if years1 else ("20"+years2[-1] if years2 else None )
        
        md1 = re.findall(ur'[^\d]\d{4}[_\-\.](\d{1,2})[_\-\.]{0,1}(\d{0,2})',fn, re.U) #2003.1000 2009-0129
        md2 = re.findall(ur'[^\d]\d\d(\d\d)(\d\d)[_\-\./\\]',fn, re.U) #091102
        md3 = re.findall(ur'[^\d](\d{1,2})\.(\d{1,2})[^\d]',fn,re.U) #\10.1
        (m,d)=md3[0] if md3 else (md1[-1] if md1 else ( md2[-1] if md2 else (None,None)))
        
        return int(y if y else 0),int(m if m else 0),int(d if d else 0)
        
    for fn in abc.split("\n"):
        print fn
        (y,m,d) = guessdate(fn)
        print y, m, d
        
#testfind()
   
def testhash(fn):
    import hashlib
    h = hashlib.new('md5')
    with open(fn,'rb') as f:
        h.update(f.read())
    return h.hexdigest()
    
#print testhash(ur"C:\1.JPG")
#print testhash(ur"C:\2.JPG")
    
def testos(rootDir):
    import os 
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs: 
        for d in dirs: 
            print os.path.join(root, d)     
        for f in files: 
            print os.path.join(root, f)     

#testos("c:/George/Tools")
            
def testexif(fn):
    from PIL import Image
    from PIL.ExifTags import TAGS
    
    def get_exif():
        ret = {}
        i = Image.open(fn)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
            #print value
        return ret
    print "\n".join(['{}\n\t{}'.format(a,repr(b)) for a,b in get_exif().iteritems()])
    
#testexif("c:\George\julie\照片打印\Img_3199.jpg")    
#testexif("c:\George\julie\照片打印\Dsc00330.jpg")    
#   testexif("c:\George\julie\照片打印\P5270039.jpg")    
#testexif(r"c:\Temp\1.泸沽湖\9.26~9.28泸沽湖-扎西聊吧\100_1459.jpg")
#testexif(r'c:\temp\美丽的泸沽湖－里格半岛.jpg')
#testexif(r'c:\temp\1.jpg')

def testexifread(fn):
    #http://tilloy.net/dev/pyexiv2/tutorial.html
    import pyexiv2
    metadata = pyexiv2.ImageMetadata(fn)
    metadata.read()
    print "\n".join(metadata.exif_keys)
    
    print "\n".join(['{}\n\t{}'.format(a,b) for a,b in metadata.iteritems()])
#testexifread(r"E:\Except\2BB\sony-hz\DSC02780.JPG")     
#testexifread("c:\George\julie\照片打印\Img_3199.jpg")    
#testexifread("c:\George\julie\照片打印\Dsc00330.jpg")    
#testexifread("c:\George\julie\照片打印\P5270039.jpg")
#testexifread(ur"c:\Temp\美丽的泸沽湖－里格半岛.jpg") 
#testexifread(ur"E:\Temp\090314\2007-1224.Julia.艺术\1688册白雪公主册入32张DSC_8525.jpg")
#testexifread(ur"I:\Except\HD_Video\AVCHD\BDMV\STREAM\2012_0118-00114.MTS")



def testexifwrite(fn):
    import pyexiv2
    metadata = pyexiv2.ImageMetadata(fn)
    metadata.read()
    print "\n".join(metadata.exif_keys)
    metadata['Exif.Image.DateTime']=datetime.datetime.today()
    metadata.write()

#testexifwrite(r'c:\temp\2.jpg')
#testexifwrite(r'c:\temp\2.jpg')

def testexifhachoir(filename):
    from hachoir_core.error import HachoirError
    from hachoir_core.cmd_line import unicodeFilename
    from hachoir_parser import createParser
    from hachoir_core.tools import makePrintable
    from hachoir_metadata import extractMetadata
    from hachoir_core.i18n import getTerminalCharset
    from sys import argv, stderr, exit

    filename, realname = unicodeFilename(filename), filename
    parser = createParser(filename, realname)
    if not parser:
        print >>stderr, "Unable to parse file"
        exit(1)
    try:
        metadata = extractMetadata(parser)
    except HachoirError, err:
        print "Metadata extraction error: %s" % unicode(err)
        metadata = None
    if not metadata:
        print "Unable to extract metadata"
        exit(1)

    text = metadata.exportPlaintext()
    charset = getTerminalCharset()
    for line in text:
        print makePrintable(line, charset)

#testexifhachoir(r"I:\Except\HD_Video\AVCHD\BDMV\STREAM\2012_0118-00114.MTS")
#testexifhachoir(r"I:\pics\090314\2007-1224.Julia.艺术\1688册白雪公主册入32张DSC_8525.jpg")
def testextractor(fn):
    import extractor
    xtract = extractor.Extractor()
    
    keys = xtract.extract(fn)
    for keyword_type, keyword in keys:
        print "%s - %s" % (keyword_type.encode('iso-8859-1'), keyword.encode('iso-8859-1'))

#testextractor(ur"I:\Except\HD_Video\AVCHD\BDMV\STREAM\2012_0118-00114.MTS")
#testextractor(ur"I:\pics\090314\2007-1224.Julia.艺术\1688册白雪公主册入32张DSC_8525.jpg")
testextractor(ur"I:\1.mpg")
#comment for testinspect
def testinspect():
    import inspect
    
    print GREEN+"[Position1] inspect.getcomments\n", inspect.getcomments(testinspect)
    print GREEN+"\n[Position2] inspect.getsource\n", inspect.getsource(testinspect) 
    lines,no = inspect.getsourcelines(testinspect)
    
    print GREEN+"\n[Position3] inspect.getsourcelines\n",  no
    for l in lines:
        print l,

    print GREEN+"\n[Position4] getargvalues/formatargvalues\n",  no
    def f0(a,b,c,*args,**kws):
        args, varargs, keywords, locals = inspect.getargvalues(inspect.currentframe())
        print inspect.formatargvalues(args, varargs, keywords, locals)
        
    f0(1,2,3,'a','b','c', x=10,y=20,z=30)
    
    print GREEN+"\n[Position5] inspect.stack()\n",  no
    def f1():
        def f2():
            def f3():
                print "\n\n".join([ "%d:\n"%-i + "\n".join(["\t"+str(item) for item in s]) for i,s in enumerate(inspect.stack()) ])
            f3()
        f2()
    f1()
    
    print GREEN+"\n[Position6] inspect.currentframe()\n",  no
    ff=inspect.currentframe()
    print dir(ff)
    for x in ff.f_locals:
        print x
    
#testinspect()

def testtry():
    def testtry1():
        def divide(x, y):
            try:
                result = x / y
            except ZeroDivisionError:
                print "division by zero!"
            else:
                print "result is", result
            finally:
                 print "executing finally clause"

        divide(2, 1)
        divide(2, 0)
        divide("2", "1")
        #系统打印出来的错误，是在finally之后。

    try:
        testtry1()
    except Exception as e:
        print type(e)
        print e.args

#testtry()


def testwith():
    from contextlib import contextmanager
    from timeit import default_timer
    from time import sleep
    
    @contextmanager
    def gtime(s0,s1):
        t0 = default_timer()
        if s0 is not None:
            print s0,
        yield
        
        print s1.format(default_timer()-t0)
            
    with gtime("Starting working 1 ","{:.2f} seconds used.\n"):
        sleep(0.3)
       
    with gtime("Starting working 2 ","{:.2f} seconds used.\n"):
        sleep(0.1)

#testwith()
       

def teststrformat():
    import math
    for x in range(1,11):
        print '{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x)
    
    print '12'.zfill(5)
    print '-3.14'.zfill(7)
    
    print '{0} and {1}'.format('spam', 'eggs')
    print 'This {food} is {adjective}.'.format(
                        food='spam', adjective='absolutely horrible')
    print 'The story of {0}, {1}, and {other}.'.format(
                        'Bill', 'Manfred',other='Georg')
    
    print 'The value of PI is approximately {!r}.'.format(math.pi)
    print 'The value of PI is approximately {0:.3f}.'.format(math.pi)
    
    table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
    for name, phone in table.items():
        print '{0:10} ==> {1:10d}'.format(name, phone)

    table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
    print ('Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; '
           'Dcab: {0[Dcab]:d}'.format(table))
    print 'Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table)
    
    for n,v in vars().iteritems():
        print n,v
    
#teststrformat()    
    


def testunpackargs():
    def f(a, b, c):
        print a, b, c
    
    a=(1, 2, 3)
    f(*a)
    a=[5, 6]
    f(4, *a)
    
    a={"a": 1, "b": 2, "c": 3}
    f(**a)
    
    x={"b": 2, "c": 3}
    f(1, **x)
    f(a=1, **x)

#testunpackargs()

def testdefaultval():
    def f(a, L=[]):
        L.append(a)
        return L
        #L只初始化一次

    print f(1)
    print f(2)
    print f(3)

#testdefaultval()

def testforelse():
    print
    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print n, 'equals', x, '*', n/x
                break
        else:
            # loop fell through without finding a factor
            #a loop’s else clause runs when no break occurs
            # try's else run when no exception
            print n, 'is a prime number'

#testforelse()

def testlistdel():
    """详细可以看 Python Standard Library 5.6.4. Mutable Sequence Types """
    a = [-1, 1, 66.25, 333, 333, 1234.5]
    print a
    del a[0]
    print a
    del a[2:4]
    print a
    del a[:]
    print a
    del a
    print a
    #a已经被删除，所以此语句会报错

#testlistdel()    
    
def testlist2():
    vec = [[1,2,3], [4,5,6], [7,8,9]]
    
    print [n for e in vec for n in e]
    #[1, 2, 3, 4, 5, 6, 7, 8, 9]
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    
    def print_matrix(m):
        print
        for l in m:
            print l
            
    print_matrix( [[row[i] for row in matrix] for i in range(4)] )
    
    print_matrix( zip(*matrix) )

#testlist2()
    
    

def testlist1():
    A = ['spam', 'eggs', 100, 1234]
    
    #不能用 a=A, 这样的话，实际上就是一个东东了。
    a = A[:]
    a[0:2] = [1, 12]
    print A
    print a
    
    a = A[:]
    a[0:2] = []
    print
    print A
    print a
    
    a = A[:]
    a[1:1] = ['bletch', 'xyzzy']
    print
    print A
    print a
    
    a = A[:]
    a[:0] = a
    print
    print A
    print a
    
    a = A[:]
    a[:] = []
    print
    print A
    print a

#testlist1()

def testjoindictzipget():
#作用：将s中的某些字符变换为某些字符
    a = ['1', '2', '3', '4']
    b = ['5', '6', '7', '8']
    s = '1234'

    print ''.join(dict(zip(a, b)).get(c, c) for c in s)
    print ''.join(dict(zip(a, b)).get(c, c) for c in "12345678abcdefg")

testjoindictzipget()

def testarghz():
    def safeunicode(t):
        #print repr(t)
        try:
            u=unicode(t)
            #对unicode调用此函数，返回值等于输入
        except UnicodeDecodeError:
            try:
                u=unicode(t, "gb2312")
            except UnicodeDecodeError:
                u=unicode(t, "utf-8")
        return u
    
    import sys
    print u"测试命令行参数"
    #print repr('我')
    for i,j in enumerate(sys.argv):
        #print u"[%d] = %s" % (i,unicode(sys.argv[i], "gb2312"))
        print u"[{}] = {}".format(i, safeunicode(sys.argv[i]))
        #因为命令行传递的东东编码方式不定
    
#testarghz()

    
