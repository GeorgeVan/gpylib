# -*- coding: gb2312 -*-

import re, dis,copy,inspect,random
import colorama

GREEN=colorama.Fore.GREEN+colorama.Style.BRIGHT
RED=colorama.Fore.RED+colorama.Style.BRIGHT
BLUE=colorama.Fore.BLUE+colorama.Style.BRIGHT

if __name__ == '__main__':
    colorama.init(autoreset=True)


__testexecrun=False
_testexec_g = 1
_testexec_h = 10
_testexec_c = 100
_testexec_d = 1000

def testexec():
    '''exec����ĸ�ֵ������Ƚϸ���'''
    a = 0   
    #STORE_DEREF Stores TOS into the cell contained in slot i of the cell 
    #and free variable storage.
    
    _testexec_g = 2
    _testexec_h = 20
    _testexec_c = 200
    def f1():
        __testexecrun #LOAD_GLOBAL
        a             #LOAD_DEREF
        b=1           #STORE_FAST
        _testexec_g   #LOAD_DEREF
        global _testexec_h
        _testexec_h   #LOAD_GLOBAL  
        c             #LOAD_GLOBAL ������ֻ���϶�c��ȫ�ֱ���
        
    print "Code of f1:\n", dis.dis(f1)    

    def f11():
        __testexecrun #LOAD_NAME******
        a             #LOAD_DEREF
        b=1           #STORE_FAST
        _testexec_g   #LOAD_DEREF
        global _testexec_h
        _testexec_h   #LOAD_GLOBAL  
        c             #LOAD_NAME*******
        exec("") in globals(), locals()
    print "Code of f11:\n", dis.dis(f11)

    '''
    If exec is used in a function and the function contains or is a nested block 
    with free variables, the compiler will raise a SyntaxError unless the exec 
    explicitly specifies the local namespace for the exec. (In other words, exec 
    obj would be illegal, but exec obj in ns would be legal.)

    The eval(), execfile(), and input() functions and the exec statement do not 
    have access to the full environment for resolving names. Names may be 
    resolved in the local and global namespaces of the caller. Free variables 
    are not resolved in the nearest enclosing namespace, but in the global 
    namespace. [1] The exec statement and the eval() and execfile() functions 
    have optional arguments to override the global and local namespace. If only 
    one namespace is specified, it is used for both.

    http://docs.python.org/2/reference/executionmodel.html
    4.4.1
    '''
    
    '''
    ֻҪ�������г���exec��䣬��ô��֮ǰ�ж�Ϊȫ�ֵı���������LOAD_NAME�������롣
    ��������exec��䶯̬�ش����˾������ʱ��������������������ֵ�����������������ʱ��
    ������ȫ�ֱ�����

    LOAD_NAME����Ӵ�������co_names���Զ�ȡ��������Ȼ�����δӾ���������ֵ��Լ�
    ȫ�ֱ������ֵ�Ѱ�Ҷ�Ӧ��ֵ��
            
    �ڱ����ʱ�򣬲�ȥ����exec�����ݡ��������ֻ������·�ʽ��ΪOPCODE
    freevar refing upper function: LOAD_DEREF
    freevar refing global : LOAD_NAME
    �����أ� LOAD_FAST

    EXECִ�к���Щ���뻹�ǻ���֮ǰ��OPCODE��
    ���������EXEC�и����ְ󶨺󣬾��������Щ����Ƚϸ��ӡ�
    1) free var refing uppfunction: 
        ��locals() �����������ָ�����freevar��
        �����Ѿ�����Ĵ��뻹�ǻ�ʹ�ø��������Ǹ�����
        
        ���ֻ��ʹ�ã����ȥglobal�ռ���������������global���ϴ�func��
        ͬһ������������ϲ�func
    2��freevar ��ȫ�ֱ���
        ������Ƕ��壬������ʹ����ֵ����Ϊ��LOAD_NAME
        ���ҿ���ɾ�����name���ﵽ��̬�л�����ָ���Ч����
            
    http://hyry.dip.jp/tech/book/page/python/variable_scope_global.html

    '''
    def f2():
        a             #LOAD_DEREF
        __testexecrun #LOAD_NAME
        b=1           #STORE_FAST
        b             #LOAD_FAST
        c = []
        
        #���0��0-1 �޷��޸ı����ʱ��ʹ�� *_Fast����ͨ�ֲ������İ�
        exec("b=2") in globals(), locals()
        assert b==1
        
        #���0��0-2 ���޸İ󶨣�ֻ�ǵ����ڲ����������Է���ʵ�ֹ��� 
        exec("c.append(34)") in globals(), locals()
        assert c[0]==34
        
        '''���A-1�����ʣ�exec�޷����ʵ���ȫ�ֱ�����freevar'''
        assert a==0
        assert locals().get("a",None) is None
        #locals()û�з���freevar
        try:
            exec("a")in globals(),locals()
            #��Ϊa��һ���ϲ㺯����freevar��������globals()��locals()���涼û��
            #�����Ҳ���
        except NameError as ne:
            print GREEN+str(ne)
        else:
            print RED+"����ʧ��"
            
        '''���A-2�����ʣ�ʹ��һ��freevar�����global�����ң�������������block'''
        assert _testexec_g == 2
        exec("d=_testexec_g") in globals(),locals()
        assert locals().get("d",None) == 1 != _testexec_g
        #Free variables  are not resolved in the nearest enclosing namespace, 
        #but in the global namespace.
            
        '''���B-1�� ���ǣ���local���¶�����һ���ʹ���FUNCfreevalһ����name
        locals()�ĺ���˵������֤�������OK'''
        exec("a=10") in globals(), locals()
        assert locals().get("a",None) == 10
        assert a==0 #LOAD_DEREF ������ڱ����ʱ���ȷ���ˣ����Բ��ܱ���a��Ӱ��
        
        exec("del a") in globals(), locals()
        assert locals().get("a",None) is None
        assert a==0 #LOAD_DEREF
        
        
        '''���B-2�����ǣ�������ڱ��ش����˶�һ�� _testexec_g ������ȫ�ֵ�Ҳ���仯'''
        assert _testexec_g == 2
        exec("_testexec_g=3;") in globals(), locals()
        assert _testexec_g == 2 #����� free���� LOAD_DEREF
        assert locals().get("_testexec_g",None) == 3
        assert globals().get("_testexec_g",None) == 1
        exec("del _testexec_g;") in globals(), locals()
        assert locals().get("_testexec_g",None) == None

        
        '''���C-1��ȫ�֣���global������һ��ȫ��name�����ⲿ���Է���'''
        exec("_testexec_a=10") in globals()
        assert locals().get("_testexec_a",None) is None
        global _testexec_a
        assert _testexec_a == 10
        assert globals().get("_testexec_a",None) is _testexec_a
        
        '''���C-2��ȫ�֣���ȫ�ֿռ������޸ľ�ȫ�ֱ���'''
        exec("_testexec_h=30;") in globals()
        assert _testexec_h == 20
        assert locals().get("_testexec_h",None) == None
        assert globals().get("_testexec_h",None) == 30
        
        '''���C-3��ȫ�֣���ȫ�ֿռ������޸�ȫ�ֱ���'''
        exec("global _testexec_c; _testexec_c=300;") in globals(), locals()
        assert _testexec_c == 200 #����� free���� LOAD_DEREF
        assert locals().get("_testexec_c",None) == None
        assert globals().get("_testexec_c",None) == 300

        
        '''���D����̬��ȫ�ֱ���_testexec_d���Ա任�ֲ�/ȫ��'''
        tmp=_testexec_d
        assert _testexec_d == 1000
        exec("_testexec_d=2000;") in globals(), locals()
        assert _testexec_d==2000
        assert _testexec_d is not tmp
        assert tmp==1000
        exec("del _testexec_d") in globals(), locals()
        assert _testexec_d == 1000
        assert _testexec_d is tmp
        
    
    f2()
    
    def f3():
        x=1
        cod=compile("x=2",'<string>','exec')
        #dis.dis(cod)#STORE_NAME
        exec(cod) in globals(), locals()
        assert locals()['x'] is x
        assert x==1
    f3()
    
    #print dis.dis(testexec)
    #print dis.dis(f1)
    #print dis.dis(f2)
    #print dis.dis(f3)


