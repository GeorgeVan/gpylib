# coding=gb2312
"""这个是George的版本V2

"""

import inspect
import re
import colorama

 
class ValidateException(Exception): pass
 
def _wrapps(wrapper, wrapped):
    '''复制元数据'''
     
    for attr in ('__module__', '__name__', '__doc__'):
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in ('__dict__',):
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
     
    return wrapper
    
def validParam(*condvalues, **condkwvalues):
    '''验证参数的装饰器。'''
    def vpinner(func):
        """函数定义的时候，调用这个函数"""
       
        #验证函数字典
        dctValidator = _getdefargs(func,condvalues, condkwvalues)
        #这个也可以在wrapper里面调用，但是定义时的错误只有在调用的时候才能发现了
        
        varsname, kwsname = inspect.getargspec(func)[1:3]
        
        #函数真正调用的时候，会调用这个
        def wrapper(*values, **kwvalues):
            '''doc of wrapper'''
            #调用是真正参数字典
            dctCallArgs = inspect.getcallargs(func,*values, **kwvalues)
            
            def verify(v):
                if not validation(v):
                    raise ValidateException,\
                           ('%s() param check failed: param[%s] should be [%s], now [%s]'
                           % (func.__name__, name, validation._ghc_name, repr(v)))
                
            
            for name,value in dctCallArgs.iteritems():
                validation = dctValidator.get(name,None)
                if not validation:
                    continue
                    
                if name == varsname:
                    for v in value:
                        verify(v)
                elif name == kwsname:
                    for n,v in value.iteritems():
                        name="%s.%s"%(kwsname,n)
                        verify(v)
                else:
                    verify(value)
                    
            return func(*values, **kwvalues)
            
        return _wrapps(wrapper, func) 
     
    return vpinner

def _assignName(f,n=None):
    f._ghc_name = getattr(f,"_ghc_name",None) or n or f.__name__
    return f

#OK
def _toStardardCondition(usercondition):
    '''将各种格式的 单个 检查条件转换为检查函数'''
     
    #条件是int  string  Student
    if inspect.isclass(usercondition):
        return _assignName(lambda x: isinstance(x, usercondition),
                            usercondition.__name__)
    
    
    #(int, '10<x<20') (str, 'len(x)<20') (Student, 'x.age<20') (str, '/^\d+$/')
    if isinstance(usercondition, tuple): #如果是tuple
        cls, condition = usercondition[:2]
        if condition is None: #在例子中没有。类似(int,) (str,)
            return _toStardardCondition(cls)
        
        #如果是字符串，而且必须以/开头和结尾，则正则表达式
        if cls in (str, unicode) and condition[0] == condition[-1] == '/':
            return _assignName( lambda x: (isinstance(x, cls)
                                    and re.match(condition[1:-1], x) is not None),
                                "(%s, '%s')" % (cls.__name__, condition))
        
        #其余字符串，则是一个语句
        return _assignName( lambda x: isinstance(x, cls) and eval(condition),
                            "(%s, '%s')" % (cls.__name__, condition))
    
    #本身就是一个函数，是nullOk或者multiType的返回值
    return _assignName(usercondition)
 
#OK
def nullOk(cls, condition=None):
    '''这个函数指定的检查条件可以接受None值，例如
    nullOk(int)
    nullOk(int, '10<x<20')
    nullOk(str, '/^\d+$/')
    
    '''
    f1=_toStardardCondition((cls, condition))
    return _assignName( lambda x: x is None or f1(x),
                        "(None or %s)" % f1._ghc_name)
 
#OK 
def multiType(*conditions):
    '''这个函数指定的检查条件只需要有一个通过'''
    #return lambda x: any([v(x) for v in map(_toStardardCondition, conditions)])
    m = map(_toStardardCondition, conditions)
    return _assignName( lambda x: any([v(x) for v in m]),
                    " | ".join(["{}".format(mi._ghc_name) for mi in m]))

def _assignDefNames(names,values,kwvalues):
    _dctArgs = {}
    
    if names and values:
        _dctArgs.update(zip(names,values))
    
    unusedvarvalues=None
    if values:
        unusedvarvalues = values[len(_dctArgs):]
    
    unusedkeys,repeatekeys=[],[]
    
    if kwvalues:
        kwsdict={}
        for (k,v) in kwvalues.iteritems():
            if k in names:
                if _dctArgs.get(k, None):
                    repeatekeys.append((k,v))
                else:
                    _dctArgs[k]=v
            else:
                unusedkeys.append((k,v))
        if kwsdict:
            _dctArgs[kwsname] = kwsdict
    
    return _dctArgs,unusedvarvalues,repeatekeys,unusedkeys

