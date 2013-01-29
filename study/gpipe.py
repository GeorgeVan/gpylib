#coding=gb2312

'''用于学习pipe库的原理'''

class pipeg:
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return self.function(other)
    """
    These functions are only called if the left operand does not support the corresponding operation 
    and the operands are of different types. 
    For instance, to evaluate the expression x - y, 
    where y is an instance of a class that has an __rsub__() method, 
    y.__rsub__(x) is called if x.__sub__(y) returns NotImplemented.

    所以， abc | pipeg_instance 的结果就是pipeg_instance.__ror__(abc)
    """
        
@pipeg
def add(x):
    return sum(x)
    
@pipeg
def as_list(iterable):
    return list(iterable)

    
@pipeg
def concat(iterable, separator=", "):
    return separator.join(map(str,iterable))
    #map函数

class pipegx(pipeg):
    def __call__(self, *args, **kwargs):
        return pipegx(lambda x: self.function(x, *args, **kwargs))
    #这个函数调用的时候，是没有iterator的；
    #返回的新对象的函数却只接受iterator，相当于做了一个偏函数

@pipegx
def concatx(iterable, separator=", "):
    return separator.join(map(str,iterable))        
 
@pipegx
def addx(x):
    return sum(x)
 
@pipegx
def procstr(s,s1):
    return s+s1
#pipe 可以处理iterable的东东，也可以处理一般的东东，完全看实现函数如何

def mypipetest():  
    print "\ntest1"    
    print [1,2,3] | add     # 相当于调用 add_func([1,2,3])，这个func不存在，只是假设而已
                            # add是一个对象，pipeg(add_fun).__ror___([1,2,3])

    print "\ntest1-1"
    try:
        print [1,2,3] | add() #AttributeError: pipeg instance has no __call__ method
                               #相当于调用 pipeg(add_fun).__call___()
                               #但是pipeg没有实现__call__，所以就报错了
    except AttributeError as e:
        print "error: %s" % e

    print "\ntest1-2"    
    print [1,2,3] | addx()

                            
    print "\ntest2"
    print [1,2,3] | as_list # 相当于调用 as_list_func([1,2,3])

    print "\ntest3"
    print [1,2,3] | concat # 相当于调用 concat_func([1,2,3])

    print "\ntest4"
    print [1,2,3] | concatx("|")

    print "\ntest5"
    print [1,2,3] | concatx.__call__("||") 

    p1=concatx.__call__("|||") 
        #这个函数返回的pipegx对象中的执行函数是 f(x): concat_func(x,"!")，也就是concat_func的偏函数

    print "\ntest6"
    print p1.__ror__([1,2,3])

    print "\ntest7"
    print [1,2,3] | p1

    print "\ntest8"
    try:
        print [1,2,3] | concat("|") #AttributeError: pipeg instance has no __call__ method
    except AttributeError as e:
        print "error: %s" % e
        
    print "\ntest9"
    print "a" | procstr("1") | procstr("2") | procstr("3")

    
import pipe

@pipe.Pipe
def stdoutall(iterable,s):
    print s.join(map(str,iterable))
'''
pipe a|b|c|d 相当于 d(c(b(a)))
add/stdout等就是把左边的东东当作一般对象来处理
as_list就是把左边的东西当作iterable来处理
'''

def pubpipetest():
    print "\n\n\nPipe Test\nTest1"
    print range(5) | pipe.add   
        # pipe.Pipe(add).__ror__(range(5))
    
    print "\n\nTest2"
    print xrange(5) | pipe.add
    
    print "\n\nTest3"    
    xrange(5) | pipe.stdout 
    
    print "\n\nTest4"    
    xrange(5) | pipe.stdout| pipe.stdout 
    #最后一个输出None，因为第一个stdout实际上是一个函数，没有返回值
    
    print "\n\nTest5"    
    xrange(5) | pipe.as_list | pipe.stdout
    
    print "\n\nTest6"    
    xrange(5) | stdoutall(":")
    
    print "\n\nTest7"    
    xrange(5) | pipe.concat(";") | pipe.stdout
    
if __name__ == '__main__':
    mypipetest()
    pubpipetest()


    
    
    