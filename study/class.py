# -*- coding: gb2312 -*-

import re, dis,copy,inspect,random
import colorama

GREEN=colorama.Fore.GREEN+colorama.Style.BRIGHT
RED=colorama.Fore.RED+colorama.Style.BRIGHT
BLUE=colorama.Fore.BLUE+colorama.Style.BRIGHT


if __name__ == '__main__':
    colorama.init(autoreset=True)

def test_method_object():
    def f(self,b):
        self.v=b
        
    class C(object):
        f1=f
    
    c=C()
    c.f1(1)
    
    C.f2=f
    c.f2(1)
    
    c.f3=f.__get__(c,C)
    c.f3(1)
    
    assert c.f1.im_func is c.f2.im_func is c.f3.im_func is f
    
    ms = [c.f1 for i in xrange(10)]
    ids=map(id,ms)
    assert len(set(ids))==10
    #每次调用都会激发 __get__，也会产生一个新的method对象
    
    ids1 = [id(c.f1) for i in xrange(10)]
    assert len(set(ids1))==1
    #如果c.f1没有引用，则会立刻销毁，造成连续调用的ID一样。
    
    
#test_method_object()

def testchangesuper():
    print BLUE+"testchangesuper"
    class C:
        a="a of C"
        def f(self):
            return 'f of C'
    class D:
        b="b of D"
        def f(self):
            return 'f of D'
    c=C()
    
    assert c.a is C.a
    assert c.f() == 'f of C'
    
    
    #动态修改实例的类
    c.__class__=D
    assert c.b is D.b
    assert c.f() == 'f of D'
    assert isinstance(c,D)
    
#testchangesuper()

def test_static_method_dynaic():
    print BLUE+"testmethoddynaic"
    class C:pass
    
    @staticmethod
    def f():pass
    C.f= f
    C.f()
    
    def g():pass
    C.g=staticmethod(g)
    C.g()
    
    class D:
        @staticmethod
        def f():pass
        
        def _g():pass
        g=staticmethod(_g)
    D.f()
    D.g()

#test_static_method_dynaic()
    
def test_class_in_func():
    '''测试函数里面的类的动态特性'''
    '''*******************************1***********************************'''
    def f():
        class C:pass
        return C
    print dis.dis(f)
    #定义一个类，其OPCODE是BUILD_CLASS(Creates a new class object)
    
    
    ins=[f()() for i in xrange(10)]
    cls2=[id(i.__class__) for i in ins]
    assert len(set(cls2))==10
    #发现每次返回的C都不同
    
    cls1=[id(f()) for i in xrange(10)]
    assert len(set(cls1))==1
    #因为这些类没有实例，但因为立刻被销毁了的缘故吧。所以id都一样。
    
    '''*******************************2***********************************'''
    #动态基类
    def f(base):
        class C(base):pass
        return C
    
    class A: 
        def read(self):
            return 'A'
    class B:
        def read(self):
            return 'B'
    
    AC=f(A)
    BC=f(B)
    
    assert AC().read()=='A' and BC().read()=='B'
    
    '''*******************************3***********************************'''
    #类block使用freevar
    def f(base, s):
        a = int(random.random()*1000)
        class C(base):
            x,y=a,s
        
        return C
        
    AC=f(A,"abc")
    BC=f(B,"xyz")
    
    assert AC.y=='abc' and BC.y=='xyz'
    assert AC.x != BC.x
    
    
    '''*******************************4***********************************'''
    #类method使用freevar
    #类method无法使用类block中定义的变量，如果要用，只能用class.x来使用。但是可以使用类BLOCK之上的
    def f(a):
        b = int(random.random()*1000) #STORE_DEREF
        class C:
            def m(self):
                return b,a   #LOAD_DEREF
        return b, C
    #dis.dis(f.func_code)
    #dis.dis(C.m.im_func.func_code)
    b, C=f(1)
    c=C()
    assert c.m() == (b,1)
    
    
    
#test_class_in_func()