def _getdefargs(func, condvalues, condkwvalues):
    '''获取定义时的各参数名-判断函数的字典
    '''
    
    names, varsname, kwsname = inspect.getargspec(func)[:3]
    condfuncs = map(_toStardardCondition, condvalues) #变为一个函数list
    condkwfuncs = dict((k, _toStardardCondition(condkwvalues[k])) #变为字典 (x,判断函数)
                    for k in condkwvalues)
                    
    print colorama.Fore.GREEN+colorama.Style.BRIGHT+"\n\t{}{}{}".format(
                ", ".join([i._ghc_name for i in condfuncs]), 
                ", " if condfuncs and condkwfuncs else "",
                ", ".join(["{} = {}".format(a,b._ghc_name) for (a,b) in condkwfuncs.iteritems()]))
    

    print colorama.Fore.BLUE+colorama.Style.BRIGHT+"\t{}{}{}{}{}".format(
                ", ".join(names), 
                ", " if names and varsname else "",
                "*"+varsname if varsname else "",
                ", " if (names or varsname) and kwsname else "",
                "**"+kwsname if kwsname else "")
                
    if varsname: names.append(varsname)
    if kwsname: names.append(kwsname)
    
    _dctArgs,unusedvarvalues,repeatekeys, unusedkeys = _assignDefNames(names,condfuncs,condkwfuncs)
    
    if unusedvarvalues:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam参数过多:"%func.__name__,
        print ", ".join([c._ghc_name for c in unusedvarvalues])
        
    if repeatekeys:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam参数重复: "%func.__name__,
        print ", ".join(["{}={}".format(a,b._ghc_name) for a,b in repeatekeys])
    if unusedkeys:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam参数过多:"%func.__name__,
        print ", ".join(["{}={}".format(a,b._ghc_name) for a,b in unusedkeys])

    return _dctArgs 
 
#===============================================================================
# 测试
#===============================================================================

def _unittest(func, *cases):
    #return
    print
    for case in cases:
        _functest(func, *case)

def _functest(func, isCkPass, *argnames, **kws):
    #return
    
    print "\t{0}({1}{2}{3}) {4}\n\t\tTesting".format(
                func.__name__, 
                ", ".join((repr(i) for i in argnames)), 
                ", " if argnames and kws else "",
                ", ".join(["{}={}".format(a,repr(b)) for (a,b) in kws.iteritems()]),
                isCkPass),
    
    try:
        func(*argnames, **kws)
    except ValidateException as e:
        print e
        isCkPass = isCkPass==False
        
    if isCkPass:
        print "\r\t\tPassed "
    else:
        print colorama.Fore.RED+colorama.Style.BRIGHT+"\r\t\tFailed"
    
def _test1_simple():
    #检查第一个位置的参数是否为int类型：
    @validParam(int)
    def foo1(i): pass
    _unittest(foo1, 
              (True, 1), 
              (False, 's'), 
              (False, None))
 
    #检查名为x的参数是否为int类型：
    @validParam(x=int)
    def foo2(s, x): pass
    _unittest(foo2, 
              (True, 1, 2), 
              (False, 's', 's'))
     
    #验证多个参数：
    @validParam(int, int)
    def foo3(s, x): pass
    _unittest(foo3, 
              (True, 1, 2), 
              (False, 's', 2))
     
    #指定参数名验证：
    @validParam(int, s=str)
    def foo4(i, s): pass
    _unittest(foo4, 
              (True, 1, 'a'), 
              (False, 's', 1))
     
    #针对*和**参数编写的验证器将验证这些参数包含的每个元素：
    @validParam(varargs=int)
    def foo5(*varargs): pass
    _unittest(foo5,
              (True, 1, 2, 3, 4, 5),
              (False, 'a', 1))
     
    @validParam(kws=int)
    def foo6(**kws): pass
    _functest(foo6, True, a=1, b=2)
    _functest(foo6, False, a='a', b=2)
     
    @validParam(kws=int)
    def foo7(s, **kws): pass
    _functest(foo7, True, s='a', a=1, b=2)
 
 
