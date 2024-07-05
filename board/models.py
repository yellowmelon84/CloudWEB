from django.db import models
import uuid

# Create your models here.
class CodeOption(models.Model):
    """
    CodeID : 코드ID
    CodeTypeID : 코드 타입 ID
    CodeTypeName : 코드 유형 명
    CodeDataID : 코드 데이터 ID
    CodeDataName : 코드 데이터 명
    CodeNote : 비고
    UseYN : 사용여부
    Created_data : 생성일자
    Modified_date : 수정일자
    """
    CodeID = models.AutoField(primary_key=True)
    CodeTypeID = models.CharField(max_length=3)
    CodeTypeName = models.CharField(max_length=100)
    CodeDataID = models.CharField(max_length=3)
    CodeDataName = models.CharField(max_length=100)
    CodeNote = models.CharField(max_length=100, null=True, blank=True)
    UseYN = models.CharField(max_length=1)
    Created_date = models.DateTimeField()
    Modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.CodeID)
    
class Cluster(models.Model):
    """
    ClusterID : 클러스터 ID
    ClusterName : 클러스터 명
    SERVER_TYPE1 : 영역 구분 1 (운영/개발/DR)
    SERVER_TYPE2 : 영역 구분 2 (중요/비중요)
    SERVER_TYPE3 : 영역 구분 3 (DMZ/AP/DB/LX/WIN/AP(W)/BIG/GPU/WLX)
    Created_data : 생성일자
    Modified_date : 수정일자
    """
    ClusterID = models.AutoField(primary_key=True)
    ClusterName = models.CharField(max_length=100)
    SERVER_TYPE1 = models.CharField(max_length=3)
    SERVER_TYPE2 = models.CharField(max_length=3)
    SERVER_TYPE3 = models.CharField(max_length=3)
    Created_date = models.DateTimeField()
    Modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.ClusterID)

class Host(models.Model):
    """
    HostID : 서버 ID
    HostName : 서버 명
    ClusterID : 서버 클러스터 ID
    Gen : 도입 세대
    Model : 서버 모델
    SerialNumber : 시리얼 번호
    CPU_Model : CPU 모델
    Core : CPU Core수
    Memory : 메모리 용량
    vSANDISK : 디스크 용량(vSAN 일경우)
    GPUMem : 메모리 용량(GPU 서버일 경우)
    EOS_Date : EOS 일자
    Created_Date : 생성 일자
    Modified_Date : 수정 일자
    """
    HostID = models.AutoField(primary_key=True)
    HostName = models.CharField(max_length=100)
    ClusterID = models.IntegerField()
    Gen = models.CharField(max_length=3)
    Model = models.CharField(max_length=100)
    SerialNumber = models.CharField(max_length=100)
    CPU_Model = models.CharField(max_length=100)
    Core = models.IntegerField()
    Memory = models.IntegerField()
    vSANDISK = models.IntegerField(null=True, blank=True)
    GPUMem = models.IntegerField(null=True, blank=True)
    EOS_Date = models.DateTimeField(null=True, blank=True)
    Created_date = models.DateTimeField()
    Modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.HostID)

class Storage(models.Model):
    """
    StorageID : 스토리지 ID
    StorageName : 스토리지 명
    Gen : 도입 세대
    Model	 : 스토리지 모델
    SerialNumber : 시리얼 번호
    FuncType :기능 (SAN/NAS/SAN&NAS)
    Size : 스토리지 용량(GB)
    EOS_Date : EOS 일자
    Created_Date	 : 생성 일자
    Modified_Date : 수정 일자
    """
    StorageID = models.AutoField(primary_key=True)
    StorageName = models.CharField(max_length=100)
    Gen = models.CharField(max_length=3)
    Model = models.CharField(max_length=100)
    SerialNumber = models.CharField(max_length=100)
    FuncType = models.CharField(max_length=10)
    Size = models.IntegerField()
    EOS_Date = models.DateTimeField(null=True, blank=True)
    Created_date = models.DateTimeField()
    Modified_date = models.DateTimeField(null=True, blank=True)
