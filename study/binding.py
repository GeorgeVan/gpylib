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
    '''exec里面的赋值，结果比较复杂'''
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
        c             #LOAD_GLOBAL 编译器只能认定c是全局变量
        
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
    只要函数体中出现exec语句，那么被之前判断为全局的变量都采用LOAD_NAME命令载入。
    这样，当exec语句动态地创建了局域变量时，能优先载入局域变量的值，当局域变量不存在时，
    再载入全局变量。

    LOAD_NAME命令从代码对象的co_names属性读取变量名，然后依次从局域变量的字典以及
    全局变量的字典寻找对应的值。
            
    在编译的时候，不去考察exec的内容。所以名字会以如下方式变为OPCODE
    freevar refing upper function: LOAD_DEREF
    freevar refing global : LOAD_NAME
    纯本地： LOAD_FAST

    EXEC执行后，这些代码还是会用之前的OPCODE。
    所以如果在EXEC中给名字绑定后，具体会用哪些，会比较复杂。
    1) free var refing uppfunction: 
        在locals() 创建了新名字覆盖了freevar。
        但是已经编译的代码还是会使用父函数的那个对象。
        
        如果只是使用，则会去global空间找这个变量。如果global和上次func有
        同一个，则忽略了上层func
    2）freevar 纯全局变量
        如果覆盖定义，则代码会使用新值。因为是LOAD_NAME
        而且可以删除这个name，达到动态切换名字指向的效果。
            
    http://hyry.dip.jp/tech/book/page/python/variable_scope_global.html

    '''
    def f2():
        a             #LOAD_DEREF
        __testexecrun #LOAD_NAME
        b=1           #STORE_FAST
        b             #LOAD_FAST
        c = []
        
        #情况0：0-1 无法修改编译的时候使用 *_Fast的普通局部变量的绑定
        exec("b=2") in globals(), locals()
        assert b==1
        
        #情况0：0-2 不修改绑定，只是调用内部函数，可以方便实现功能 
        exec("c.append(34)") in globals(), locals()
        assert c[0]==34
        
        '''情况A-1：访问：exec无法访问到非全局变量的freevar'''
        assert a==0
        assert locals().get("a",None) is None
        #locals()没有返回freevar
        try:
            exec("a")in globals(),locals()
            #因为a是一个上层函数的freevar，所以在globals()和locals()里面都没有
            #所以找不到
        except NameError as ne:
            print GREEN+str(ne)
        else:
            print RED+"测试失败"
            
        '''情况A-2：访问：使用一个freevar，会从global里面找，而不会从最近的block'''
        assert _testexec_g == 2
        exec("d=_testexec_g") in globals(),locals()
        assert locals().get("d",None) == 1 != _testexec_g
        #Free variables  are not resolved in the nearest enclosing namespace, 
        #but in the global namespace.
            
        '''情况B-1： 覆盖：在local重新定义了一个和纯父FUNCfreeval一样的name
        locals()的函数说明不保证这个代码OK'''
        exec("a=10") in globals(), locals()
        assert locals().get("a",None) == 10
        assert a==0 #LOAD_DEREF 这个是在编译的时候就确定了，所以不受本地a的影响
        
        exec("del a") in globals(), locals()
        assert locals().get("a",None) is None
        assert a==0 #LOAD_DEREF
        
        
        '''情况B-2：覆盖：这个是在本地创造了而一个 _testexec_g 变量，全局的也不变化'''
        assert _testexec_g == 2
        exec("_testexec_g=3;") in globals(), locals()
        assert _testexec_g == 2 #这个是 free变量 LOAD_DEREF
        assert locals().get("_testexec_g",None) == 3
        assert globals().get("_testexec_g",None) == 1
        exec("del _testexec_g;") in globals(), locals()
        assert locals().get("_testexec_g",None) == None

        
        '''情况C-1：全局：给global定义了一个全新name，在外部可以访问'''
        exec("_testexec_a=10") in globals()
        assert locals().get("_testexec_a",None) is None
        global _testexec_a
        assert _testexec_a == 10
        assert globals().get("_testexec_a",None) is _testexec_a
        
        '''情况C-2：全局：在全局空间里面修改旧全局变量'''
        exec("_testexec_h=30;") in globals()
        assert _testexec_h == 20
        assert locals().get("_testexec_h",None) == None
        assert globals().get("_testexec_h",None) == 30
        
        '''情况C-3：全局：在全局空间里面修改全局变量'''
        exec("global _testexec_c; _testexec_c=300;") in globals(), locals()
        assert _testexec_c == 200 #这个是 free变量 LOAD_DEREF
        assert locals().get("_testexec_c",None) == None
        assert globals().get("_testexec_c",None) == 300

        
        '''情况D：动态：全局变量_testexec_d可以变换局部/全局'''
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
    '''查询locals()函数的说明：
    The contents of this dictionary should not be modified; 
    changes may not affect the values of local and free variables 
    used by the interpreter.
    '''
    
    ddd=copy.copy(locals())
    exec("y=4")in globals(), ddd
    assert ddd['y']==4
    assert y==2
    '''而这也果然就可以了'''
    
    exec("z=1")
    assert z==1 #LOAD_NAME
    '''定义一个新变量，可以，因为这个是freeval，只能用LOAD_NAME'''
    
    exec("q=1") in globals(),locals()
    assert q==1 #LOAD_NAME
    '''定义一个新变量，可以'''
    
#testexec0();testexec()

    
def testdummy1():pass
_testnames_g1="_testnames_g1_string"
def testnames():
    '''测试python的名字静态编译后的表格
    对于理解名字scope等诸多概念都有好处
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
        
        from gpylib.misc import printfuncodeinfo #printfuncodeinfo也会存在于 co_names，没空深究
        printfuncodeinfo(colorama,testnames)
        assert set(['_testnames_g1', 'testdummy1', 'testdummy2']) == set(testnames.func_code.co_names)
        assert set(['b', 'C', 'D', 'f0bak', 'Dbak']) == set(testnames.func_code.co_varnames)
        assert len(testnames.func_code.co_freevars)==0
        assert set(['a', 'f0']) == set(testnames.func_code.co_cellvars)
        
        printfuncodeinfo(colorama,f0)#这里打印的也只是父block中的f0名字而已。
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
    #f0bak() #现在打印出来的f0其实已经是testdummy2了
    #因为加上了assert，所以这个如果执行，就会出错
    
    Dbak=D
    D=C