def _test2_condition():
    #验证一个10到20之间的整数：
    @validParam(i=(int, '10<x<20'))
    def foo1(x, i): pass
    _unittest(foo1, 
              (True, 1, 11), 
              (False, 1, 'a'), 
              (False, 1, 1))
     
    #验证一个长度小于20的字符串：
    @validParam(s=(str, 'len(x)<20'))
    def foo2(a, s): pass
    _unittest(foo2, 
              (True, 1, 'a'), 
              (False, 1, 1), 
              (False, 1, 'a'*20))
     
    #验证一个年龄小于20的学生：
    class Student(object):
        def __init__(self, age): self.age=age
     
    @validParam(stu=(Student, 'x.age<20'))
    def foo3(stu): pass
    _unittest(foo3, 
              (True, Student(18)), 
              (False, 1), 
              (False, Student(20)))
     
    #验证一个由数字组成的字符串：
    @validParam(s=(str, r'/^\d*$/'))
    def foo4(s): pass
    _unittest(foo4, 
              (True, '1234'), 
              (False, 1), 
              (False, 'a1234'))
 
 
def _test3_nullok():
    @validParam(i=nullOk(int))
    def foo1(i): pass
    _unittest(foo1, 
              (True, 1), 
              (False, 'a'), 
              (True, None))
     
    @validParam(i=nullOk(int, '10<x<20'))
    def foo2(i): pass
    _unittest(foo2, 
              (True, 11), 
              (False, 'a'), 
              (True, None), 
              (False, 1))
 
 
def _test4_multitype():
    @validParam(s=multiType(int, str))
    def foo1(s): pass
    _unittest(foo1, 
              (True, 1),
              (True, 'a'),
              (False, None),
              (False, 1.1))
     
    @validParam(s=multiType((int, 'x>20'), nullOk(str, '/^\d+$/')))
    def foo2(s): pass
    _unittest(foo2, 
              (False, 1),
              (False, 'a'),
              (True, None),
              (False, 1.1),
              (True, 21),
              (True, '21'))

def _test5_george():
    @validParam(str,i=(int,"x>10")) #测试 dctArgs.update(vl_kws)
    def foo1_g(i): pass
    _unittest(foo1_g, 
              (True, 11), 
              (True, 1), 
              (False, 's'), 
              (False, None))
              
    #指定参数名验证：
    @validParam(int, str, str)
    def foo4(i, s): pass
    _unittest(foo4, 
              (True, 1, 'a'), 
              (False, 's', 1))
              
def _test6_george_patch():              
    @validParam()
    def foo51(*varargs): pass
    _unittest(foo51,
              (True, 1, 2, 3, 4, 5),
              (True, 'a', 1))
     
    @validParam(int)
    def foo52(*varargs): pass
    _unittest(foo52,
              (True, 1, 2, 3, 4, 5),
              (False, 'a', 1))
              
    @validParam(str,int)
    def foo53(a,*varargs): pass
    _unittest(foo53,
              (True, "x", 1, 2, 3, 4, 5),
              (True, 1, 2, 3, 4, 5),
              (False, 'x', 1, 2, 'y', 4, 5),
              (True, 'a', 1))
              
    @validParam(int)
    def foo6(**kws): pass
    print
    _functest(foo6, True, a=1, b=2)
    _functest(foo6, False, a='a', b=2)
     
    @validParam(str, int)
    def foo7(s, **kws): pass
    print
    _functest(foo7, True, s='a', a=1, b=2)

    @validParam(str, str, int, int)
    def foo8(s, *varargs, **kws): pass
    print
    _functest(foo8, True, s='a', a=1, b=2)
    _functest(foo8, False, 'a', 1, 2, 3, a=1, b=2)
    _functest(foo8, True, 'a', "1", "2", "3", a=1, b=2)
    _functest(foo8, False, 'a', "1", "2", "3", a="1", b=2)
    
def _test7_george_patch(): 
    @validParam(kws=int)
    def foo7(s, **kws): pass
    _functest(foo7, True, s='a', a=1, b=2)

    @validParam(kws=int, y=str)
    def foo8(s, **kws): pass
    _functest(foo8, True, s='a', a=1, b=2)
    
def __test8_george_testme(): 
    #针对*和**参数编写的验证器将验证这些参数包含的每个元素：
    @validParam(varargs=int)    
    def foo5(*varargs): pass
    _unittest(foo5,
              (True, 1, 2, 3, 4, 5),
              (False, 'a', 1))
        
def _main():
    colorama.init(autoreset=True)

    def callblock(f):
        print "\n%s()"%f.__name__
        f()

    from types import FunctionType
    [callblock(f) for (n,f) in sorted(globals().iteritems()) \
         if n.startswith('_test') and isinstance(f, FunctionType)]
 
if __name__ == '__main__':
    _main()
    