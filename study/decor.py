# coding=gb2312

'''����decoration/*args/**argv
'''

import timeit
        
# --exeTime
def exeTime1(func):
    def _wrapps(wrapper, wrapped):
        '''����Ԫ����'''
         
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
��newFunc1��ʹ����func�����Ľ��ͣ�
�հ�(closure) 
�հ��ǰ����ⲿ������ı�����������ȫ�ֱ������ĺ������󲿷�������ⲿ������ָ�����ⲿ������ 
�հ���������������������ⲿ�����еġ������������á���
���ñ�������ζ�Ű󶨵��Ǳ������������Ǳ���ʵ��ָ��Ķ���������������¸�ֵ���հ����ܷ��ʵ��Ľ����µ�ֵ�� 
�հ�ʹ������������ǿ��
��ʹ�����������뿪�ⲿ����������հ���Ȼ�ɼ����򱻰󶨵ı�����Ȼ��Ч��

�հ�����һ����Ҫ�����ԣ�ÿ��ִ�����հ����崦ʱ���ṹ��һ���µıհ���
�������ʹ�þɵıհ��󶨵ı���������ڶ��ε����ⲿ���������ġ�

http://www.cnblogs.com/huxi/archive/2011/06/18/2084316.html
'''

@exeTime1
def foo1(a,b,c,d):
    return a+b+c+d
#��Ч�� #foo1=exeTime(foo1)
 
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
��Ч��

a=exeTime(foo)(1,2,3,4,tt="Starting foo",yy="end %.3fs\n")
��Ч��

newFunc(1,2,3,4,tt="Starting foo",yy="end %.3fs\n")
��������ڵ���fooǰ������һЩ����

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
    