def testdummy2():pass
_testnames_g2="_testnames_g1_string"
    
#testnames()    

def testdynamicfunc7():
    '''
    原理：Python没有局部对象的概念，只有局部name的概念。所有对象都是全局的。
    原理1：一个函数F如果用了局部名称，无论局部变量是在哪一级函数中定义的，则函数在调用的时候，
    会使用最新的这个局部名称对应的对象。也就是说，回去locals()、globals()里面去找这个对象。
    这个locals()是函数定义的地方的locals()和globals()
    推理1：如果定义这些局部名称的父函数已经返回，而外部还引用了F，则如果外部调用F，则F中的局部
    名称对应的对象是父函数返回的时刻的那个对象。
    引用了一个已经结束调用的函数f里面定义的函数f1，而f1还使用了f0的局部变量，看起来很有陷阱，但是
    python却保证这个f0指向的函数对象能够被调用。


    初始理解：函数引用的name，在该block运行过程中变化，该name总能实时反应
    在执行的时候，才按照命名空间去找该name所引用的对象。
    python的object，无论怎么创建都没有区别。程序中只是和name打交道。
    name只是指向哪个object。但是程序中的代码只指向name。每次用这个
    name的时候，才去找这个name所对应的object。这个和C完全相反。
    
    而通过观察f.func_closure[0].cell_contents，能够看到，只要freevariable
    被赋值，cell_contents就会立刻更新。而不是调用的时候才更新。
    
    继续看cpython的实现中 PyCodeObject的代码，可以看到python把函数block中定义的
    被子孙block使用的变量单独放置一个List里面。猜测这样的话，这些变量被赋值的时候
    python回去修改这些子孙的func_closure里面的值。
    
    python中的name是静态的，是代码写好后就确定的了。每个名字在什么地方定义，是在
    编译的时候就确定的了。推理而言，每使用一个名字，在执行的时候去哪个BLOCK去找那个
    被绑定的Object，也是静态的。
    
    看二进制代码，对于这些name，在binding的时候使用了：STORE_DEREF
    Stores TOS into the cell contained in slot i of the cell and free variable storage.
    
    '''
    def checkfuncclosure(f,n,i):
        assert f.__code__.co_freevars[0] == n
        assert f.func_closure[0].cell_contents is i
        
    def ff(i):
        def f0():
            return b
        
        try:       
            checkfuncclosure(f0,'b',None)#空
        except ValueError as e:
            print GREEN+str(e)
        
        for x in (11,22):
            b=[x*i]
            checkfuncclosure(f0,'b',b) 
            #f.func_closure[0].cell_contents立刻变化了，所以函数无论何时被调用，
            #都会使用最新的free variable对象
            yield b,f0 
            #后面的多次Yield，f0是不变化的，b变化了
        
        for x in (33,44,55):
            b=[x*i]
            checkfuncclosure(f0,'b',b) 
            yield b,None

        
    print "\n[Position 1]"
    bf=[]
    for b,f in ff(1):
        bf.append([b, f])
        checkfuncclosure(bf[0][1],'b',b)
        #只检查第一个返回的函数对象即可
        
    assert bf[0][1] is bf[1][1] #f
    assert bf[0][1]() is bf[-1][0] is not bf[0][0] #b 
    
        
    '''第二部分，证明了不同的调用其返回的函数真正执行的时候，其环境已经不同了
    第二次环境里面的局部变量，已经不会对第一次的函数结果造成影响。
    说明，如果局部函数引用的局部变量具有镜像功能。
    '''
    print "\n[Position 3]"
    bf2=[]
    for b,f in ff(1):
        bf2.append([b, f])
        checkfuncclosure(bf2[0][1],'b',b)
        #只检查第一个返回的函数对象即可
        
    assert bf2[0][1] is bf2[1][1] #f
    assert bf2[0][1]() is bf2[-1][0] is not bf2[0][0] #b 

    print "\n[Position 5]"
    assert bf[0][1] is not bf2[0][1]() #f
    
    bf[-1][0][0]="me"
    
    assert bf[0][1]()[0] is bf[1][1]()[0] is bf[-1][0][0] is not bf2[0][1]()[0]
    
    print "\n[Position 6"
    bf2[-1][0][0]="you"
    assert bf2[0][1]()[0] is bf2[1][1]()[0] is bf2[-1][0][0] is not bf[0][1]()[0]
    
    global _ghc_f #用于在命令行调试
    _ghc_f=bf[0][1]
    
    from gpylib.misc import printfuncodeinfo
    printfuncodeinfo(colorama, _ghc_f)
    printfuncodeinfo(colorama, testdynamicfunc7)
    printfuncodeinfo(colorama, ff)
    
