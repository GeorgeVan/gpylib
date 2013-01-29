# coding=gb2312

"""�����Ӱ��Ļ��

"""

import re, codecs
import chardet, pipe

def formatengsrt(input, output):
    """Converts english srt file to plain txt file to easy human reading.
    
    Support all encoding.
    
    """
    
    p = ( (r"-=.*?=-\s+", "", re.U), #���� ==http://a.b.c/=- ɾ��
        (r"<.*?>", "", re.U), #���� <...> ɾ��
        (r"^[\s\d\-:>,]*[\r\n]+", r"", re.M|re.U), #'-'�������ַ�
        (r"(\S+)\s+$", r"\1", re.M|re.U), #ɾ����β�Ŀ����ַ�
        (r"\.{3}[\r\n]+([a-z])", r" \1", re.U), #��β��...�ģ���һ�п�ʼ��һ��Сд��ĸ�ġ�
        (r"([^\.?!])[\r\n]+", r"\1 ", re.U), #��βû�� .?!�ģ���ӿո�ȥ���س�����
        (r"(\w+)[,.?!](\w)", r"\1, \2", re.U), #��Щ���ʺ󶺺ź���û�пո񣬼���
      )

    d = chardet.detect(open(input, "r").read())
    print "[%s] �Զ����Ϊ %s" %(input, d)

    with codecs.open(input, encoding=d['encoding'], mode='r') as fi:
        t = fi.read()
   
    for a, b, c in p:
        t = re.sub(a, b, t, 0, c)

    with codecs.open(output, encoding=d['encoding'], mode='w') as fo:
        fo.write(t)
        print "[{}] compeleted.".format(output)


if __name__ == "__main__":
    print formatengsrt.__doc__
    formatengsrt("The.Big.Bang.Theory.S01E01.720p.HDTV.x264-CTU.en.srt", "BBT_S01E01.txt")

    #fmtfilename(r"c:\george\coding",r"2\.5mens10e(\w)\.txt",r"2.5Men_S10E0\1.txt") 
    #fmtfilename(r"c:\down\thunder",r".*?.Two\.And\.A\.Half\.Men\.(S\d+E\d+).*?mkv",r"2.5Men_\1.mkv") 
    #fmtfilename(r"c:\gt\��Ӱ",r".*?The.Big.Bang.Theory.*?(S\d+E\d+).*?mkv",r"BBT_\1.mkv")


'''
���·���
'''












#formatsrt3u("The.Big.Bang.Theory.S01E01.720p.HDTV.x264-CTU.en.srt","BBT_S01E01.txt")  
#formatsrt("two.and.a.half.men.1003.hdtv-lol.en.srt","2.5mens10e3.txt")  
#formatsrt("Kane.srt","kanecn.txt")    
#formatAss("c:\\GTemp\\a.ass","c:\\GTemp\\b.txt")

def __formatsrt3xp(input, output):
    d = chardet.detect(open(input, "r").read())
    print "[%s] �Զ����Ϊ %s" %(input, d)

    @pipe.Pipe
    def X(t, org, rep="", op=re.U): return re.sub(org, rep, t, 0, op|re.U)

    @pipe.Pipe
    def W(t, output): codecs.open(output, encoding=d['encoding'], mode='w').write(t)

    codecs.open(input, encoding=d['encoding'], mode='r').read() \
        | X(r"-=.*?=-\s+") \
        | X(r"<.*?>") \
        | X(r"^[\s\d\-:>,]*[\r\n]+", "", re.M)\
        | X(r"(\S+)\s+$", r"\1", re.M)\
        | X(r"\.{3}[\r\n]+([a-z])", r" \1")\
        | X(r"([^\.?!])[\r\n]+", r"\1 ")\
        | X(r"(\w+)[,.?!](\w)", r"\1, \2")\
        | W(output)
    #�Ҳ����õ�ע�Ͱ취���Ͳ�ע���ˡ�    

