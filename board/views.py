from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
import datetime
import xlwt
import pandas as pd
from openpyxl import Workbook, load_workbook

from .models import CodeOption, Cluster, Host, Storage

# Main 페이지
def main(request):
    return render(request, 'board/main.html')

# Code 페이지
def code_index(request):
    #all_Codes = CodeOption.objects.all().order_by("-CodeTypeID", "-CodeDataID")
    #all_Codes = CodeOption.objects.filter(UseYN='Y').order_by("CodeTypeID", "CodeDataID")
    all_Codes = CodeOption.objects.all().order_by("CodeTypeID", "CodeDataID")
    return render(request, 'board/code_index.html', {'title': 'CODE 정보', 'board_list':all_Codes})

# Code 추가 페이지
def code_add(request):
    return render(request, 'board/code_add.html')

# Code 추가 처리
def code_add_exec(request):
    b = CodeOption(CodeTypeID=request.POST['CodeTypeID'], CodeTypeName=request.POST['CodeTypeName'], CodeDataID=request.POST['CodeDataID'], CodeDataName=request.POST['CodeDataName'], UseYN=request.POST['UseYN'], Created_date=timezone.now())
    b.save()
    return HttpResponseRedirect(reverse('board:code_index'))

# Code 상세 페이지
def code_detail(request, codeid):
    code = CodeOption.objects.get(CodeID=codeid)
    return render(request, 'board/code_detail.html', {'Code': code})

# Code 변경 처리 (Code_detail.html)
def edit_code(request, codeid):
    CodeOption.objects.filter(CodeID=codeid).update(CodeTypeID=request.POST['CodeTypeID'], CodeTypeName=request.POST['CodeTypeName'], CodeDataID=request.POST['CodeDataID']
                                                     , CodeDataName=request.POST['CodeDataName'], UseYN=request.POST['UseYN'], Modified_date=timezone.now())
    messages.add_message(request, messages.INFO, '변경되었습니다.')

    return redirect('/board/code_index/'+str(codeid))

# Code 삭제 처리 (Code_detail.html)
def delete_code(request, codeid):
    record = CodeOption.objects.get(CodeID=codeid)
    record.delete()

    return HttpResponseRedirect(reverse('board:code_index'))



# Cluster 페이지
def cluster_index(request):
    query = '''select A.ClusterID as 'ClusterID', A.ClusterName as 'ClusterName', B.CodeDataName as 'SERVER_TYPE1'
                                        ,C.CodeDataName as 'SERVER_TYPE2', D.CodeDataName as 'SERVER_TYPE3' 
                                        from board_cluster A
                                        left outer join (select * from board_codeoption where CodeTypeID = 'S01') B on A.SERVER_TYPE1 = B.CodeDataID
                                        left outer join (select * from board_codeoption where CodeTypeID = 'S02') C on A.SERVER_TYPE2 = C.CodeDataID
                                        left outer join (select * from board_codeoption where CodeTypeID = 'S03') D on A.SERVER_TYPE3 = D.CodeDataID
                                        order by B.CodeDataID, C.CodeDataID, D.CodeDataID, A.ClusterName
                                        '''
    all_Clusters = Cluster.objects.raw(query)
    return render(request, 'board/cluster_index.html', {'title': 'Cluster 정보', 'board_list':all_Clusters})

# Cluster 추가 페이지
def cluster_add(request):
    # 코드 정보에서 서버 타입 정보 조회 (도롭다운리스트에서 사용)
    type1 = CodeOption.objects.filter(CodeTypeID='S01').only('CodeDataID', 'CodeDataName')
    type2 = CodeOption.objects.filter(CodeTypeID='S02').only('CodeDataID', 'CodeDataName')
    type3 = CodeOption.objects.filter(CodeTypeID='S03').only('CodeDataID', 'CodeDataName')

    return render(request, 'board/cluster_add.html', {'type1_list':type1, 'type2_list':type2, 'type3_list':type3})

# cluster 추가 처리
def cluster_add_exec(request):
    b = Cluster(ClusterName=request.POST['ClusterName'], SERVER_TYPE1=request.POST['SERVER_TYPE1'], SERVER_TYPE2=request.POST['SERVER_TYPE2'], SERVER_TYPE3=request.POST['SERVER_TYPE3'], Created_date=timezone.now())
    b.save()
    return HttpResponseRedirect(reverse('board:cluster_index'))