#testdynamicfunc7() 


def testdynamicfunc5():
    '''一个函数对象引用了已经执行完毕的外部block一个局部变量，在外部修改它'''
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
    #说明在ff return的时候，f记住了当时的a
    print "testdynamicfunc5 ended"
    
#testdynamicfunc5()    

def testdynamicfunc4():
    '''一个函数对象引用了已经执行完毕的外部block一个局部变量'''
    print "\n\ntestdynamicfunc4 started"
    def ff(i):
        def f0():
            print "[ID{}]={}".format(id(a),a)
            return id(a), a
        a=i*3
        return f0
        #返回的这个函数对象使用了局部变量，这个变量的对象就是返回时刻绑定的那个对象
        #block的局部变量a是每次这个block执行的时候绑定的一个新对象
    
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
        #说明每次执行的时候都会去找name[a]的绑定对象，找到了上一级block的a
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
        #在此次的ff1对象中会保留一个对ll/对i的引用
        #因为Python的函数是个对象，而python对所有变量都使用同样的垃圾回收机制。
        #局部变量和全局变量在生命周期上没有区别。无论是什么name，只要被赋一个值，就会有一个对象
        #创建。这个对象何时销毁很难说。
        #因此返回的函数使用局部变量这件事情就很容易理解。
        #外部无法把ll给清除掉。即使在外部调用del ll，也只是把外部的变量名ll和ll指向的对象给解锁而已
        #Python的函数是一个实例，而不是一段代码。这个是其方便的一个重要原因。
        
    ll=[1,2,3,4]
    ff=ff0(ll)
    
    print ff(1)
    ll[2]=9999
    
    print ff(1)
    
    ff1=ff0(ll)
    
    print id(ff), id(ff1)
    assert id(ff)!=id(ff1)
    #这两个不同，虽然功能一样。
    
    print "testdynamicfunc2 ended"
    
