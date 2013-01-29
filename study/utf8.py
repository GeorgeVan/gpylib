# coding: utf-8

'''测试UTF-8编码的文件对各种情况的影响
You may see ugly chars. Try print unicode(__doc__,"utf-8")
'''

#汉 utf8 '\xe6\xb1\x89' gb2312 '\xba\xba' utf16 '\u6c49'

def print_hz_utf8():
    global h,h2u8,h2u82gb,uh,uh2u8,uh2
    #为了调试方便

    h='汉'
    print "Test1 UTF8"
    print repr(h) # '\xe6\xb1\x89'
    print len(h)  # 3
    print h #乱码

    print "\nTest2 UNICODE"
    h2u8 = h.decode('utf-8')
    print  h2u8  #返回一个unicode“汉”，所以打印成功

    print "\nTest3 gb2312"
    h2u82gb = h.decode('utf-8').encode('gb2312')
    print repr(h2u82gb) #'\xba\xba'
    print len(h2u82gb) #2
    print h2u82gb #返回一个GB2312的string，因系统窗口是GB2312的，所以可以打印成功

    uh=u'汉'
    print "\nTest4 unicode"
    print repr(uh) # u'\u6c49'
    print len(uh)  #1
    print uh

    uh2u8 = uh.encode('UTF-8')
    print "\nTest5 utf8"
    print repr(uh2u8) # '\xe6\xb1\x89'
    print len(uh2u8)    #3
    print uh2u8

    uh2 = uh2u8.decode('UTF-8')
    print "\nTest6 unicode"
    print repr(uh2) # u'\u6c49'
    print len(uh2)   #1
    print uh2
    
    print "\nTest7"
    print u"测试一下"
    print "测试一下" #如果这个能够显示正确，说明命令行输出实际上是UTF8的
    #在eric4的shell里面，支持的是UTF8，不知道如何更改为GB2312
    #在WindowsCMD里面，支持的是GB2312，不知道如何更改为UTF8
    
    print "\nTest8"
    print globals()['__doc__']
    print unicode(globals()['__doc__'],"utf-8")
    print unicode(globals()['__doc__'],"utf-8").encode("gb2312")
    

if __name__ == '__main__':
    print_hz_utf8()
    