def __formatsrt3xpcc(input, output):
    d = chardet.detect(open(input, "r").read())
    print "[%s] �Զ����Ϊ %s" %(input, d)

    @pipe.Pipe
    def X(t, org, rep="", op=re.U): return re.sub(org, rep, t, 0, op|re.U)

    @pipe.Pipe
    def W(t, output): codecs.open(output, encoding=d['encoding'], mode='w').write(t)

    codecs.open(input, encoding=d['encoding'], mode='r').read() \
        | X( #���� ==http://a.b.c/=- ɾ��
        r"-=.*?=-\s+") \
        | X( #���� <...> ɾ��
        r"<.*?>") \
        | X( #ɾ������Ҫ���С�ע��'-'�������ַ�
        r"^[\s\d\-:>,]*[\r\n]+", "", re.M)\
        | X(  #ɾ����β�Ŀ����ַ�
        r"(\S+)\s+$", r"\1", re.M)\
        | X(  #��β��...�ģ���һ�п�ʼ��һ��Сд��ĸ�ġ�
        r"\.{3}[\r\n]+([a-z])", r" \1")\
        | X(  #��βû�� .?!�ģ���ӿո�ȥ���س�����
        r"([^\.?!])[\r\n]+", r"\1 ")\
        | X( #��Щ���ʺ󶺺ź���û�пո񣬼���
        r"(\w+)[,.?!](\w)", r"\1, \2")\
        | W(output)

#��pipe�İ취��������Щ�ַ�������ʤ
def __subp(t):
    @pipe.Pipe
    def X(t, org, rep="", op=re.U): return re.sub(org, rep, t, 0, op|re.U)

    return  t | X(r"-=.*?=-\s+") \
              | X(r"<.*?>") \
              | X(r"^[\s\d\-:>,]*[\r\n]+", "", re.M) \
              | X(r"(\S+)\s+$", r"\1", re.M) \
              | X(r"\.{3}[\r\n]+([a-z])", r" \1") \
              | X(r"([^\.?!])[\r\n]+", r"\1 ") \
              | X(r"(\w+)[,.?!](\w)", r"\1, \2")

def __subf(t):
    def sub(org, rep="", op=re.U): return re.sub(org, rep, t, 0, op|re.U)
        #������ֻ����t�������޸�t�����ܸ�t��ֵ���������һ���µľֲ�������

    t = sub(r"-=.*?=-\s+")
    t = sub(r"<.*?>")
    t = sub(r"^[\s\d\-:>,]*[\r\n]+", "", re.M)
    t = sub(r"(\S+)\s+$", r"\1", re.M)
    t = sub(r"\.{3}[\r\n]+([a-z])", r" \1")
    t = sub(r"([^\.?!])[\r\n]+", r"\1 ")
    t = sub(r"(\w+)[,.?!](\w)", r"\1, \2")
    return t

def __subc(t):
    class sub:
        def __init__(self, t): self.t = t
        def __unicode__(self): return self.t
        def __call__(self, org, rep, op):
            self.t = re.sub(org, rep, self.t, 0, op)
            return self

    t = sub(t)(r"-=.*?=-\s+", "", re.U)\
          (r"<.*?>", "", re.U)\
          (r"^[\s\d\-:>,]*[\r\n]+", r"", re.M|re.U)\
          (r"(\S+)\s+$", r"\1", re.M|re.U)\
          (r"\.{3}[\r\n]+([a-z])", r" \1", re.U)\
          (r"([^\.?!])[\r\n]+", r"\1 ", re.U)\
          (r"(\w+)[,.?!](\w)", r"\1, \2", re.U)
    return unicode(t)

def __formatsrt3xEasy(input, output):
    d = chardet.detect(open(input, "r").read())
    print "[%s] �Զ����Ϊ %s" %(input, d)

    t = codecs.open(input, encoding=d['encoding'], mode='r').read()
    #t=subf(t)
    #t=subc(t)
    t = subp(t)
    codecs.open(output, encoding=d['encoding'], mode='w').write(t)
