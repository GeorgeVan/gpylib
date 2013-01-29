#coding=gb2312
""" George's misc lib"""
from __future__ import print_function
#from gpylib.misc import GREEN,RED,BLUE,YELLOW

def gprint(format, *args):
    '''gprint("something __ is __ is __dddd\n",RED+"1", BLUE+"2", YELLOW+"3")
    gprint("/_/_something __ is __ is __\n",RED+"1", BLUE+"2", YELLOW+"3")
    '''
    pargs=[]
    for a in args:
        i=format.find('<>')
        if i==-1:
            return
        pargs.extend([format[:i],a])
        format=format[i+2:]
    pargs.append(format)
    print(*pargs,sep='',end='')

if __name__ == '__main__':
    pass
    #gprint("something <> is <> is <>dddd\n",RED+"1", BLUE+"2", YELLOW+"3")
    #gprint("<>something <> is <> is <>\n",RED+"1", BLUE+"2", YELLOW+"3")