def testexec0():
    y=1 #STORE_FAST
    exec("y=2")
    assert y==2 #LOAD_FAST

    cod=compile("y=3",'<string>','exec')
    dis.dis(cod) #STORE_NAME
    print cod.co_names

    exec(cod) in globals(), locals()
    assert y==2  #LOAD_FAST
    
    
    exec("y=4")in globals(), locals()
    assert y==2 #LOAD_FAST
    '''��ѯlocals()������˵����
    The contents of this dictionary should not be modified; 
    changes may not affect the values of local and free variables 
    used by the interpreter.
    '''
    
    ddd=copy.copy(locals())
    exec("y=4")in globals(), ddd
    assert ddd['y']==4
    assert y==2
    '''����Ҳ��Ȼ�Ϳ�����'''
    
    exec("z=1")
    assert z==1 #LOAD_NAME
    '''����һ���±��������ԣ���Ϊ�����freeval��ֻ����LOAD_NAME'''
    
    exec("q=1") in globals(),locals()
    assert q==1 #LOAD_NAME
    '''����һ���±���������'''
    
#testexec0();testexec()

    
def testdummy1():pass
_testnames_g1="_testnames_g1_string"
def testnames():
    '''����python�����־�̬�����ı��
    �����������scope��������кô�
    '''
    a=1
    b=1
    a="string a" + _testnames_g1
    b="string b"
    
    class C:
        pass
    
    class D:
        pass
    def f0():
        x=_testnames_g1 + a 
        x="string x"
        y="string y"
        def f1():
            i= _testnames_g1 + a + x
            i="string i"
            j='string j'
        
        from gpylib.misc import printfuncodeinfo #printfuncodeinfoҲ������� co_names��û���
        printfuncodeinfo(colorama,testnames)
        assert set(['_testnames_g1', 'testdummy1', 'testdummy2']) == set(testnames.func_code.co_names)
        assert set(['b', 'C', 'D', 'f0bak', 'Dbak']) == set(testnames.func_code.co_varnames)
        assert len(testnames.func_code.co_freevars)==0
        assert set(['a', 'f0']) == set(testnames.func_code.co_cellvars)
        
        printfuncodeinfo(colorama,f0)#�����ӡ��Ҳֻ�Ǹ�block�е�f0���ֶ��ѡ�
        assert set(['y', 'f1', 'printfuncodeinfo', 'z']) == set(f0.func_code.co_varnames)
        assert set(['a', 'f0']) == set(f0.func_code.co_freevars)
        assert set(['x']) == set(f0.func_code.co_cellvars)
        
        printfuncodeinfo(colorama,f1)
        assert set(['i', 'j']) == set(f1.func_code.co_varnames)
        assert set(['a', 'x']) == set(f1.func_code.co_freevars)
        assert len(f1.func_code.co_cellvars)==0
        
        z=re.compile("abcd")
        
    testdummy1()
    testdummy2()
    
    f0()
    
    f0bak=f0
    f0=testdummy2
    print "\n\n\n\nPosition 1"
    #f0bak() #���ڴ�ӡ������f0��ʵ�Ѿ���testdummy2��
    #��Ϊ������assert������������ִ�У��ͻ����
    
    Dbak=D
    D=C
