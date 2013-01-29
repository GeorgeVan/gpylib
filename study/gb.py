# coding: gb2312

'''测试gb2312编码的文件对各种情况的影响
You may see ugly chars. Try print unicode(__doc__,"gb2312")
'''

#汉 utf8 '\xe6\xb1\x89' gb2312 '\xba\xba' utf16 '\u6c49'

def print_hz_gb():
    h = '汉'
    print "Test1"
    print repr(h) # '\xba\xba'
    print len(h)  # 2

    
    print "\nTest2"
    u = u'汉'
    print repr(u) # u'\u6c49'
    print len(u)  #1


    s = u.encode('UTF-8')
    print "\nTest3"
    print repr(s) # '\xe6\xb1\x89'
    print len(s)    #3
    
    
    u2 = s.decode('UTF-8')
    print "\nTest4"
    print repr(u2) # u'\u6c49'
    print len(u2)   #1

    print "\nTest5"
    print u"测试一下"
    print "测试一下" #如果是乱码，说明输出不支持GB2312
    #在eric4的shell里面，支持的是UTF8，不知道如何更改为GB2312
    #在WindowsCMD里面，支持的是GB2312，不知道如何更改为UTF8
    
    print "\nTest6"
    print globals()['__doc__']
    print unicode(globals()['__doc__'],"gb2312")
    print unicode(globals()['__doc__'],"gb2312").encode("utf-8")

if __name__ == '__main__':
    print_hz_gb()

    
