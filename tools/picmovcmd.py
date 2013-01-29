#coding=gb2312
'''
    Usage:
        p help
            ��Ƭ���ݵ���������
        
        p zzp
            ����Ƭ
            
        p tj 1
            [ͳ��] ��ǰĿ¼�µ���Ƭ�ļ�
            ʹ�ù淶�ļ����е���Ϣ/dtadjust
            ʹ��datetime
        p tj 0
            [ͳ��] ��ǰĿ¼�µ���Ƭ�ļ�����ʹ��metadata
            ʹ�ù淶�ļ����е���Ϣ/dtadjust
            ��ʹ��datetime��
            
        p sc 1
            [����] ��ǰĿ¼�µ�û��DT����Ƭ��datetime�����֮ǰ�У��򲻸���
        p sc 0
            [����] ��ǰĿ¼�µ�û��DT����Ƭ��datetime������
                        
        p jc 1
            [���] ��ǰĿ¼�µ���Ƭ�ļ��Ƿ���Թ鵵
            ʹ�ù淶�ļ����е���Ϣ/dtadjust
            ʹ��datetime
        p jc 0
            [���]��ǰĿ¼�µ���Ƭ�ļ��Ƿ���Թ鵵
            ʹ�ù淶�ļ����е���Ϣ/dtadjust
            ��ʹ��datetime��
        
        p mz
            Ԥ����ǰĿ¼���Զ����ɵ��ļ�[����]��Ϣ��
            
        p mzj
            Ԥ����ǰĿ¼���Զ����ɵ��ļ�[����]��Ϣ��
            
        p bf [archivedir]
            �ѵ�ǰĿ¼[����]��archivedir��ȥ��ԭʼ�ļ�����
            
        p bfm [archivedir]
            �ѵ�ǰĿ¼[����]��archivedir��ȥ��ԭʼ�ļ���ɾ��
            
        p jcbf [archivedir]
            [��鱸��]��ǰĿ¼�Ƿ��Ѿ���ȫ���ݵ�archivedir��ȥ
            MD5У��
            
        p scys [archivedir]
            [ɾ��ԭʼ]
            ����ǰĿ¼���Ѿ�������archive������ļ�ɾ��
        
        p sckml [dir]
            [ɾ����Ŀ¼] dir���ݹ�
            
        p jca
            ��ǰĿ¼�ǹ鵵���ļ��У�����Ƿ���ʱ��˳����� 
            ʱ��ʹ�ù淶�ļ����е���Ϣ/dtadjust/datetime

'''

def process(pic=True):
    import os,sys
    cmdhelpdoc = __doc__ if pic else __doc__.replace(" p "," m ").replace("��Ƭ","��Ƶ")
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