def testdummy2():pass
_testnames_g2="_testnames_g1_string"
    
#testnames()    

def testdynamicfunc7():
    '''
    ԭ��Pythonû�оֲ�����ĸ��ֻ�оֲ�name�ĸ�����ж�����ȫ�ֵġ�
    ԭ��1��һ������F������˾ֲ����ƣ����۾ֲ�����������һ�������ж���ģ������ڵ��õ�ʱ��
    ��ʹ�����µ�����ֲ����ƶ�Ӧ�Ķ���Ҳ����˵����ȥlocals()��globals()����ȥ���������
    ���locals()�Ǻ�������ĵط���locals()��globals()
    ����1�����������Щ�ֲ����Ƶĸ������Ѿ����أ����ⲿ��������F��������ⲿ����F����F�еľֲ�
    ���ƶ�Ӧ�Ķ����Ǹ��������ص�ʱ�̵��Ǹ�����
    ������һ���Ѿ��������õĺ���f���涨��ĺ���f1����f1��ʹ����f0�ľֲ��������������������壬����
    pythonȴ��֤���f0ָ��ĺ��������ܹ������á�


    ��ʼ��⣺�������õ�name���ڸ�block���й����б仯����name����ʵʱ��Ӧ
    ��ִ�е�ʱ�򣬲Ű��������ռ�ȥ�Ҹ�name�����õĶ���
    python��object��������ô������û�����𡣳�����ֻ�Ǻ�name�򽻵���
    nameֻ��ָ���ĸ�object�����ǳ����еĴ���ָֻ��name��ÿ�������
    name��ʱ�򣬲�ȥ�����name����Ӧ��object�������C��ȫ�෴��
    
    ��ͨ���۲�f.func_closure[0].cell_contents���ܹ�������ֻҪfreevariable
    ����ֵ��cell_contents�ͻ����̸��¡������ǵ��õ�ʱ��Ÿ��¡�
    
    ������cpython��ʵ���� PyCodeObject�Ĵ��룬���Կ���python�Ѻ���block�ж����
    ������blockʹ�õı�����������һ��List���档�²������Ļ�����Щ��������ֵ��ʱ��
    python��ȥ�޸���Щ�����func_closure�����ֵ��
    
    python�е�name�Ǿ�̬�ģ��Ǵ���д�ú��ȷ�����ˡ�ÿ��������ʲô�ط����壬����
    �����ʱ���ȷ�����ˡ�������ԣ�ÿʹ��һ�����֣���ִ�е�ʱ��ȥ�ĸ�BLOCKȥ���Ǹ�
    ���󶨵�Object��Ҳ�Ǿ�̬�ġ�
    
    �������ƴ��룬������Щname����binding��ʱ��ʹ���ˣ�STORE_DEREF
    Stores TOS into the cell contained in slot i of the cell and free variable storage.
    
    '''
    def checkfuncclosure(f,n,i):
        assert f.__code__.co_freevars[0] == n
        assert f.func_closure[0].cell_contents is i
        
    def ff(i):
        def f0():
            return b
        
        try:       
            checkfuncclosure(f0,'b',None)#��
        except ValueError as e:
            print GREEN+str(e)
        
        for x in (11,22):
            b=[x*i]
            checkfuncclosure(f0,'b',b) 
            #f.func_closure[0].cell_contents���̱仯�ˣ����Ժ������ۺ�ʱ�����ã�
            #����ʹ�����µ�free variable����
            yield b,f0 
            #����Ķ��Yield��f0�ǲ��仯�ģ�b�仯��
        
        for x in (33,44,55):
            b=[x*i]
            checkfuncclosure(f0,'b',b) 
            yield b,None

        
    print "\n[Position 1]"
    bf=[]
    for b,f in ff(1):
        bf.append([b, f])
        checkfuncclosure(bf[0][1],'b',b)
        #ֻ����һ�����صĺ������󼴿�
        
    assert bf[0][1] is bf[1][1] #f
    assert bf[0][1]() is bf[-1][0] is not bf[0][0] #b 
    
        
    '''�ڶ����֣�֤���˲�ͬ�ĵ����䷵�صĺ�������ִ�е�ʱ���价���Ѿ���ͬ��
    �ڶ��λ�������ľֲ��������Ѿ�����Ե�һ�εĺ���������Ӱ�졣
    ˵��������ֲ��������õľֲ��������о����ܡ�
    '''
    print "\n[Position 3]"
    bf2=[]
    for b,f in ff(1):
        bf2.append([b, f])
        checkfuncclosure(bf2[0][1],'b',b)
        #ֻ����һ�����صĺ������󼴿�
        
    assert bf2[0][1] is bf2[1][1] #f
    assert bf2[0][1]() is bf2[-1][0] is not bf2[0][0] #b 

    print "\n[Position 5]"
    assert bf[0][1] is not bf2[0][1]() #f
    
    bf[-1][0][0]="me"
    
    assert bf[0][1]()[0] is bf[1][1]()[0] is bf[-1][0][0] is not bf2[0][1]()[0]
    
    print "\n[Position 6"
    bf2[-1][0][0]="you"
    assert bf2[0][1]()[0] is bf2[1][1]()[0] is bf2[-1][0][0] is not bf[0][1]()[0]
    
    global _ghc_f #�����������е���
    _ghc_f=bf[0][1]
    
    from gpylib.misc import printfuncodeinfo
    printfuncodeinfo(colorama, _ghc_f)
    printfuncodeinfo(colorama, testdynamicfunc7)
    printfuncodeinfo(colorama, ff)
    