#testdynamicfunc2()

def testdynamicfunc1():
    print "\n\ntestdynamicfunc1 started"
    ll,counts = [],[0,0,0]
    
    def f0():
        def f1():
            ll.append( (id(f1),counts[0],1) )
            counts[0] += 1 #无法使用int类型，如使用了，就是一个新变量了。
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
    
    '''根据f1/f2/f3的实现代码不同，uniqueidcount有所区别，在测试的时候是154个
    结论f0/f1/f3/f3都是动态创建的，不是300是可能是因为有垃圾回收'''
    
#testdynamicfunc1()

def testdynamicfunc9():
    '''name的environment是代码级别的，不是执行级别的'''
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
        #在运行时找不到a
    else:
        print RED+"Test failed"
        
    def f1():
        f0()
        
        try:
            print "\n[Postion 2]"
            f0(True)
        except NameError as e:
            print GREEN+ "f0(True) failed: [{}]{}\n".format(e.__class__.__name__,str(e))
            #在运行时找不到a
        else:
            print RED+"Test failed"
        
        a=6
        try:
            print "\n[Postion 3]"
            f0(True)
        except NameError as e:
            print GREEN+ "f0(True) failed: [{}]{}\n".format(e.__class__.__name__,str(e))
            #这里会Exception，说明f00会在自己的environment里面查找'a'对应的对象，
            #而不是在调用的environment里面去找
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
            '''这里会Exception，是因为f00会从自己的block往上找，找到testdynamicfunc9发现有一个a=5
            但是这个a的binding代码还没有开始执行。按照python的逻辑，不会继续去全局空间找了。
            
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
    
    
    #即使在global定义之前，也可以用这个变量，但是会出现一个警告
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
    #x和y实际上指向的是同一个东东
    #不论Object是否mutualble，只要互相赋值，都只指向同一个对象
    #比如将一个名字通过参数传递到函数中一样
    #不论Object是否Mutuable,作为参数传递进去后。如果重新赋值，都和之前的对象没有关系。
    #所谓Mutuable只是因为有内部函数可以调用来修改。
    
    def test(c):
        id3=id(c)
        c=5
        id4=id(c)
        return id3,id4
        
    id3,id4 = test(x) #打印出来的第一个ID和之前x/y都相同
    assert id1==id2==id3!=id4
    
    y=2
    id5=id(y)
    assert id1!=id5
    #现在Y的ID就变了
    
    y=3
    id6=id(y)
    assert id5!=id6
    #现在Y的ID也变了
    
    print "testobjectid ended"
    
#testobjectid()

testslope_lll=["aaa",]
def testdynamicscope():    
    print "\n\ntestdynamicscope started"
    testslope_lll=['bbb']
    del testslope_lll
    #这个name是这个block的name
    
    try:
        a=testslope_lll
        #表面上看，因为local的这个变量被删除了，那么就可以去global中去找
        #但是python不支持这个动态过程，一个name是指向哪个block，代码写好就固定好了
    except Exception as e:
        print GREEN+str(e)
   
    print "testdynamicscope ended"

#testdynamicscope()


def testblock1():
    print "\n\ntestblock1 started"
    n = 1

    def inner():
        n = 'x' #这个绑定操作后，在这个block的所有n都是'x'了，和全局的n无关
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
    
    print a #Defined in True，因为if语句并不构成一个block，所以a是本block的局部变量了
    
    for i in xrange(4):
        iii = i
        
    print i, iii
    #在一个block中定义后，都可以使用    
    
    print "testblock1 ended"
#testblock1()