# cluster 상세 페이지
def cluster_detail(request, clusterid):
    query = f'''select A.ClusterID as 'ClusterID', A.ClusterName as 'ClusterName' 
                    ,A.SERVER_TYPE1 as 'ST1_ID', B.CodeDataName as 'ST1_NAME'
                    ,A.SERVER_TYPE2 as 'ST2_ID', C.CodeDataName as 'ST2_NAME'
                    ,A.SERVER_TYPE2 as 'ST3_ID', D.CodeDataName as 'ST3_NAME'
                    ,A.Created_date as 'Created_date', A.Modified_date as 'Modified_date'
                from board_cluster A
                left outer join (select * from board_codeoption where CodeTypeID = 'S01') B on A.SERVER_TYPE1 = B.CodeDataID
                left outer join (select * from board_codeoption where CodeTypeID = 'S02') C on A.SERVER_TYPE2 = C.CodeDataID
                left outer join (select * from board_codeoption where CodeTypeID = 'S03') D on A.SERVER_TYPE3 = D.CodeDataID
                where A.ClusterID = {clusterid}'''
    cluster = Cluster.objects.raw(query)

    type1 = CodeOption.objects.filter(CodeTypeID='S01').only('CodeDataID', 'CodeDataName')
    type2 = CodeOption.objects.filter(CodeTypeID='S02').only('CodeDataID', 'CodeDataName')
    type3 = CodeOption.objects.filter(CodeTypeID='S03').only('CodeDataID', 'CodeDataName')

    return render(request, 'board/cluster_detail.html', {'cluster':cluster[0], 'type1_list':type1, 'type2_list':type2, 'type3_list':type3})


# cluster 변경 처리 (cluster_detail.html)
def edit_cluster(request, clusterid):
    Cluster.objects.filter(ClusterID=clusterid).update(ClusterName=request.POST['ClusterName'], SERVER_TYPE1=request.POST['SERVER_TYPE1'], SERVER_TYPE2=request.POST['SERVER_TYPE2'], SERVER_TYPE3=request.POST['SERVER_TYPE3'], Modified_date=timezone.now())
    messages.add_message(request, messages.INFO, '변경되었습니다.')

    return redirect('/board/cluster_index/'+str(clusterid))
    
# cluster 삭제 처리 (cluster_detail.html)
def delete_cluster(request, clusterid):
    record = Cluster.objects.get(ClusterID=clusterid)
    record.delete()

    return HttpResponseRedirect(reverse('board:cluster_index'))


# Host 페이지
def host_index(request):
    query = f'''select A.HostID as 'HostID', A.HostName as 'HostName', A.ClusterID as 'ClusterID', B.ClusterName as 'ClusterName'
                     ,A.Gen as 'GenID' ,B.CodeDataName as 'GenName', A.Model as 'Model', A.SerialNumber as 'SerialNumber'
                     ,A.CPU_Model as 'CPU_Model', A.Core as 'Core', A.Memory as 'Memory'
                     ,A.vSANDISK as 'vSANDISK', A.GPUMem as 'GPUMem', A.EOS_Date as 'EOS_Date'
                from board_host A
                left outer join board_cluster B on A.ClusterID = B.ClusterID
                left outer join (select * from board_codeoption where CodeTypeID = 'G01') B on A.Gen = B.CodeDataID
                order by A.HostName
            '''
    all_Hosts = Host.objects.raw(query)
    return render(request, 'board/host_index.html', {'title': 'Host 정보', 'board_list':all_Hosts})

# host 추가
def host_add(request):
    all_cluster = Cluster.objects.only('ClusterID', 'ClusterName')
    all_gen = CodeOption.objects.filter(CodeTypeID='G01').only('CodeDataID', 'CodeDataName')
    today = timezone.now()
    return render(request, 'board/host_add.html', {'cluster_list': all_cluster, 'gen_list': all_gen, 'today': today})

# host 추가 처리
def host_add_exec(request):
    b = Host(HostName=request.POST['HostName'], ClusterID=request.POST['ClusterID'], Gen=request.POST['Gen'], Model=request.POST['Model'], SerialNumber=request.POST['SerialNumber'], CPU_Model=request.POST['CPU_Model'], Core=request.POST['Core'], Memory=request.POST['Memory'], vSANDISK=nvl(request.POST['vSANDISK']), GPUMem=nvl(request.POST['GPUMem']), EOS_Date=request.POST['EOS_Date'], Created_date=timezone.now())
    b.save()
    return HttpResponseRedirect(reverse('board:host_index'))