#testdynamicfunc7() 


def testdynamicfunc5():
    '''һ�����������������Ѿ�ִ����ϵ��ⲿblockһ���ֲ����������ⲿ�޸���'''
    print "\n\ntestdynamicfunc5 started"
    def ff(i):
        def f0():
            print a[0]
            return a[0]
        
        a=["abc"+str(i)]
        return a,f0
    
    a1,f1=ff(1)
    
    assert f1() == 'abc1'
    
    a1[0]='bcd' 
    assert f1() == 'bcd'
    #˵����ff return��ʱ��f��ס�˵�ʱ��a
    print "testdynamicfunc5 ended"
    
#testdynamicfunc5()    

def testdynamicfunc4():
    '''һ�����������������Ѿ�ִ����ϵ��ⲿblockһ���ֲ�����'''
    print "\n\ntestdynamicfunc4 started"
    def ff(i):
        def f0():
            print "[ID{}]={}".format(id(a),a)
            return id(a), a
        a=i*3
        return f0
        #���ص������������ʹ���˾ֲ���������������Ķ�����Ƿ���ʱ�̰󶨵��Ǹ�����
        #block�ľֲ�����a��ÿ�����blockִ�е�ʱ��󶨵�һ���¶���
    
    f1=ff(1)
    f2=ff(2)
    
    id1,a1=f1()
    id2,a2=f2()
    id3,d3=f1()
    
    assert id1==id3!=id2
    print "testdynamicfunc4 ended"
    
