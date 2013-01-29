# coding=gb2312
"""�����George��ע�Ͱ汾���޶�СBUG�İ汾
����ѧϰ http://www.cnblogs.com/huxi/archive/2011/03/31/2001522.html 
"""

import inspect
import re
import colorama 

 
class ValidateException(Exception): pass
 
def _wrapps(wrapper, wrapped):
    '''����Ԫ����'''
     
    for attr in ('__module__', '__name__', '__doc__'):
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in ('__dict__',):
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
     
    #return wrapper
    
def validParam(*varargs, **keywords):
    '''��֤������װ������
    ���������ʱ�򣬵����������
    '''
    varargs = map(_toStardardCondition, varargs) #��Ϊһ������list
    keywords = dict((k, _toStardardCondition(keywords[k])) #��Ϊ�ֵ� x,�жϺ���
                    for k in keywords)
    
    def generator(func):
        """���������ʱ�򣬵����������
        """

        #print "{}=[{}]".format(func.__name__,id(generator))
        
        args, varargname, kwname = inspect.getargspec(func)[:3]
        #��֤�����ֵ�
        dctValidator = _getcallargs(args, varargname, kwname,
                                    varargs, keywords,True,func)
                                    
        
        #�����������õ�ʱ�򣬻�������
        def wrapper(*callvarargs, **callkeywords):
            '''doc of wrapper'''
            #���������������ֵ�
            dctCallArgs = _getcallargs(args, varargname, kwname,
                                       callvarargs, callkeywords,False,func)
             
            k, item = None, None
            try:
                for k in dctValidator:
                    if k == varargname:
                        for item in dctCallArgs[varargname]: #ÿ������������Ҫ������ͬ�Ĺ���
                            assert dctValidator[varargname](item)
                    elif k == kwname:
                        for item in dctCallArgs[kwname].values(): 
                            #ÿ�������ֵ������������ͬ�Ĺ���
                            #�жϵ�ʱ��kw�Ĳ������Ʋ�����Ҫ
                            assert dctValidator[kwname](item)
                    else:
                        item = dctCallArgs[k]
                        assert dctValidator[k](item)
            except:
                raise ValidateException,\
                       ('%s() parameter validation fails, param: %s, value: %s(%s)'
                       % (func.func_name, k, item, item.__class__.__name__))
                       #���ø����__init__����
             
            return func(*callvarargs, **callkeywords)
            
        _wrapps(wrapper, func) 
        #wrapper = _wrapps(wrapper, func)
        #���Ʊ���װ������__module__/__name__/__doc__�ȡ����򶼱�Ϊ wrapper����
        return wrapper
     
    return generator
 

#OK
def _toStardardCondition(usercondition):
    '''�����ָ�ʽ�� ���� �������ת��Ϊ��麯��'''
     
    #������int  string  Student
    if inspect.isclass(usercondition):
        f= lambda x: isinstance(x, usercondition)
        f._ghc_name=usercondition.__name__
        return f;
    
    
    #(int, '10<x<20') (str, 'len(x)<20') (Student, 'x.age<20') (str, '/^\d+$/')
    if isinstance(usercondition, (tuple, list)): #�����tuple����list
        cls, condition = usercondition[:2]
        if condition is None: #��������û�С�����(int,) (str,)
            return _toStardardCondition(cls)
        
        #������ַ��������ұ�����/��ͷ�ͽ�β����������ʽ
        if cls in (str, unicode) and condition[0] == condition[-1] == '/':
            f = lambda x: (isinstance(x, cls)
                              and re.match(condition[1:-1], x) is not None)
            f._ghc_name = "(%s, '%s')" % (cls.__name__, condition)
            return f
        
        #�����ַ���������һ�����
        f = lambda x: isinstance(x, cls) and eval(condition)
        f._ghc_name = "(%s, '%s')" % (cls.__name__, condition)
        return f
    
    #�������һ����������nullOk����multiType�ķ���ֵ
    return usercondition
 
