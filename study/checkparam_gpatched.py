# coding=gb2312
"""这个是George的注释版本和修订小BUG的版本
用于学习 http://www.cnblogs.com/huxi/archive/2011/03/31/2001522.html 
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
     
    #return wrapper
    
def validParam(*varargs, **keywords):
    '''验证参数的装饰器。
    函数定义的时候，调用这个函数
    '''
    varargs = map(_toStardardCondition, varargs) #变为一个函数list
    keywords = dict((k, _toStardardCondition(keywords[k])) #变为字典 x,判断函数
                    for k in keywords)
    
    def generator(func):
        """函数定义的时候，调用这个函数
        """

        #print "{}=[{}]".format(func.__name__,id(generator))
        
        args, varargname, kwname = inspect.getargspec(func)[:3]
        #验证函数字典
        dctValidator = _getcallargs(args, varargname, kwname,
                                    varargs, keywords,True,func)
                                    
        
        #函数真正调用的时候，会调用这个
        def wrapper(*callvarargs, **callkeywords):
            '''doc of wrapper'''
            #调用是真正参数字典
            dctCallArgs = _getcallargs(args, varargname, kwname,
                                       callvarargs, callkeywords,False,func)
             
            k, item = None, None
            try:
                for k in dctValidator:
                    if k == varargname:
                        for item in dctCallArgs[varargname]: #每个匿名参数都要遵守相同的规则
                            assert dctValidator[varargname](item)
                    elif k == kwname:
                        for item in dctCallArgs[kwname].values(): 
                            #每个命名字典参数都遵守相同的规则
                            #判断的时候，kw的参数名称并不重要
                            assert dctValidator[kwname](item)
                    else:
                        item = dctCallArgs[k]
                        assert dctValidator[k](item)
            except:
                raise ValidateException,\
                       ('%s() parameter validation fails, param: %s, value: %s(%s)'
                       % (func.func_name, k, item, item.__class__.__name__))
                       #调用父类的__init__函数
             
            return func(*callvarargs, **callkeywords)
            
        _wrapps(wrapper, func) 
        #wrapper = _wrapps(wrapper, func)
        #复制被包装函数的__module__/__name__/__doc__等。否则都变为 wrapper的了
        return wrapper
     
    return generator
 

#OK
def _toStardardCondition(usercondition):
    '''将各种格式的 单个 检查条件转换为检查函数'''
     
    #条件是int  string  Student
    if inspect.isclass(usercondition):
        f= lambda x: isinstance(x, usercondition)
        f._ghc_name=usercondition.__name__
        return f;
    
    
    #(int, '10<x<20') (str, 'len(x)<20') (Student, 'x.age<20') (str, '/^\d+$/')
    if isinstance(usercondition, (tuple, list)): #如果是tuple或者list
        cls, condition = usercondition[:2]
        if condition is None: #在例子中没有。类似(int,) (str,)
            return _toStardardCondition(cls)
        
        #如果是字符串，而且必须以/开头和结尾，则正则表达式
        if cls in (str, unicode) and condition[0] == condition[-1] == '/':
            f = lambda x: (isinstance(x, cls)
                              and re.match(condition[1:-1], x) is not None)
            f._ghc_name = "(%s, '%s')" % (cls.__name__, condition)
            return f
        
        #其余字符串，则是一个语句
        f = lambda x: isinstance(x, cls) and eval(condition)
        f._ghc_name = "(%s, '%s')" % (cls.__name__, condition)
        return f
    
    #本身就是一个函数，是nullOk或者multiType的返回值
    return usercondition
 
#OK
def nullOk(cls, condition=None):
    '''这个函数指定的检查条件可以接受None值，例如
    nullOk(int)
    nullOk(int, '10<x<20')
    nullOk(str, '/^\d+$/')
    
    '''
    f1=_toStardardCondition((cls, condition))
    f = lambda x: x is None or f1(x)
    f._ghc_name = "(None or %s)" % f1._ghc_name
    return f;
 
#OK 
def multiType(*conditions):
    '''这个函数指定的检查条件只需要有一个通过'''
    #return lambda x: any([v(x) for v in map(_toStardardCondition, conditions)])
    m = map(_toStardardCondition, conditions)
    f = lambda x: any([v(x) for v in m])
    f._ghc_name = "|".join(["{}".format(mi._ghc_name) for mi in m])
    return f
 
 
def _getcallargs(args, varargname, kwname, vl_args, vl_kws, atdef, func):
    '''获取调用时的各参数名-值的字典
    args, varargname, kwname 从函数定义中取得
        args is a list of the argument names 
        varargname and kwname are the names of the * and ** arguments or None
    vl_args, vl_kws 从validParam取得，是已经规整后的，或者是函数调用时的参数
    
    主要目的是函数定义和检查定义给对照起来。把匿名和keyword定义也给存进去
    '''
    if atdef:
        print colorama.Fore.GREEN+colorama.Style.BRIGHT+"\n\t{}{}{}".format(
                    ", ".join([i._ghc_name for i in vl_args]), 
                    ", " if len(vl_args)>0 and len(vl_kws)>0 else "",
                    ", ".join(["{}={}".format(a,b._ghc_name) for (a,b) in vl_kws.iteritems()]))
        
        print colorama.Fore.BLUE+colorama.Style.BRIGHT+"\t{}{}{}{}{}".format(
                    ", ".join(args), 
                    ", " if len(args)>0 and varargname else "",
                    "*"+varargname if varargname else "",
                    ", " if (len(args)>0 or varargname) and kwname else "",
                    "**"+kwname if kwname else "")
    
    _dctArgs = {}
    vl_args = tuple(vl_args) #复制一个新的局部变量
    vl_kws = dict(vl_kws) #复制一个新的局部变量
     
    argcount = len(args)
    vl_argcount = len(vl_args)
    callvarargs = None
    
    #如果函数定义的时候arg数目小于使用的时候的数目，
    #一般出现在调用的时候。如果出现在定义的时候，说明定义的条件有无效的
    if argcount < vl_argcount:
        for n, argname in enumerate(args):
            _dctArgs[argname] = vl_args[n]
            #有名参数
         
        callvarargs = vl_args[-(vl_argcount-argcount):]
        #原始版本是<=。如果是=，则上面的就会变为[-0:]，这个无效
        #剩下的就会和*vars和*keys对应
    else: #argcount>=vl_argcount 定义的大于等于调用的，则调用时的每个参数都是正常参数
        for n, var in enumerate(vl_args):
            _dctArgs[args[n]] = var
            #其实和上一个for是一样的
        
        if argcount>vl_argcount:
            #这部分参数可能使用了x=int 来调用的，所以从字典里面找
            for argname in args[-(argcount-vl_argcount):]:
                if argname in vl_kws:
                    _dctArgs[argname] = vl_kws.pop(argname)
         
        callvarargs = ()
        #没有无名参数的份了。
     
    if varargname is not None:
        if not atdef:
            _dctArgs[varargname] = callvarargs #原始版本只有这么一行
            callvarargs=()
        elif len(callvarargs)>0:
            _dctArgs[varargname] = callvarargs[0]
            callvarargs=callvarargs[1:]
        
        if varargname in vl_kws:
            _dctArgs[varargname] = vl_kws.pop(varargname)
        
        '''    
        print "{} x".format(atdef)
        varargname是函数定义的时候，变长匿名参数的名字
        callvarargs是一个tuple/list
        这段代码只对调用时有用或者正确
        对于验证定义，字典中应该是一个函数。所以后面通过 _dctArgs.update(vl_kws) 来打补丁，因为作者
        定义的语法是这些变长匿名参数的条件需要使用xxx=xxx的形式
        但是作者对于如下这个就要出错，因为此时 callvarargs 是()，这个不是断定函数
        出错情况：只要函数定义有 *varargs，但是在validParam中没有设定varargs=，都会出错
            @validParam(int)
            def foo5(a, *varargs): pass
            _unittest(foo5,
                      (True, 1, 2, 3, 4, 5),
                      (False, 'a', 1))
        
            @validParam()
            def foo5(*varargs): pass
            _unittest(foo5,
                      (True, 1, 2, 3, 4, 5),
                      (False, 'a', 1))
        George修改过的补丁后，就可以了。
        '''
     
    if kwname is not None:
        if not atdef:
            _dctArgs[kwname] = vl_kws #初始只有这么一行
            vl_kws={}
            #这段代码也只对调用时有用。定义参数验证时会通过后面的补丁来搞定
            #出错情况：只要函数定义有 *kws，但是在validParam中没有设定kws=，都会出错
            #原因相同
        elif len(callvarargs)>0:#George补丁
            _dctArgs[kwname] = callvarargs[0]
            callvarargs=callvarargs[1:]
        if kwname in vl_kws:
            _dctArgs[kwname] = vl_kws.pop(kwname)
    
    if len(callvarargs)>0:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam参数过多, 剩余"%func.__name__,
        print ", ".join([c._ghc_name for c in callvarargs])
        
    if len(vl_kws)>0:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam参数过多, 剩余"%func.__name__,
        print ", ".join(["{}={}".format(a,b._ghc_name) for a,b in vl_kws.iteritems()])
        #_dctArgs.update(vl_kws)
    #print _dctArgs
    #_dctArgs.update(vl_kws)
    #print _dctArgs
    #额外好处：处理重复限定的情况，用带名字的验证条件去覆盖，作者的补丁
    #如果上面两个BUG都打补丁了，就不需要了。
    '''
    if atdef:
        print "\t",
        print colorama.Fore.BLUE+colorama.Style.BRIGHT+", ".join([i._ghc_name for i in _dctArgs.itervalues()])
    '''
    return _dctArgs
 
 

 
 
#===============================================================================
# 测试
#===============================================================================

def _unittest(func, *cases):
    print
    for case in cases:
        _functest(func, *case)

def _functest(func, isCkPass, *args, **kws):
    print "\t{0}({1}{2}{3}) {4}\n\t\tTestng".format(func.__name__, 
                ", ".join((repr(i) for i in args)), 
                ", " if len(args)>0 and len(kws)>0 else "",
                ", ".join(["{}={}".format(a,repr(b)) for (a,b) in kws.iteritems()]),
                isCkPass),
    
    
    try:
        func(*args, **kws)
    except ValidateException:
        isCkPass = isCkPass==False
        
    if isCkPass:
        print "\r\t\tPassed"
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
    
def __test7_george_patch(): 
    @validParam(kws=int)
    def foo7(s, **kws): pass
    _functest(foo7, True, s='a', a=1, b=2)
    
def _main():
    from types import FunctionType
    colorama.init(autoreset=True)

    def callblock(f):
        print "\n%s()"%f.__name__
        f()

    [callblock(f) for (n,f) in sorted(globals().iteritems()) \
         if n.startswith('_test') and isinstance(f, FunctionType)]
 
if __name__ == '__main__':
    _main()
    