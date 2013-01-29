# coding: gb2312

'''����gb2312������ļ��Ը��������Ӱ��
You may see ugly chars. Try print unicode(__doc__,"gb2312")
'''

#�� utf8 '\xe6\xb1\x89' gb2312 '\xba\xba' utf16 '\u6c49'

def print_hz_gb():
    h = '��'
    print "Test1"
    print repr(h) # '\xba\xba'
    print len(h)  # 2

    
    print "\nTest2"
    u = u'��'
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
    print u"����һ��"
    print "����һ��" #��������룬˵�������֧��GB2312
    #��eric4��shell���棬֧�ֵ���UTF8����֪����θ���ΪGB2312
    #��WindowsCMD���棬֧�ֵ���GB2312����֪����θ���ΪUTF8
    
    print "\nTest6"
    print globals()['__doc__']
    print unicode(globals()['__doc__'],"gb2312")
    print unicode(globals()['__doc__'],"gb2312").encode("utf-8")

if __name__ == '__main__':
    print_hz_gb()

    
