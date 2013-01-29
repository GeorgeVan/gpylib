# coding=gb2312

"""其他小工具"""

import os, time, re, itertools
from collections import defaultdict

import gpylib.misc
from gpylib.misc import GREEN,RED,BLUE,YELLOW,BWHITE,DIM
from gpylib.future import gprint

    
def runall():
    """执行一个目录下面的所有程序"""
    
    for parent, dirnames, filenames in os.walk(ur'C:\Down\360'):
        for filename in filenames:
            t = os.path.join(parent, filename)
            print t
            os.system('"%s"'% t.encode("gb2312") )
            time.sleep(3)

if __name__ == "__main__":
    pass
    #runall()
    
def fmtfilename(dir, patten, replace, test=False):
    """批量重命名某个目录下的文件"""
    
    os.chdir(dir)
    for f in os.listdir(dir):
        f1 = re.sub(patten, replace, f)
        if cmp(f, f1) != 0:
            print f+"\r\n\t\t"+f1
            if not test:
                os.rename(f, f1)

def randomwords(words):
    import random
    wl=str.split(words)
    random.shuffle(wl)
    return " ".join(wl)
                
if __name__ == "__main__":
    pass
    #print randomwords("Dark big wet long few light small dry short many tall quick soft old empty slow hard young full open fat dirty front high close thin clean back low")

    #fmtfilename(r"c:\george\coding",r"2\.5mens10e(\w)\.txt",r"2.5Men_S10E0\1.txt") 
    #fmtfilename(r"c:\down\thunder",r".*?.Two\.And\.A\.Half\.Men\.(S\d+E\d+).*?mkv",r"2.5Men_\1.mkv") 
    #fmtfilename(r"c:\gt\电影",r".*?The.Big.Bang.Theory.*?(S\d+E\d+).*?mkv",r"BBT_\1.mkv")