#���ܻ��Ч���Զ��жϱ��롣    
def __formatsrt3x(input, output):
    d = chardet.detect(open(input, "r").read())
    print "[%s] �Զ����Ϊ %s" %(input, d)

    t = codecs.open(input, encoding=d['encoding'], mode='r').read()

    t = re.sub(r"-=.*?=-\s+", "", t, 0, re.U)   #���� ==http://a.b.c/=- ɾ��
    t = re.sub(r"<.*?>", "", t, 0, re.U)          #���� <...> ɾ��
    t = re.sub(r"^[\s\d\-:>,]*[\r\n]+", r"", t, 0, re.M|re.U) #'-'�������ַ�
    t = re.sub(r"(\S+)\s+$", r"\1", t, 0, re.M|re.U) #ɾ����β�Ŀ����ַ�

    t = re.sub(r"\.{3}[\r\n]+([a-z])", r" \1", t, 0, re.U) #��β��...�ģ���һ�п�ʼ��һ��Сд��ĸ�ġ�
    t = re.sub(r"([^\.?!])[\r\n]+", r"\1 ", t, 0, re.U) #��βû�� .?!�ģ���ӿո�ȥ���س�����

    t = re.sub(r"(\w+)[,.?!](\w)", r"\1, \2", t, 0, re.U)#��Щ���ʺ󶺺ź���û�пո񣬼���

    codecs.open(output, encoding=d['encoding'], mode='w').write(t)


#��ʽ����Ӣ�����Ļ�ļ���elegent�汾, ASCII/GB2312/GBK������
def __formatsrt3(input, output):
    t = open(input, "r").read()

    t = re.sub(r"-=.*?=-\s+", "", t)   #���� ==http://a.b.c/=- ɾ��
    t = re.sub("<.*?>", "", t)          #���� <...> ɾ��
    t = re.sub(r"^[\s\d\-:>,]*[\r\n]+", "", t, 0, re.M) #ɾ������Ҫ���С�ע��'-'�������ַ�
    t = re.sub(r"(\S+)\s+$", r"\1", t, 0, re.M) #ɾ����β�Ŀ����ַ�

    t = re.sub(r"\.{3}[\r\n]+([a-z])", r" \1", t) #��β��...�ģ���һ�п�ʼ��һ��Сд��ĸ�ġ�
    t = re.sub(r"([^\.?!])[\r\n]+", r"\1 ", t) #��βû�� .?!�ģ���ӿո�ȥ���س�����

    t = re.sub(r"(\w+)[,.?!](\w)", r"\1, \2", t)#��Щ���ʺ󶺺ź���û�пո񣬼���

    open(output, "w").write(t)

#��ʽ����Ӣ�����Ļ�ļ���elegent�汾, unicode������
def __formatsrt3u(input, output):
    t = codecs.open(input, encoding='utf-16', mode='r').read()

    t = re.sub(r"-=.*?=-\s+", "", t, 0, re.U)   #���� ==http://a.b.c/=- ɾ��
    t = re.sub(r"<.*?>", "", t, 0, re.U)          #���� <...> ɾ��
    t = re.sub(r"^[\s\d\-:>,]*[\r\n]+", r"", t, 0, re.M|re.U) #'-'�������ַ�
    t = re.sub(r"(\S+)\s+$", r"\1", t, 0, re.M|re.U) #ɾ����β�Ŀ����ַ�

    t = re.sub(r"\.{3}[\r\n]+([a-z])", r" \1", t, 0, re.U) #��β��...�ģ���һ�п�ʼ��һ��Сд��ĸ�ġ�
    t = re.sub(r"([^\.?!])[\r\n]+", r"\1 ", t, 0, re.U) #��βû�� .?!�ģ���ӿո�ȥ���س�����

    t = re.sub(r"(\w+)[,.?!](\w)", r"\1, \2", t, 0, re.U)#��Щ���ʺ󶺺ź���û�пո񣬼���

#����ASSΪ����ѧϰ���ļ�������          
def __formatAss(input, output):
    f = open(input, "r")
    f1 = open(output, "w")
    for line in f:
        if not line.startswith("Dialogue"):
            continue;

        txt = line.find("fs24}")
        if(txt == -1):
            continue;

        line = line[txt+5:]
        cn = line[0:line.find("{\\r}")]

        enpos = line.find("\\N")
        if(enpos != -1):
            eng = line[enpos+2:-1]
            print eng
            f1.write(eng)
            f1.write("\n")
        print cn
        f1.write(cn)
        f1.write("\n\n")
    f.close()
    f1.close()