def test_init_base():
    '''初始化的基类'''
    class P:
        def __init__(self,a):
            self.a=a
    
    class S(P):
        pass
     
    
    s=S("aaa")
    #如果没有定义__init__，则会调用父类的__init__。任意method都如此
    print s.a
    
    s=S()
    #虽然S没哟定义__init__，但是s这个实例能够看到__init__，所以就会被调用了。
    
#test_init_base()

def test_method_dynamic():
    print BLUE+"test_method_dynamic"
    class C:pass
    e=C()
    
    
    #1-----------------------------
    def func0(x):
        return x
    e.func0=func0 #实例属性是一个函数
    assert e.func0(5) == 5
    assert inspect.isfunction(e.func0)
    
    #2-----------------------------
    def funaa(self,v):
        self.e=v
    e.set=funaa #这个只是给e新增一个函数变量而已
    e.set(e,"Value of E")  #不能通过e.set("Value of E")来调用
    assert e.e == "Value of E"
    assert inspect.isfunction(e.set)
    assert not inspect.ismethod(e.set)

    
    #3-----------------------------
    class C:
        set = funaa #直接在定义里面添加就可以
        def g(self,v):
            self.aa=v
        h = g
    c=C()
    c.set("xyz")
    assert c.e=="xyz"
    c.h("abc")
    assert c.aa=="abc"

    c.set1=c.set
    c.set1("12345")
    assert c.e=="12345"

    #4-------------------------
    def funab(self):
        self.ab="funab"
    import functools
    c.set3=functools.partial(funab,self=c)
    c.set3()
    assert c.ab == 'funab'

    #5-----------------------------
    def funa4(self,v): self.e=v
    C.set4=funa4
    c.set4("c.set4()")  #事后给类添加，就可以
    assert c.e == "c.set4()"

    import new
    def funa6(self,v): self.e=v
    c.set6=new.instancemethod(funa6,c,C)
    c.set6("c.set6()")
    assert c.e == "c.set6()"

    def funa7(self,v): self.e=v
    c.set7=funa7.__get__(c,C)
    c.set7("c.set7()")
    assert c.e == "c.set7()"

#test_method_dynamic()
    
def test_attrib_dynamic():
    """测试类和实例的普通成员动态创建过程"""
    
    class C:
        a="class C" #这个只能用C.a来访问
        
        def __init__(self):
            self.a="Instance 1" #这个是实例命名空间的
            C.a="Class C of 1"  #这个是类命名空间的
    
    C.__dict__['aaa']=12345
    assert C.aaa == 12345

    assert C.a == "class C"
    assert C.a is C.__dict__['a']
    c=C()
    assert C.a == "Class C of 1"
    assert c.a  == "Instance 1"
    assert c.a is c.__dict__['a']
    #实例覆盖了类的同名
    
    del C.a
    try:
        C.a   #没有了
    except AttributeError as e:
        print GREEN+str(e)
    else:
        print RED+ "Test Failed 1"
        
    assert c.a == "Instance 1"

    d=C()
    d.b="New attrib"
    assert d.b=="New attrib" #可以随意动态创建一个成员

#test_attrib_dynamic()


def testwrapcount():
    '''类成员的包装'''
    class Counter:

        value = 0

        def set(self, x):
            self.value = x
            print self.value
            print Counter.value

        def up(self):
            self.value = self.value + 1
            print self.value
            print Counter.value

        def down(self):
            self.value = self.value - 1
            print self.value
            print Counter.value

    count = Counter()
    inc, dec, reset = count.up, count.down, count.set
    #这些是已经包装好的bound methond对象了，里面包装了self

    reset(1)
    inc()
    dec()
    dec()

#testwrapcount();    

