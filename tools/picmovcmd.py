#coding=gb2312
'''
    Usage:
        p help
            照片备份的完整帮助
        
        p zzp
            找照片
            
        p tj 1
            [统计] 当前目录下的照片文件
            使用规范文件名中的信息/dtadjust
            使用datetime
        p tj 0
            [统计] 当前目录下的照片文件，不使用metadata
            使用规范文件名中的信息/dtadjust
            不使用datetime，
            
        p sc 1
            [生成] 当前目录下的没有DT的照片的datetime，如果之前有，则不覆盖
        p sc 0
            [生成] 当前目录下的没有DT的照片的datetime，覆盖
                        
        p jc 1
            [检查] 当前目录下的照片文件是否可以归档
            使用规范文件名中的信息/dtadjust
            使用datetime
        p jc 0
            [检查]当前目录下的照片文件是否可以归档
            使用规范文件名中的信息/dtadjust
            不使用datetime，
        
        p mz
            预览当前目录下自动生成的文件[名字]信息。
            
        p mzj
            预览当前目录下自动生成的文件[名字]信息。
            
        p bf [archivedir]
            把当前目录[备份]到archivedir中去，原始文件存在
            
        p bfm [archivedir]
            把当前目录[备份]到archivedir中去，原始文件被删除
            
        p jcbf [archivedir]
            [检查备份]当前目录是否已经完全备份到archivedir中去
            MD5校验
            
        p scys [archivedir]
            [删除原始]
            将当前目录下已经备份在archive里面的文件删除
        
        p sckml [dir]
            [删除空目录] dir，递归
            
        p jca
            当前目录是归档主文件夹，检查是否有时间顺序错误 
            时间使用规范文件名中的信息/dtadjust/datetime

'''

def process(pic=True):
    import os,sys
    cmdhelpdoc = __doc__ if pic else __doc__.replace(" p "," m ").replace("照片","视频")
    if len(sys.argv) < 2:
        print cmdhelpdoc
        return
        
    cmd = sys.argv[1]
        
    import gpylib.tools.sonyhdr as s
    if pic:
        s.CLAIM_PROCESS_PIC()
    else:
        s.CLAIM_PROCESS_MOV()
    
    if cmd=="help":
        print s.__doc__
    elif cmd=="zzp":
        s.globphotoescurrentdir()
    elif cmd=='tj':
        s.countcurrentdir(len(sys.argv)>=3 and sys.argv[2]=='1')
    elif cmd=='sc':
        s.gendtcurrentdir(len(sys.argv)>=3 and sys.argv[2]=='1')
    elif cmd=='jc':
        s.checkcurrentdir(len(sys.argv)>=3 and sys.argv[2]=='1')
    elif cmd=='jca':
        s.picarchiveselftestcurrentdir()
    elif cmd=='mzj':
        s.printgennotecurrentdir()
    elif cmd=='mz':
        s.printgennamecurrentdir()
    elif cmd=='bf':
        s.autobakpiccurrentdir( unicode(sys.argv[2]) ,False)
    elif cmd=='bfm':
        s.autobakpiccurrentdir( unicode(sys.argv[2]) ,True)
    elif cmd=='jcbf':
        s.testarchiveiflostcurrentdir(  unicode(sys.argv[2]), len(sys.argv)>3 and sys.argv[3], False)
    elif cmd=='scys':
        s.testarchiveiflostcurrentdir( unicode(sys.argv[2]), "0", "del_ifok")
    else:
        print cmdhelpdoc