#OK
def nullOk(cls, condition=None):
    '''�������ָ���ļ���������Խ���Noneֵ������
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
    '''�������ָ���ļ������ֻ��Ҫ��һ��ͨ��'''
    #return lambda x: any([v(x) for v in map(_toStardardCondition, conditions)])
    m = map(_toStardardCondition, conditions)
    f = lambda x: any([v(x) for v in m])
    f._ghc_name = "|".join(["{}".format(mi._ghc_name) for mi in m])
    return f
 
 
def _getcallargs(args, varargname, kwname, vl_args, vl_kws, atdef, func):
    '''��ȡ����ʱ�ĸ�������-ֵ���ֵ�
    args, varargname, kwname �Ӻ���������ȡ��
        args is a list of the argument names 
        varargname and kwname are the names of the * and ** arguments or None
    vl_args, vl_kws ��validParamȡ�ã����Ѿ�������ģ������Ǻ�������ʱ�Ĳ���
    
    ��ҪĿ���Ǻ�������ͼ�鶨���������������������keyword����Ҳ�����ȥ
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
    vl_args = tuple(vl_args) #����һ���µľֲ�����
    vl_kws = dict(vl_kws) #����һ���µľֲ�����
     
    argcount = len(args)
    vl_argcount = len(vl_args)
    callvarargs = None
    
    #������������ʱ��arg��ĿС��ʹ�õ�ʱ�����Ŀ��
    #һ������ڵ��õ�ʱ����������ڶ����ʱ��˵���������������Ч��
    if argcount < vl_argcount:
        for n, argname in enumerate(args):
            _dctArgs[argname] = vl_args[n]
            #��������
         
        callvarargs = vl_args[-(vl_argcount-argcount):]
        #ԭʼ�汾��<=�������=��������ľͻ��Ϊ[-0:]�������Ч
        #ʣ�µľͻ��*vars��*keys��Ӧ
    else: #argcount>=vl_argcount ����Ĵ��ڵ��ڵ��õģ������ʱ��ÿ������������������
        for n, var in enumerate(vl_args):
            _dctArgs[args[n]] = var
            #��ʵ����һ��for��һ����
        
        if argcount>vl_argcount:
            #�ⲿ�ֲ�������ʹ����x=int �����õģ����Դ��ֵ�������
            for argname in args[-(argcount-vl_argcount):]:
                if argname in vl_kws:
                    _dctArgs[argname] = vl_kws.pop(argname)
         
        callvarargs = ()
        #û�����������ķ��ˡ�
     
    if varargname is not None:
        if not atdef:
            _dctArgs[varargname] = callvarargs #ԭʼ�汾ֻ����ôһ��
            callvarargs=()
        elif len(callvarargs)>0:
            _dctArgs[varargname] = callvarargs[0]
            callvarargs=callvarargs[1:]
        
        if varargname in vl_kws:
            _dctArgs[varargname] = vl_kws.pop(varargname)
        
        '''    
        print "{} x".format(atdef)
        varargname�Ǻ��������ʱ�򣬱䳤��������������
        callvarargs��һ��tuple/list
        ��δ���ֻ�Ե���ʱ���û�����ȷ
        ������֤���壬�ֵ���Ӧ����һ�����������Ժ���ͨ�� _dctArgs.update(vl_kws) ���򲹶�����Ϊ����
        ������﷨����Щ�䳤����������������Ҫʹ��xxx=xxx����ʽ
        �������߶������������Ҫ������Ϊ��ʱ callvarargs ��()��������Ƕ϶�����
        ���������ֻҪ���������� *varargs��������validParam��û���趨varargs=���������
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
        George�޸Ĺ��Ĳ����󣬾Ϳ����ˡ�
        '''
     
    if kwname is not None:
        if not atdef:
            _dctArgs[kwname] = vl_kws #��ʼֻ����ôһ��
            vl_kws={}
            #��δ���Ҳֻ�Ե���ʱ���á����������֤ʱ��ͨ������Ĳ������㶨
            #���������ֻҪ���������� *kws��������validParam��û���趨kws=���������
            #ԭ����ͬ
        elif len(callvarargs)>0:#George����
            _dctArgs[kwname] = callvarargs[0]
            callvarargs=callvarargs[1:]
        if kwname in vl_kws:
            _dctArgs[kwname] = vl_kws.pop(kwname)
    
    if len(callvarargs)>0:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam��������, ʣ��"%func.__name__,
        print ", ".join([c._ghc_name for c in callvarargs])
        
    if len(vl_kws)>0:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam��������, ʣ��"%func.__name__,
        print ", ".join(["{}={}".format(a,b._ghc_name) for a,b in vl_kws.iteritems()])
        #_dctArgs.update(vl_kws)
    #print _dctArgs
    #_dctArgs.update(vl_kws)
    #print _dctArgs
    #����ô��������ظ��޶���������ô����ֵ���֤����ȥ���ǣ����ߵĲ���
    #�����������BUG���򲹶��ˣ��Ͳ���Ҫ�ˡ�
    '''
    if atdef:
        print "\t",
        print colorama.Fore.BLUE+colorama.Style.BRIGHT+", ".join([i._ghc_name for i in _dctArgs.itervalues()])
    '''
    return _dctArgs
 
 

 
 
#===============================================================================
# ����
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
    #����һ��λ�õĲ����Ƿ�Ϊint���ͣ�
    @validParam(int)
    def foo1(i): pass
    _unittest(foo1, 
              (True, 1), 
              (False, 's'), 
              (False, None))
 
    #�����Ϊx�Ĳ����Ƿ�Ϊint���ͣ�
    @validParam(x=int)
    def foo2(s, x): pass
    _unittest(foo2, 
              (True, 1, 2), 
              (False, 's', 's'))
     
    #��֤���������
    @validParam(int, int)
    def foo3(s, x): pass
    _unittest(foo3, 
              (True, 1, 2), 
              (False, 's', 2))
     
    #ָ����������֤��
    @validParam(int, s=str)
    def foo4(i, s): pass
    _unittest(foo4, 
              (True, 1, 'a'), 
              (False, 's', 1))
     
    #���*��**������д����֤������֤��Щ����������ÿ��Ԫ�أ�
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
    #��֤һ��10��20֮���������
    @validParam(i=(int, '10<x<20'))
    def foo1(x, i): pass
    _unittest(foo1, 
              (True, 1, 11), 
              (False, 1, 'a'), 
              (False, 1, 1))
     
    #��֤һ������С��20���ַ�����
    @validParam(s=(str, 'len(x)<20'))
    def foo2(a, s): pass
    _unittest(foo2, 
              (True, 1, 'a'), 
              (False, 1, 1), 
              (False, 1, 'a'*20))
     
    #��֤һ������С��20��ѧ����
    class Student(object):
        def __init__(self, age): self.age=age
     
    @validParam(stu=(Student, 'x.age<20'))
    def foo3(stu): pass
    _unittest(foo3, 
              (True, Student(18)), 
              (False, 1), 
              (False, Student(20)))
     
    #��֤һ����������ɵ��ַ�����
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
    @validParam(str,i=(int,"x>10")) #���� dctArgs.update(vl_kws)
    def foo1_g(i): pass
    _unittest(foo1_g, 
              (True, 11), 
              (True, 1), 
              (False, 's'), 
              (False, None))
              
    #ָ����������֤��
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
    