#testdynamicfunc4()    
    
def testdynamicfunc3():
    print "\n\ntestdynamicfunc3 started"
    def f0():
        print a,b,c
        #˵��ÿ��ִ�е�ʱ�򶼻�ȥ��name[a]�İ󶨶����ҵ�����һ��block��a
    a,b,c=1,2,3
    f0()
    
    a,b,c,=4,5,6
    f0()
    print "testdynamicfunc2 ended"

#testdynamicfunc3()

def testdynamicfunc2():
    print "\n\ntestdynamicfunc2 started"
    def ff0(ll):
        i=1
        def ff1(a):
            return ll[i+a]
        
        return ff1
        #�ڴ˴ε�ff1�����лᱣ��һ����ll/��i������
        #��ΪPython�ĺ����Ǹ����󣬶�python�����б�����ʹ��ͬ�����������ջ��ơ�
        #�ֲ�������ȫ�ֱ���������������û������������ʲôname��ֻҪ����һ��ֵ���ͻ���һ������
        #��������������ʱ���ٺ���˵��
        #��˷��صĺ���ʹ�þֲ������������ͺ�������⡣
        #�ⲿ�޷���ll�����������ʹ���ⲿ����del ll��Ҳֻ�ǰ��ⲿ�ı�����ll��llָ��Ķ������������
        #Python�ĺ�����һ��ʵ����������һ�δ��롣������䷽���һ����Ҫԭ��
        
    ll=[1,2,3,4]
    ff=ff0(ll)
    
    print ff(1)
    ll[2]=9999
    
    print ff(1)
    
    ff1=ff0(ll)
    
    print id(ff), id(ff1)
    assert id(ff)!=id(ff1)
    #��������ͬ����Ȼ����һ����
    
    print "testdynamicfunc2 ended"
    
