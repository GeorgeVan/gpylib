#coding=gb2312
""" George's misc lib"""

import contextlib, timeit, inspect, os, hashlib, stat, re, itertools

from collections import defaultdict
import colorama

import gpylib
from gpylib.future import gprint

GREEN=colorama.Fore.GREEN+colorama.Style.BRIGHT
RED=colorama.Fore.RED+colorama.Style.BRIGHT
BLUE=colorama.Fore.BLUE+colorama.Style.BRIGHT
YELLOW=colorama.Fore.YELLOW+colorama.Style.BRIGHT
BWHITE= colorama.Back.WHITE
DIM = colorama.Style.DIM

colorama.init(autoreset=True)

def findsamefile(*dirlist):
    gprint(u"Checking the following directories:\n<>\n", u"".join(u"\t[{}]\n".format(d) for d in dirlist))
    
    sizedict, fc = defaultdict(list), 0
    for fn in itertools.chain( *(gpylib.misc.walkfiles(d, lambda x: True, True) for d in dirlist) ):
        sizedict[os.stat(fn).st_size].append( fn )
        fc += 1
    
    md5dict, mc = defaultdict(list), 0
    for f in itertools.chain( *(filter(lambda x: len(x)>1, sizedict.itervalues())) ):
        gpylib.misc.printworking()
        md5dict[gpylib.misc.getmd5(f)].append(f)
        mc+=1
    
    samefilelist = filter(lambda x: len(x)>1, md5dict.itervalues())
    gprint("\nTotal [<>] duplicate files.\n", BLUE + str(len(samefilelist)) )
    print u"\n\n\n".join("\n".join(fns) for fns in sorted(samefilelist) )
    gprint("Total [<>] files, calc md5 [<>].",BLUE+str(fc), RED+str(mc) )
        
if __name__ == "__main__":
    pass
    #findsamefile( ur'D:\Delia')
