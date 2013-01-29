# -*- coding: UTF-8 -*-
 
'''
�˰汾ΪGeorge��С���԰汾��_test0_george��_test1_george��
������֤��BUG�Ĵ��� 

@summary: ��֤��
��ģ���ṩ��һ��װ����������֤�����Ƿ�Ϸ���ʹ�÷���Ϊ��
 
from validator import validParam, nullOk, multiType
 
@validParam(i=int)
def foo(i):
    return i+1
 
��д��֤����
 
1. ����֤���ͣ�
@validParam(type, ...)
���磺
����һ��λ�õĲ����Ƿ�Ϊint���ͣ�
@validParam(int)
�����Ϊx�Ĳ����Ƿ�Ϊint���ͣ�
@validParam(x=int)
 
��֤���������
@validParam(int, int)
ָ����������֤��
@validParam(int, s=str)
 
���*��**������д����֤������֤��Щ����ʵ�ʰ�����ÿ��Ԫ�أ�
@validParam(varargs=int)
def foo(*varargs): pass
 
@validParam(kws=int)
def foo7(s, **kws): pass
 
2. ������������֤��
@validParam((type, condition), ...)
���У�condition��һ�����ʽ�ַ�����ʹ��x���ô���֤�Ķ���
����bool(���ʽ��ֵ)�ж��Ƿ�ͨ����֤����������ʽʱ�׳��쳣����Ϊʧ�ܡ�
���磺
��֤һ��10��20֮���������
@validParam(i=(int, '10<x<20'))
��֤һ������С��20���ַ�����
@validParam(s=(str, 'len(x)<20'))
��֤һ������С��20��ѧ����
@validParam(stu=(Student, 'x.age<20'))
 
���⣬����������ַ�����condition������ʹ��б�ܿ�ͷ�ͽ�β��ʾ������ʽƥ�䡣
��֤һ����������ɵ��ַ�����
@validParam(s=(str, '/^\d*$/'))
 
3. ������֤��ʽĬ��Ϊ��ֵ��Noneʱ��֤ʧ�ܡ����None�ǺϷ��Ĳ���������ʹ��nullOk()��
nullOk()����һ����֤������Ϊ������
���磺
@validParam(i=nullOk(int))
@validParam(i=nullOk((int, '10<x<20')))
Ҳ���Լ�дΪ��
@validParam(i=nullOk(int, '10<x<20'))
 
4. ��������ж���Ϸ������ͣ�����ʹ��multiType()��
multiType()�ɽ��ܶ��������ÿ����������һ����֤������
���磺
@validParam(s=multiType(int, str))
@validParam(s=multiType((int, 'x>20'), nullOk(str, '/^\d+$/')))
 
5. ����и����ӵ���֤���󣬻����Ա�дһ��������Ϊ��֤�������롣
����������մ���֤�Ķ�����Ϊ����������bool(����ֵ)�ж��Ƿ�ͨ����֤���׳��쳣��Ϊʧ�ܡ�
���磺
def validFunction(x):
    return isinstance(x, int) and x>0
@validParam(i=validFunction)
def foo(i): pass
 
�����֤�����ȼ��ڣ�
@validParam(i=(int, 'x>0'))
def foo(i): pass
 
 
@author: HUXI
@since: 2011-3-22
@change: 
'''
 
import inspect
import re
 