#testdynamicfunc2()

def testdynamicfunc1():
    print "\n\ntestdynamicfunc1 started"
    ll,counts = [],[0,0,0]
    
    def f0():
        def f1():
            ll.append( (id(f1),counts[0],1) )
            counts[0] += 1 #�޷�ʹ��int���ͣ���ʹ���ˣ�����һ���±����ˡ�
            def f2():
                ll.append((id(f2), counts[1],2))
                counts[1] += 1
            f2()
        
        f1()
        
        def f3():pass
        f3()
        
        ll.append((id(f3), counts[2],3))
        counts[2] += 1
    
    for x in xrange(100):
        f0()
    
    la,cc = -1,0
    for a,b,c in sorted(ll):
        if a!=la:
            stra = a
            cc += 1
            la=a
        else:
            stra = "        "
        print "{}\t{}\t{}".format(stra, b,c)
        
    print "\n\nUnique id count ", cc
    
    #print "\n\nUnique id count ", len( {}.fromkeys([a for (a,b,c) in ll]).keys())
    
    print "testdynamicfunc1 ended"
    
    '''����f1/f2/f3��ʵ�ִ��벻ͬ��uniqueidcount���������ڲ��Ե�ʱ����154��
    ����f0/f1/f3/f3���Ƕ�̬�����ģ�����300�ǿ�������Ϊ����������'''
    
#testdynamicfunc1()

def testdynamicfunc9():
    '''name��environment�Ǵ��뼶��ģ�����ִ�м����'''
    '''http://docs.python.org/2/reference/executionmodel.html#naming-and-binding'''
    def f0(c=False):
        print "f0{{{{{{{{{{{{{{"
        def f00():
            print "\tf00{{{{{{{{{{{{{{"
            print "\t\t", a
            print "\tf00}}}}}}}}}}}}}}"
        if c:
            f00()
        print "f0}}}}}}}}}}}}}}"
    f0()
    try:
        print "\n[Postion 1]"
        f0(True)
    except NameError as e:
        print GREEN+ "f0(True) failed: [{}]{}\n".format(e.__class__.__name__,str(e))
        #������ʱ�Ҳ���a
    else:
        print RED+"Test failed"
        
    def f1():
        f0()
        
        try:
            print "\n[Postion 2]"
            f0(True)
        except NameError as e:
            print GREEN+ "f0(True) failed: [{}]{}\n".format(e.__class__.__name__,str(e))
            #������ʱ�Ҳ���a
        else:
            print RED+"Test failed"
        
        a=6
        try:
            print "\n[Postion 3]"
            f0(True)
        except NameError as e:
            print GREEN+ "f0(True) failed: [{}]{}\n".format(e.__class__.__name__,str(e))
            #�����Exception��˵��f00�����Լ���environment�������'a'��Ӧ�Ķ���
            #�������ڵ��õ�environment����ȥ��
        else:
            print RED+"Test failed"
        
    f1()
    
    def f2():
        global a
        a=10
        print "\n[Position 4]"
        try:
            f0(True)
        except NameError as e:
            print GREEN+ "f0(True) failed: [{}]{}\n".format(e.__class__.__name__,str(e))
            '''�����Exception������Ϊf00����Լ���block�����ң��ҵ�testdynamicfunc9������һ��a=5
            �������a��binding���뻹û�п�ʼִ�С�����python���߼����������ȥȫ�ֿռ����ˡ�
            
            Names refer to objects. Names are introduced by name binding operations. Each 
            occurrence of a name in the program text refers to the binding of that name 
            established in the innermost function block containing the use.
            '''
        else:
            print RED+"Test failed"
    
    f2()
    
    a=5
    print "\n[Postion 4]"
    f0(True)
    