def test_create_by_name():
    '''动态寻找类名字来创建'''
    class C:
        def __init__(self,a):
            self.x=a
    

    import sys
    import new
    '''
    namespace = __import__(__name__)
    '''
    
    #m=sys.modules[__name__]
    #cls= getattr(m,"C")
    #o=new.instance(cls)
    
    cls1=locals()['C']
    cls2=vars()['C']
    assert cls1 is cls2 is C
    
    c=cls1("c")
    d=cls2("d")
    
    print c
    print c.x
    print d
    print d.x
    
#testclass1()   

#这个测试并不成功：BB应该能够管住，但是没有管住。
def testslot():
    global B,BB,C,CC,D
    class B(object):
        def __init__(self,a,b):
            self.x,self.y=a,b
    
    class BB(B):
        __slots__='x','y'
        
    
    #好像就只有这一种情况能够管住
    class C(object):
        __slots__='x','y'
        
        def __init__(self,a,b):
            self.x,self.y=a,b
    
    class CC(C):
        pass
    
    #好像就只有这一种情况能够管住  
    class D(object):
        __slots__='x','y'
        
    
    D.x #通过定义__slots__，系统就会创建这个东东 member_descriptor
    
    b=B(1,2)
    bb=BB(11,22)
    c=C(10,20)
    cc=CC(10,20)
    d=D()
    d.x,d.y=100,200
    
    print b.x, bb.x, c.x, cc.x,d.x
    
    b.z=10
    bb.z=10
    cc.z=10
    try:
        c.z=10
    except AttributeError as e:
        print GREEN+str(e)
    else:
        print RED+'test failed'
        
    try:
        d.z=10
    except AttributeError as e:
        print GREEN+str(e)
    else:
        print RED+'test failed'
        
    C.z=100
    print c.z
    try:
        c.z=100
    except AttributeError as e:
        print GREEN+str(e)
        
#testslot()    
    
def testproperty():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
        def getArea(self):
            return self.width * self.height
        area = property(getArea, doc='area of the rectangle')
    
    r=Rectangle(30,40)
    assert r.area==30*40
    try:
        r.area=10
    except AttributeError as e:
        print GREEN+str(e)
    
    try:
        del r.area
    except AttributeError as e:
        print GREEN+str(e)
            
        
    class B(object):
        def f(self): return 23
        g = property(f) #这里f当作对象传递进去，所以就没有经过查找
    class C(B):
        def f(self): return 42
    c = C( )
    
    assert c.g==23 !=c.f()
    
    
    class B(object):
        def f(self): 
            return 23
        def _f(self):
            return self.f() #这里的f经过查找了。注意：method里面无法使用直接类block中定义的变量
        g = property(_f) 
    class C(B):
        def f(self): return 42
    c = C( )
    
    assert c.g==42 ==c.f()
    
    class OptimizedRectangle(Rectangle):
        __slots__ = 'width', 'height'

    opt=OptimizedRectangle(300,400)
    opt.aaa='b'
    #不成功不知为何
#testproperty()

def test_getattribe():
    class listNoAppend(list):
        def __getattribute__(self, name):
            if name == 'append': raise AttributeError, name
            return list.__getattribute__(self, name)
            
    ll=listNoAppend()
    try:
        ll.append(10)
    except AttributeError as e:
        print GREEN+str(e)
        
#test_getattribe()    

def testspecialmethods():
    def fakeGetItem(idx): return idx 
    def fakeGetItem1(self,idx): return idx 
    class Classic: pass
    c = Classic( )
    c.__getitem__ = fakeGetItem
    assert c[23]==23 #说明c[23]相当于调用c.__getitem(23)，现在是一个函数对象
    c.__getitem__ = fakeGetItem1.__get__(c,Classic)
    assert c[23]==23 #现在是一个方法了


    class NewStyle(object): pass
    n = NewStyle( )
    n.__getitem__ = fakeGetItem 
    try:
        print n[23]                       # results in:
    except TypeError as e:
        print GREEN+str(e)
    '''
    In the new-style object model, implicit use of special methods always relies on 
    the class-level binding of the special method, if any.
    '''    
    NewStyle.__getitem__=fakeGetItem1
    assert n[23]==23