# host 상세 페이지
def host_detail(request, hostid):
    query = f'''select A.HostID as 'HostID', A.HostName as 'HostName', A.ClusterID as 'ClusterID', B.ClusterName as 'ClusterName'
                     ,A.Gen as 'GenID' ,B.CodeDataName as 'GenName', A.Model as 'Model', A.SerialNumber as 'SerialNumber'
                     ,A.CPU_Model as 'CPU_Model', A.Core as 'Core', A.Memory as 'Memory'
                     ,A.vSANDISK as 'vSANDISK', A.GPUMem as 'GPUMem', A.EOS_Date as 'EOS_Date'
                from board_host A
                left outer join board_cluster B on A.ClusterID = B.ClusterID
                left outer join (select * from board_codeoption where CodeTypeID = 'G01') B on A.Gen = B.CodeDataID 
                where A.HostID = {hostid}
                order by A.HostName
            '''
    host = Cluster.objects.raw(query)

    all_cluster = Cluster.objects.only('ClusterID', 'ClusterName')
    all_gen = CodeOption.objects.filter(CodeTypeID='G01').only('CodeDataID', 'CodeDataName')

    return render(request, 'board/host_detail.html', {'host':host[0], 'cluster_list': all_cluster, 'gen_list': all_gen})

# Host 변경 처리 (host_detail.html)
def host_edit(request, hostid):
    Host.objects.filter(HostID=hostid).update(HostName=request.POST['HostName'], ClusterID=request.POST['ClusterID'], Gen=request.POST['Gen'], Model=request.POST['Model'], SerialNumber=request.POST['SerialNumber'], CPU_Model=request.POST['CPU_Model'], Core=request.POST['Core'], Memory=request.POST['Memory'], vSANDISK=nvl(request.POST['vSANDISK']), GPUMem=nvl(request.POST['GPUMem']), EOS_Date=request.POST['EOS_Date'], Modified_date=timezone.now())
    messages.add_message(request, messages.INFO, '변경되었습니다.')

    return redirect('/board/host_index/'+ str(hostid))

# Storage 페이지
def storage_index(request):
    query = f'''select A.StorageID as 'StorageID', A.StorageName as 'StorageName'
                     ,A.Gen as 'GenID' ,B.CodeDataName as 'GenName'
                     ,A.Model as 'Model', A.SerialNumber as 'SerialNumber'
                     ,A.FuncType as 'FuncType', A.Size as 'Size'
                     ,A.EOS_Date as 'EOS_Date'
                from board_storage A
                left outer join (select * from board_codeoption where CodeTypeID = 'G01') B on A.Gen = B.CodeDataID
                order by A.StorageName
            '''
    all_Storages = Storage.objects.raw(query)
    return render(request, 'board/storage_index.html', {'title': 'Storage 정보', 'board_list':all_Storages})

#### 공통 영역 ####

