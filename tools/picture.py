# coding=gb2312

"""拼接图像
一般情况下，使用主函数grouppiccurdircmdline就行
"""

import os
import sys
import time
import re
import codecs
import Image
from gpylib.misc import gt,GREEN
from gpylib.future import gprint
#需要将gpylib安装，或者把路径添加到PYTHONPATH上

def fitpic(image1, (dstw, dsth), best):
    """翻转、放大、切边
    
    """
    
    image = image1
    (w, h) = image.size

    if (w-h)*(dstw-dsth) < 0:
        image = image.rotate(90)
        (w, h) = (h, w)

    if float(w)/h > float(dstw)/dsth:  # 宽度过大
        (w1, h1) = (int(float(w)*dsth/h), dsth)  # 缩放到目标高度
        crop = ((w1-dstw)/2, 0, (w1-dstw)/2+dstw, dsth) #剪切两边
    else:  #高度过大
        (w1, h1) = (dstw, int(float(h)*dstw/w))  #缩放到目标宽度
        crop = (0, (h1-dsth)/2, dstw, (h1-dsth)/2+dsth) #剪切上下

    #image=image.resize((w1,h1),Image.ANTIALIAS if best else Image.NEAREST)
    exec "image=image.resize((w1,h1)" + (", Image.ANTIALIAS)" if best else ")")
    image = image.crop(crop) #剪切多余的宽

    return image

def grouppic(files, f, dstw, dsth, margin, best):
    """拼接图像2*2
    
    """

    if len(files) != 4:
        print "Warning: must have 4 files now[%d]" % (len(files))
        return

    print "{\n" + "\n".join(files) + "\n} >> %s [%d*%d]\n" % (f, dstw*2 , dsth*2)

    with gt(None, "\nsum{:.3f}秒\n"):
        target = Image.new("RGB", (dstw*2, dsth*2), (255, 255, 255))

        pos = ((0, 0), (dstw+margin, 0), (0, dsth+margin), (dstw+margin, dsth+margin))
        for i in xrange(4):
            with gt("[%s]\nLoading ..." % files[i], " {:.3f}秒\n"):
                image = Image.open(files[i])
                image.load()

            with gt("fitting...", "{:.1f}秒\n"):
                image = fitpic(image, (dstw-margin/2, dsth-margin/2), best)

            with gt("pasting...", "{:.3f}秒\n\n"):
                target.paste(image, pos[i])

        with gt("saving...", "{:.1f}秒\n"):
            if best:
                target.save(f, quality=100) #时间增加不了多少
            else:
                target.save(f)

        with gt("thumbnail...", "{:.3f}秒\n"):
            target.thumbnail((1000, 1000))


    target.show()


def grouppicdir(dir, dst, best=True, dstw=2970, dsth=2100, margin=20):
    """拼接某个目录下的jpg
    
    """

    gprint(u"组合照片 [<>] [<>]\n\n", dir, GREEN+"Best" if best else "") 
    (dd, df) = os.path.split(dst)
    if not df.startswith("_"):
        print "[%s] must start with _"%df
        return

    files = [os.path.join(dir, f) for f in os.listdir(dir) if re.match(r"[^_].+\.jpg",f,re.I) != None]
    grouppic(files, dst, dstw, dsth, margin, best)


def grouppiccurdir(best):
    """拼接当前目录下的jpg
    
    """

    grouppicdir(os.curdir, os.path.join(os.curdir, "_result.jpg"), best)

if __name__ == "__main__":
    grouppiccurdircmdline(len(sys.argv)> 1 and sys.argv[1] == "1")

    #grouppiccurdir(True)
    #grouppiccurdir(False)
    #grouppicdir(r"c:\gt",r"c:\gt\result.png")
    #grouppic((r"c:\gt\a.jpg",r"c:\gt\b.jpg",r"c:\gt\c.jpg",r"c:\gt\d.jpg"),r"c:\gt\result.png",5940,4200)