def testmetaclass1():
    def __init__(self, x):
        self.x = x
 
    def printX(self):
        print self.x
     
    Test = type('Test', (object,), {'__init__': __init__, 'printX': printX})
    
    t=Test(1)
    print t.__class__
    
#testmetaclass1()    

def testsuper():
    class A(object):
        def f(self):
            self.a=1
    
    class B(A):
        pass
        
    b=B()
    super(B,b).f()
    try:
        super(B).f(b)
    except AttributeError as e:
       print RED+str(e)
    #这个不成功，不知为何
    
#testsuper()

def testmetaclass0():
    import warnings 
    class metaMetaBunch(type):
        #这个是用来创造类的
        def __new__(mcl, classname, bases, classdict):
            def __init__(self, **kw):
                for k in self.__dflts_all__: 
                    setattr(self, k, self.__dflts_all__[k])
                for k in kw: 
                    setattr(self, k, kw[k])
            
            def get_all_bases(self):
                cs=[thisclass,]
                for b in bases:
                    if getattr(b,'get_all_bases',None):
                        cs.append(b.get_all_bases(self))
                return cs    
            def __setattr__(self,name,value):
                if self.__dflts_all__.get(name,None) is None:
                    raise AttributeError, '{}.{} not exist'.format(thisclass.__name__,name)
                self.__dict__[name]=value
            def __delattr__(self,name):
                if self.__dflts_all__.get(name,None) is not None:
                    raise AttributeError, '{}.{} cannot be deleted'.format(thisclass.__name__,name)

            def __repr__(self):
                rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dflts_all__
                        if getattr(self, k) != self.__dflts_all__[k]
                      ]
                return '%s(%s)' % (classname, ', '.join(rep))
            
            def somefun(self, depth=0):
                print "{}{}.somefun({})[".format(" "*4*depth, thisclass.__name__,depth)
                try:
                    #super(thisclass,self).somefun(depth+1)
                    super(thisclass,self).somefun(depth+1)
                    #会很详尽地调用所有父类
                except AttributeError as e:
                    print " "*4*depth, GREEN+str(e)
                print "{}]".format(" "*4*depth)
                
            newdict = { #'__slots__':[  ], 
                '__dflts__':{  }, '__dflts_all__':{  },'get_all_bases':get_all_bases,
                '__setattr__':__setattr__,'__delattr__':__delattr__,'somefun':somefun,
                '__init__':__init__, '__repr__':__repr__, }
            
            if bases:
                for b in bases:
                    if getattr(b,'__dflts_all__',None):
                        newdict['__dflts_all__'].update(b.__dflts_all__)
                    
            for k in classdict:
                if k.startswith('__') and k.endswith('__'):
                    if k in newdict:
                        warnings.warn(RED+"Can't set attr [%r] in bunch-class [%r]" % (k, classname)) 
                    else:
                        newdict[k] = classdict[k]
                else:
                    #newdict['__slots__'].append(k)
                    newdict['__dflts__'][k] = classdict[k]
                newdict['__dflts_all__'].update( newdict['__dflts__'])
            
            '''
            print "\n", BLUE+classname, " : ", mcl.__name__, id(mcl)
            print "Old"
            print "\n".join(["\t{}:{}".format(a,b) for a,b in sorted(classdict.iteritems())])
            print "\nNew"
            print "\n".join(["\t{}:{}".format(a,b) for a,b in sorted(newdict.iteritems())])
            '''
            
            thisclass= super(metaMetaBunch, mcl).__new__(
                         mcl, classname, bases, newdict)
            return thisclass
    class MetaBunch(object):
        __metaclass__ = metaMetaBunch

    class Point(MetaBunch):
        x = 0.0
        y = 0.0
        #x/y 实际上被__new__给删掉了。放到了SLOTS里面。
        #因为如果有__slots__的话，多重继承会报错

    class Point3d(Point):
        z = 0.0

    class Color(MetaBunch):
        r = 0
        g = 0
        b = 0
    class Point3dColor(Point3d,Color):
        def __init__(self,x,y,z):
            self.x,self.y,self.z=x,y,z
        pass

    PPP=type('PPP',(Point3dColor,),{'a':1,})
    ppp=PPP()
    print ppp
    p3c=Point3dColor(x=1,y=2,z=3)
    print p3c

    class P2(Point):
        x=100.0

    class P3(Point):
        x=200.0

    class P3C(P2,P3,Color):pass

    p=P3C()
    print p,p.x

    from gpylib.misc import  genclassrelations, printclassmap, printclasstree
    tree=genclassrelations([P3C,Point3dColor])
    printclassmap(tree,Point,False,True)
    printclasstree(tree, P3C, True, True)

    try:
        p.aaa=100
    except AttributeError as e:
        print GREEN+str(e)
    else:
        print RED+'p.aaa=100 should raise except'
    
    p.somefun()
    ##会很详尽地调用所有父类
    
    P2.somefun(p,0)
    Point.somefun(p,0)
