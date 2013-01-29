#coding=gb2312

'''����ѧϰpipe���ԭ��'''

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

    ���ԣ� abc | pipeg_instance �Ľ������pipeg_instance.__ror__(abc)
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
    #map����

class pipegx(pipeg):
    def __call__(self, *args, **kwargs):
        return pipegx(lambda x: self.function(x, *args, **kwargs))
    #����������õ�ʱ����û��iterator�ģ�
    #���ص��¶���ĺ���ȴֻ����iterator���൱������һ��ƫ����

@pipegx
def concatx(iterable, separator=", "):
    return separator.join(map(str,iterable))        
 
@pipegx
def addx(x):
    return sum(x)
 
@pipegx
def procstr(s,s1):
    return s+s1
#pipe ���Դ���iterable�Ķ�����Ҳ���Դ���һ��Ķ�������ȫ��ʵ�ֺ������

def mypipetest():  
    print "\ntest1"    
    print [1,2,3] | add     # �൱�ڵ��� add_func([1,2,3])�����func�����ڣ�ֻ�Ǽ������
                            # add��һ������pipeg(add_fun).__ror___([1,2,3])

    print "\ntest1-1"
    try:
        print [1,2,3] | add() #AttributeError: pipeg instance has no __call__ method
                               #�൱�ڵ��� pipeg(add_fun).__call___()
                               #����pipegû��ʵ��__call__�����Ծͱ�����
    except AttributeError as e:
        print "error: %s" % e

    print "\ntest1-2"    
    print [1,2,3] | addx()

                            
    print "\ntest2"
    print [1,2,3] | as_list # �൱�ڵ��� as_list_func([1,2,3])

    print "\ntest3"
    print [1,2,3] | concat # �൱�ڵ��� concat_func([1,2,3])

    print "\ntest4"
    print [1,2,3] | concatx("|")

    print "\ntest5"
    print [1,2,3] | concatx.__call__("||") 

    p1=concatx.__call__("|||") 
        #����������ص�pipegx�����е�ִ�к����� f(x): concat_func(x,"!")��Ҳ����concat_func��ƫ����

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
pipe a|b|c|d �൱�� d(c(b(a)))
add/stdout�Ⱦ��ǰ���ߵĶ�������һ�����������
as_list���ǰ���ߵĶ�������iterable������
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
    #���һ�����None����Ϊ��һ��stdoutʵ������һ��������û�з���ֵ
    
    print "\n\nTest5"    
    xrange(5) | pipe.as_list | pipe.stdout
    
    print "\n\nTest6"    
    xrange(5) | stdoutall(":")
    
    print "\n\nTest7"    
    xrange(5) | pipe.concat(";") | pipe.stdout
    
if __name__ == '__main__':
    mypipetest()
    pubpipetest()


    
    
    