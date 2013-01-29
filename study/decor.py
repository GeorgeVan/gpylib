# coding=gb2312

'''测试decoration/*args/**argv
'''

import timeit
        
# --exeTime
def exeTime1(func):
    def _wrapps(wrapper, wrapped):
        '''复制元数据'''
         
        for attr in ('__module__', '__name__', '__doc__'):
            setattr(wrapper, attr, getattr(wrapped, attr))
        for attr in ('__dict__',):
            getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
         
        return wrapper
        
    def newFunc1(*args, **args2):
        t0 = timeit.default_timer()
        #print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
        print args2['tt'],
        del args2['tt']
        yy=args2['yy']
        del args2['yy']
        r = func(*args, **args2)
        #print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
        #print "%r(%r, %r) %.3fs %s" % (func.__name__, args, args2 ,timeit.default_timer()-t0,yy),
        print yy%(timeit.default_timer()-t0),
        return r
        
    return _wrapps(newFunc1,func)
# --end of exeTime

'''
在newFunc1中使用了func变量的解释：
闭包(closure) 
闭包是绑定了外部作用域的变量（但不是全局变量）的函数。大部分情况下外部作用域指的是外部函数。 
闭包包含了自身函数体和所需外部函数中的“变量名的引用”。
引用变量名意味着绑定的是变量名，而不是变量实际指向的对象；如果给变量重新赋值，闭包中能访问到的将是新的值。 
闭包使函数更加灵活和强大。
即使程序运行至离开外部函数，如果闭包仍然可见，则被绑定的变量仍然有效；

闭包还有一个重要的特性，每次执行至闭包定义处时都会构造一个新的闭包，
这个特性使得旧的闭包绑定的变量不会随第二次调用外部函数而更改。

http://www.cnblogs.com/huxi/archive/2011/06/18/2084316.html
'''

@exeTime1
def foo1(a,b,c,d):
    return a+b+c+d
#等效于 #foo1=exeTime(foo1)
 
def test1(): 
    a=foo1(1,2,3,4,tt="Starting foo1",yy="end %.3fs\n")
    print a


def foo2(a,b,c,d):
    return a+b+c+d
 
def test2(): 
    a=exeTime1(foo2)(1,2,3,4,tt="Starting foo2",yy="end %.3fs\n")
    print a


'''

a=foo(1,2,3,4,tt="Starting foo",yy="end %.3fs\n")
等效于

a=exeTime(foo)(1,2,3,4,tt="Starting foo",yy="end %.3fs\n")
等效于

newFunc(1,2,3,4,tt="Starting foo",yy="end %.3fs\n")
这个函数在调用foo前后做了一些事情

'''

def exeTime3(func):
    def newFunc3((tt,yy),*args, **args2):
        print tt,

        t0 = timeit.default_timer()
        r = func(*args, **args2)
        print yy%(timeit.default_timer()-t0),

        return r
    return newFunc3
# --end of exeTime

@exeTime3
def foo3(a,b,c,d):
    return a+b+c+d
 
def test3(): 
    a=foo3(("Starting foo3","end %.3fs\n"),1,2,3,4)
    print a



def exeTime4((tt,yy),func):
    def newFunc4(*args, **args2):
        print tt,

        t0 = timeit.default_timer()
        r = func(*args, **args2)
        print yy%(timeit.default_timer()-t0),

        return r
    return newFunc4
# --end of exeTime

def foo4(a,b,c,d):
    return a+b+c+d
 
def test4():
    a=exeTime4(("Starting foo4","end %.3fs\n"),foo4)(1,2,3,4)
    print a



def exeTime5((ii,yy),func):
    def newFunc5(*args, **args2):
        print "Starting %s(%s)"%(func.__name__,",".join([str(args[i]) for i in ii])),

        t0 = timeit.default_timer()
        r = func(*args, **args2)
        print yy%(timeit.default_timer()-t0),

        return r
    return newFunc5
# --end of exeTime

def foo5(a,b,c,d):
    return a+b+c+d
 
def test5():
    a=exeTime5(([0],"%.3fs\n"),foo5)(1,2,3,4)
    print a


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    
    print foo1.func_name
    print foo2.func_name
    print foo3.func_name
    