class ValidateException(Exception): pass
 
 
def validParam(*varargs, **keywords):
    '''��֤������װ������'''
     
    varargs = map(_toStardardCondition, varargs)
    keywords = dict((k, _toStardardCondition(keywords[k]))
                    for k in keywords)
     
    def generator(func):
        args, varargname, kwname = inspect.getargspec(func)[:3]
        dctValidator = _getcallargs(args, varargname, kwname,
                                    varargs, keywords)
         
        def wrapper(*callvarargs, **callkeywords):
            dctCallArgs = _getcallargs(args, varargname, kwname,
                                       callvarargs, callkeywords)
             
            k, item = None, None
            try:
                for k in dctValidator:
                    if k == varargname:
                        for item in dctCallArgs[k]:
                            assert dctValidator[k](item)
                    elif k == kwname:
                        for item in dctCallArgs[k].values():
                            assert dctValidator[k](item)
                    else:
                        item = dctCallArgs[k]
                        assert dctValidator[k](item)
            except:
                raise ValidateException,\
                       ('%s() parameter validation fails, param: %s, value: %s(%s)'
                       % (func.func_name, k, item, item.__class__.__name__))
             
            return func(*callvarargs, **callkeywords)
         
        wrapper = _wrapps(wrapper, func)
        return wrapper
     
    return generator
 
 
def _toStardardCondition(condition):
    '''�����ָ�ʽ�ļ������ת��Ϊ��麯��'''
     
    if inspect.isclass(condition):
        return lambda x: isinstance(x, condition)
     
    if isinstance(condition, (tuple, list)):
        cls, condition = condition[:2]
        if condition is None:
            return _toStardardCondition(cls)
         
        if cls in (str, unicode) and condition[0] == condition[-1] == '/':
            return lambda x: (isinstance(x, cls)
                              and re.match(condition[1:-1], x) is not None)
         
        return lambda x: isinstance(x, cls) and eval(condition)
     
    return condition
 
 
def nullOk(cls, condition=None):
    '''�������ָ���ļ���������Խ���Noneֵ'''
     
    return lambda x: x is None or _toStardardCondition((cls, condition))(x)
 
 
def multiType(*conditions):
    '''�������ָ���ļ������ֻ��Ҫ��һ��ͨ��'''
     
    lstValidator = map(_toStardardCondition, conditions)
    def validate(x):
        for v in lstValidator:
            if v(x):
                return True
    return validate
 
 
def _getcallargs(args, varargname, kwname, varargs, keywords):
    '''��ȡ����ʱ�ĸ�������-ֵ���ֵ�'''
     
    dctArgs = {}
    varargs = tuple(varargs)
    keywords = dict(keywords)
     
    argcount = len(args)
    varcount = len(varargs)
    callvarargs = None
     
    if argcount <= varcount:
        for n, argname in enumerate(args):
            dctArgs[argname] = varargs[n]
         
        callvarargs = varargs[-(varcount-argcount):]
     
    else:
        for n, var in enumerate(varargs):
            dctArgs[args[n]] = var
         
        for argname in args[-(argcount-varcount):]:
            if argname in keywords:
                dctArgs[argname] = keywords.pop(argname)
         
        callvarargs = ()
     
    if varargname is not None:
        dctArgs[varargname] = callvarargs
     
    if kwname is not None:
        dctArgs[kwname] = keywords
     
    dctArgs.update(keywords)
    return dctArgs
 
 
def _wrapps(wrapper, wrapped):
    '''����Ԫ����'''
     
    for attr in ('__module__', '__name__', '__doc__'):
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in ('__dict__',):
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
     
    return wrapper
 
 
#===============================================================================
# ����
#===============================================================================
 
 
def _unittest(func, *cases):
    print "{} \n    Tesing".format(func)
    for case in cases:
        _functest(func, *case)
    print "    passed".format(func)
    
     
 
def _functest(func, isCkPass, *args, **kws):
    if isCkPass:
        func(*args, **kws)
    else:
        try:
            func(*args, **kws)
            assert False
        except ValidateException:
            pass
           
        
    
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

def _test0_george():
    @validParam(str,i=(int,"x>10")) #���� dctArgs.update(vl_kws)
    def foo1_g(i): pass
    _unittest(foo1_g, 
              (True, 11), 
              (False, 1), 
              (False, 's'), 
              (False, None))
              
def _test1_george():              
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
              
def _main():
    d = globals()
    from types import FunctionType
    print
    for f in d:
        if f.startswith('_test'):
            f = d[f]
            if isinstance(f, FunctionType):
                f()
 
if __name__ == '__main__':
    _main()