# Excel 다운로드 / Pandas 사용
def excel_export(request, typeid):
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    now = datetime.datetime.now()

    # CODE 정보 처리
    if typeid == 0:             
        typename = 'Code'
        # 첫번쨰 열에 들어갈 컬럼명 설정
        col_names = ['CodeID', 'CodeTypeID', 'CodeTypeName', 'CodeDataID', 'CodeDataName', 'UseYN']
        # DB에 있는 데이터 저장
        rows = CodeOption.objects.values_list('CodeID', 'CodeTypeID', 'CodeTypeName', 'CodeDataID', 'CodeDataName', 'UseYN').order_by('CodeTypeID', 'CodeDataID')
        
        print(type(rows))

    # Cluster 정보 처리
    elif typeid == 1:
        typename = 'Cluster'
        col_names = ['ClusterID', 'ClusterName', 'SERVER_TYPE1', 'SERVER_TYPE2', 'SERVER_TYPE3']
        query = f'''select A.ClusterID as 'ClusterID', A.ClusterName as 'ClusterName'
                         ,B.CodeDataName as 'SERVER_TYPE1'
                         ,C.CodeDataName as 'SERVER_TYPE2'
                         ,D.CodeDataName as 'SERVER_TYPE3' 
                   from board_cluster A
                   left outer join (select * from board_codeoption where CodeTypeID = 'S01') B on A.SERVER_TYPE1 = B.CodeDataID
                   left outer join (select * from board_codeoption where CodeTypeID = 'S02') C on A.SERVER_TYPE2 = C.CodeDataID
                   left outer join (select * from board_codeoption where CodeTypeID = 'S03') D on A.SERVER_TYPE3 = D.CodeDataID
                   order by B.CodeDataID, C.CodeDataID, D.CodeDataID
                   '''
        rows = Cluster.objects.raw(query)

        print(type(rows))

        for row in rows:   
            print(', '.join(
                ['{}: {}'.format(field, getattr(row, field))
                    for field in ['ClusterID', 'ClusterName', 'SERVER_TYPE1', 'SERVER_TYPE2', 'SERVER_TYPE3']]
                )
            )
    
    # 호스트 정보 처리
    elif typeid == 2:
        typename = "Host"
        col_names = ['HostID', 'HostName', 'ClusterName', 'Gen', 'Model', 'SerialNumber', 'CPU_Model', 'Core', 'Memory', 'vSANDISK', 'GPUMem', 'EOS_Date']
        query = f'''select A.HostID as 'HostID', A.HostName as 'HostName', B.ClusterName as 'ClusterName'
                     ,C.CodeDataName as 'Gen', A.Model as 'Model', A.SerialNumber as 'SerialNumber'
                     ,A.CPU_Model as 'CPU_Model', A.Core as 'Core', A.Memory as 'Memory'
                     ,A.vSANDISK as 'vSANDISK', A.GPUMem as 'GPUMem', A.EOS_Date as 'EOS_Date'
                    from board_host A
                    left outer join board_cluster B on A.ClusterID = B.ClusterID
                    left outer join (select * from board_codeoption where CodeTypeID = 'G01') C on A.Gen = C.CodeDataID
                    order by A.HostName
                '''
        rows = Host.objects.raw(query)
        
        rowsdics = [item.__dict__ for item in rows]
        for rowdic in rowsdics:
            rowdic["EOS_Date"] = rowdic["EOS_Date"].strftime('%Y-%m-%d')
        

    else:
        messages.add_message(request, messages.ERROR, '정의되지 않았습니다.')
        return HttpResponseRedirect(reverse('board:code_index'))
    
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\''+typename+'_Info_'+str(now.strftime("%Y%m%d"))+'.xlsx' 
    
    if typeid == 0:
        df = pd.DataFrame(rows, columns=col_names)
    else: 
        df = pd.DataFrame([item.__dict__ for item in rows], columns=col_names)

    df.to_excel(response, index=False)

    return response
    
# Excel 업로드
def excel_import(request, typeid):
    try: 
        excel_file = request.FILES['excelFile']
        rows = pd.read_excel(excel_file)

        # 코드 정보
        if typeid == 0:
            for row in rows.itertuples():
                b = CodeOption(CodeTypeID=row[1], CodeTypeName=row[2], CodeDataID=row[3], CodeDataName=row[4], UseYN=row[5], Created_date=timezone.now())
                b.save()
            url = 'board:code_index'
        # 클러스터 정보
        elif typeid == 1:
            for row in rows.itertuples():
                type1 = CodeOption.objects.filter(CodeTypeID='S01', CodeDataName=row[2]).only('CodeDataID')
                type2 = CodeOption.objects.filter(CodeTypeID='S02', CodeDataName=row[3]).only('CodeDataID')
                type3 = CodeOption.objects.filter(CodeTypeID='S03', CodeDataName=row[4]).only('CodeDataID')
                b = Cluster(ClusterName=row[1], SERVER_TYPE1=type1[0].CodeDataID, SERVER_TYPE2=type2[0].CodeDataID, SERVER_TYPE3=type3[0].CodeDataID, Created_date=timezone.now())
                b.save()
            url = 'board:cluster_index'

        # 호스트 정보
        elif typeid == 2:
            print("11111111")
            for row in rows.itertuples():
                clusterid = Cluster.objects.filter(ClusterName=row[2]).only('ClusterID')
                gen = CodeOption.objects.filter(CodeTypeID='G01', CodeDataName=row[3]).only('CodeDataID')
                print("%s %s" % clusterid, gen)
                b = Host(HostName=row[1], ClusterID=clusterid, Gen=gen, Model=row[4], SerialNumber=row[5], CPU_Model=row[6], Core=row[7], Memory=row[8], vSANDISK=nvl(row[9]), GPUMem=nvl(row[10]), EOS_Date=datetime.strptime(row[11], '%Y-%m-%d'), Modified_date=timezone.now())
                b.save()
            url = 'board:host_index'

        else:
            messages.add_message(request, messages.ERROR, '정의되지 않았습니다.')
            
        return HttpResponseRedirect(reverse(url))
    
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Data Upload Failed.')
        return HttpResponseRedirect(reverse('board:main'))  

# 공백 처리
def nvl(v):
    if v == '':
        return None
    elif v == 'None':
        return None
    elif v == 'nan':
        return None
    else:
        return v



   
    




    


    
    
    