def removeallemptydir(path, verbose=False, removetrash=False):
    trashes=('^desktop\.ini$','^thumbs\.db$','^\.picasa\.ini$','^.*?\.thm$')
    result=True
    for f in os.listdir(path):
        fullname = os.path.join(path,f)
        if os.path.isfile(fullname):
            if not removetrash:
                result=False
            elif any(re.match(t,f,re.I|re.U) for t in trashes):
                try:
                    os.chmod(fullname, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
                    os.remove(fullname)
                    if verbose:
                        print GREEN+"del", fullname
                except Exception as e:
                    gprint("Cannot remove trash file [<>]: <>", fullname, RED+str(e))
                    result = False
        else:
            result = removeallemptydir(fullname, verbose, removetrash) and result

    if result:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
        try:
            os.rmdir(path)
            if verbose:
                print GREEN+"rmdir", path
        except Exception as e:
            gprint("Cannot rmdir [<>]: <>\n", path, str(e))
    
    return result
    
if __name__ == '__main__':
    pass
    #removeallemptydir(ur"d:\pic\pic_nex5", True)
    
def printworking(current=[0]):
    chars=[RED+'-',GREEN+'\\', BLUE+"|", YELLOW+'/']
    gprint("<><>", chars[current[0]],"\b")
    current[0]=(current[0]+1)%4
    
def ppdict(d,prekey=u"",postkey=u"", prevalue=u"\t",postvalue=u""):
    for k,v in d.iteritems():
        gprint(u"<><><>\n",prekey,k,postkey)
        
        if isinstance(v,list):
            for i in v:
                gprint(u"<><><>\n",prevalue, i, postvalue)
        else:
            gprint(u"<><><>\n",prevalue,v, postvalue)
    
class _getmd5(object):
    def __init__(self):
        self.cache={}
        self.reachcount=0
        
    @property
    def status(self):
        return len(self.cache), self.reachcount
    
    def __call__(self, fn):
        md5 = self.cache.get(fn,None)
        if md5 is None:
            gprint(YELLOW+"5\b")
            h = hashlib.new('md5')
            with open(fn,'rb') as f: #如果不用rb会出现重复的概率。
                h.update(f.read())
            md5 = h.hexdigest()
            self.cache[fn]=md5   
        else:
            reachcount +=1
        return md5
        
getmd5 = _getmd5()

if __name__ == '__main__':
    pass
    #gprint("MD5 Cache Size [<>], reachcount [<>]\n", *getmd5.status )

def walkfiles(path, condition=lambda x: True, debug=False,pre=""):
    for root, dirs, files in os.walk(path): 
        myfiles = filter(condition, files)
        c = len(myfiles)
        if debug and c:
            gprint("<><> [<>]\n",pre, root, BLUE+str(c) )
            
        for f in myfiles: 
            yield os.path.join(root, f)


def genclassrelations(clses):
    '''对clses的所有类，取得其上游所有类，以继承关系tuple list返回'''
    dd=set()
    def processtree(t):
        for i in t:
            if type(i) is tuple:
                c,bases=i
                dd.update({(c,b) for b in bases})
            else:
                processtree(i)
    
    for c in clses:
        processtree( inspect.getclasstree(inspect.getmro(c),True) )
        
    return dd
    
def printclasstree(tree, cls, subfirst=True, unique=True):
    '''根据类关系列表打印cls的相关类'''
    histroy=set()
    def printthis(c,depth=0):
        print (BLUE if c is cls else "")+"{}{}".format(" "*4*depth,c.__name__)
        
        if unique and c in histroy:
            return
            
        histroy.add(c)
        for (i,j) in tree:
            if subfirst and i is c:
                printthis(j,depth+1)
            elif not subfirst and j is c:
                printthis(i,depth+1)
    
    printthis(cls,0)

def printclassmap(tree, cls=None, subfirst=True, unique=False):
    '''打印和cls关联的所有class，如果是None，则全打印'''
    if cls is None:
        map=tree.copy()
    else:
        island=tree.copy()
        map={(cls,None),}
        
        def getfriends():
            foo=set()
            for (i,j) in island:
                for (x,y) in map:
                    if len( {i,j,x,y} )!=4:
                        foo.add((i,j))
                        break
            map.update(foo)
            island.difference_update(foo)
            return len(foo) == 0 or getfriends()
                
        getfriends()
        map.remove((cls,None))
    
    first=set()
    for (s,f) in map:
        first.add( s if subfirst else f)
    for (s,f) in map:
        first.difference_update({ f if subfirst else s})
    
    histroy=set()
    def printthis(c,depth=0):
        print (BLUE if c is cls else "")+"{}{}".format(" "*4*depth,c.__name__)
        
        if unique and c in histroy:
            return
        histroy.add(c)
        
        for (i,j) in tree:
            (subfirst and i is c) and printthis(j,depth+1)
            (not subfirst and j is c) and printthis(i,depth+1)
    
    for c in first:
        printthis(c,0)

def printfuncodeinfo(colorama, f):
    '''colorama is a module'''
    fcode=f.func_code
    
    print "\n",f.func_name,"()"
    print "\tco_name:\n\t\t",fcode.co_name
    print "\tco_filename:\n\t\t",fcode.co_filename
    print "\tco_consts(函数里面定义的常量):"
    for a in fcode.co_consts:
        print "\t\t", type(a), "*"*60
        print "\t\t", colorama.Fore.MAGENTA+colorama.Style.DIM+str(a)
    print "\tco_names(好像是用到的全局的类或者函数的名字):\n\t\t",fcode.co_names 
    print "\tco_varnames(普通变量名称):\n\t\t",fcode.co_varnames
    print "\tco_freevars(freevars名称):\n\t\t",fcode.co_freevars
    print "\tco_cellvars(被子函数作为freevar使用):\n\t\t",fcode.co_cellvars

@contextlib.contextmanager
def gt(s0, s1):
    """计时器
    
    usage:
            
            dosomething
            
    """
    t0 = timeit.default_timer()
    if s0 is not None:
        print s0,
    yield

    print s1.format(timeit.default_timer()-t0),

    