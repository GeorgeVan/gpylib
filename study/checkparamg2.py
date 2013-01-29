# coding=gb2312
"""�����George�İ汾V2

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
     
    return wrapper
    
def validParam(*condvalues, **condkwvalues):
    '''��֤������װ������'''
    def vpinner(func):
        """���������ʱ�򣬵����������"""
       
        #��֤�����ֵ�
        dctValidator = _getdefargs(func,condvalues, condkwvalues)
        #���Ҳ������wrapper������ã����Ƕ���ʱ�Ĵ���ֻ���ڵ��õ�ʱ����ܷ�����
        
        varsname, kwsname = inspect.getargspec(func)[1:3]
        
        #�����������õ�ʱ�򣬻�������
        def wrapper(*values, **kwvalues):
            '''doc of wrapper'''
            #���������������ֵ�
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
    '''�����ָ�ʽ�� ���� �������ת��Ϊ��麯��'''
     
    #������int  string  Student
    if inspect.isclass(usercondition):
        return _assignName(lambda x: isinstance(x, usercondition),
                            usercondition.__name__)
    
    
    #(int, '10<x<20') (str, 'len(x)<20') (Student, 'x.age<20') (str, '/^\d+$/')
    if isinstance(usercondition, tuple): #�����tuple
        cls, condition = usercondition[:2]
        if condition is None: #��������û�С�����(int,) (str,)
            return _toStardardCondition(cls)
        
        #������ַ��������ұ�����/��ͷ�ͽ�β����������ʽ
        if cls in (str, unicode) and condition[0] == condition[-1] == '/':
            return _assignName( lambda x: (isinstance(x, cls)
                                    and re.match(condition[1:-1], x) is not None),
                                "(%s, '%s')" % (cls.__name__, condition))
        
        #�����ַ���������һ�����
        return _assignName( lambda x: isinstance(x, cls) and eval(condition),
                            "(%s, '%s')" % (cls.__name__, condition))
    
    #�������һ����������nullOk����multiType�ķ���ֵ
    return _assignName(usercondition)
 
#OK
def nullOk(cls, condition=None):
    '''�������ָ���ļ���������Խ���Noneֵ������
    nullOk(int)
    nullOk(int, '10<x<20')
    nullOk(str, '/^\d+$/')
    
    '''
    f1=_toStardardCondition((cls, condition))
    return _assignName( lambda x: x is None or f1(x),
                        "(None or %s)" % f1._ghc_name)
 
#OK 
def multiType(*conditions):
    '''�������ָ���ļ������ֻ��Ҫ��һ��ͨ��'''
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
    '''��ȡ����ʱ�ĸ�������-�жϺ������ֵ�
    '''
    
    names, varsname, kwsname = inspect.getargspec(func)[:3]
    condfuncs = map(_toStardardCondition, condvalues) #��Ϊһ������list
    condkwfuncs = dict((k, _toStardardCondition(condkwvalues[k])) #��Ϊ�ֵ� (x,�жϺ���)
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
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam��������:"%func.__name__,
        print ", ".join([c._ghc_name for c in unusedvarvalues])
        
    if repeatekeys:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam�����ظ�: "%func.__name__,
        print ", ".join(["{}={}".format(a,b._ghc_name) for a,b in repeatekeys])
    if unusedkeys:
        print colorama.Fore.YELLOW+colorama.Style.BRIGHT+"\t%s validParam��������:"%func.__name__,
        print ", ".join(["{}={}".format(a,b._ghc_name) for a,b in unusedkeys])

    return _dctArgs 
 
#===============================================================================
# ����
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
    
def _test7_george_patch(): 
    @validParam(kws=int)
    def foo7(s, **kws): pass
    _functest(foo7, True, s='a', a=1, b=2)

    @validParam(kws=int, y=str)
    def foo8(s, **kws): pass
    _functest(foo8, True, s='a', a=1, b=2)
    
def __test8_george_testme(): 
    #���*��**������д����֤������֤��Щ����������ÿ��Ԫ�أ�
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
    