#testdynamicfunc9()


testslop2_g ="some"
def testslope2():
    print "\n\ntestslope2 started"
    try:
        print a
    except Exception as e:
        print type(e) #NameError
    
    try:
        print b
    except Exception as e:
        print type(e) #UnboundError

    b=1
    
    
    #��ʹ��global����֮ǰ��Ҳ������������������ǻ����һ������
    testslop2_g = "something"
    print testslop2_g

    global testslop2_g,testslop2_f
    print testslop2_g
    
    testslop2_f="bb"
    print testslop2_f
    
    print "testslope2 ended"

#testslope2()


def testobjectid():
    print "\n\ntestobjectid started"
    x=1
    y=x
    
    id1=id(x)
    id2=id(y)
    assert id1==id2
    #x��yʵ����ָ�����ͬһ������
    #����Object�Ƿ�mutualble��ֻҪ���ำֵ����ָֻ��ͬһ������
    #���罫һ������ͨ���������ݵ�������һ��
    #����Object�Ƿ�Mutuable,��Ϊ�������ݽ�ȥ��������¸�ֵ������֮ǰ�Ķ���û�й�ϵ��
    #��νMutuableֻ����Ϊ���ڲ��������Ե������޸ġ�
    
    def test(c):
        id3=id(c)
        c=5
        id4=id(c)
        return id3,id4
        
    id3,id4 = test(x) #��ӡ�����ĵ�һ��ID��֮ǰx/y����ͬ
    assert id1==id2==id3!=id4
    
    y=2
    id5=id(y)
    assert id1!=id5
    #����Y��ID�ͱ���
    
    y=3
    id6=id(y)
    assert id5!=id6
    #����Y��IDҲ����
    
    print "testobjectid ended"
    
#testobjectid()

testslope_lll=["aaa",]
def testdynamicscope():    
    print "\n\ntestdynamicscope started"
    testslope_lll=['bbb']
    del testslope_lll
    #���name�����block��name
    
    try:
        a=testslope_lll
        #�����Ͽ�����Ϊlocal�����������ɾ���ˣ���ô�Ϳ���ȥglobal��ȥ��
        #����python��֧�������̬���̣�һ��name��ָ���ĸ�block������д�þ͹̶�����
    except Exception as e:
        print GREEN+str(e)
   
    print "testdynamicscope ended"

#testdynamicscope()


def testblock1():
    print "\n\ntestblock1 started"
    n = 1

    def inner():
        n = 'x' #����󶨲����������block������n����'x'�ˣ���ȫ�ֵ�n�޹�
        assert n=='x'
        '''Each occurrence of a name in the program text refers to the binding 
        of that name established in the innermost function block containing the use.
        http://docs.python.org/2/reference/executionmodel.html#naming-and-binding
        '''
    assert n==1
    inner()
    assert n==1
    
    if True:
        a="Defined in True"
    
    print a #Defined in True����Ϊif��䲢������һ��block������a�Ǳ�block�ľֲ�������
    
    for i in xrange(4):
        iii = i
        
    print i, iii
    #��һ��block�ж���󣬶�����ʹ��    
    
    print "testblock1 ended"
#testblock1()