#testmetaclass0()

def testabc():
    from abc import ABCMeta,abstractmethod,abstractproperty
    class Foo(object):
        def __getitem__(self, index):
            pass
        def __len__(self):
            pass
        def get_iterator(self):
            return iter(self)

    class MyIterable:
        __metaclass__ = ABCMeta
        '''【1/5】一个纯虚类的5个需要学习的东东'''

        '''【2/5】'''
        @abstractmethod
        def __iter__(self):
            while False:
                yield None

        def get_iterator(self):
            return self.__iter__()

        '''【3/5】'''
        @classmethod
        def __subclasshook__(cls, C):
            #这个是object里面就有的方法, 在ABCMeta里面定义了，这里可以继续覆盖
            if cls is MyIterable:
                if any("__iter__" in B.__dict__ for B in C.__mro__):
                    return True
            return NotImplemented
            #这个返回让ABCMeta判断是否注册、是否是严格意义子类

    class MyIterable1(MyIterable):
        @classmethod
        def __subclasshook__(cls, C):
            return MyIterable.__subclasshook__(C) == True
            #这个让register失效了
    
    assert issubclass(MyIterable,object)
    '''【4/5】'''
    MyIterable.register(Foo)
    
    assert issubclass(Foo, MyIterable)
    assert isinstance(Foo(), MyIterable)

    MyIterable1.register(Foo)
    assert not issubclass(Foo, MyIterable1)
    assert not isinstance(Foo(), MyIterable1)
    
    class Foo1(MyIterable):
        def __iter__(self):
            pass
        
    assert issubclass(Foo1, MyIterable)
    assert isinstance(Foo1(), MyIterable)
    
    assert issubclass(Foo1, MyIterable1)
    assert isinstance(Foo1(), MyIterable1)
    
    class Foo3(object):
        def __iter__(self):pass
        
    assert issubclass(Foo3, MyIterable)
    assert isinstance(Foo3(), MyIterable)        
    
    assert issubclass(Foo3, MyIterable1)
    assert isinstance(Foo3(), MyIterable1)
    
    class AbcBase:
        __metaclass__ = ABCMeta
        '''【5/5】'''
        @abstractproperty
        def area(self):
            pass
    
    class AbcReal(AbcBase):
        def __init__(self,x,y):
            self.x, self.y = x, y
            
        @property
        def area(self):
            return self.x*self.y
        
    assert issubclass(AbcReal, AbcBase)
    a=AbcReal(1,2)
    assert isinstance(a, AbcBase)
    
    print a.area
    
    class AbcReal2(AbcBase):
        def _area_set(self,value):
            self.v=value
        def _area_get(self):
            return self.v
            
        area=property(_area_get,_area_set)
        #只是要求子类有这个名字即可
            
    a=AbcReal2()
    a.area = 333
    print a.area

    assert issubclass(AbcReal2, AbcBase)
    assert isinstance(a, AbcBase)
    
testabc()
