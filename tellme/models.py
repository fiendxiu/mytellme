from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
import sys

# Create your models here.

STATUS_CHOICES = (
    (u'ON', u'ON'),
    (u'OFF',u'OFF'),
    (u'ON_TEST',u'ON_TEST'),
    (u'OFF_TEST',u'OFF_TEST'),
)

class Jituan(models.Model):
    jtid = models.IntegerField(u'集团ID' ,primary_key=True)
    jtname = models.CharField(u'集团名称', max_length=255)
    status = models.CharField(u'状态', max_length=8,choices=STATUS_CHOICES,default=u'ON')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s -- %s ' % (self.jtid,self.jtname)
      
class Cid(models.Model):
    cid = models.IntegerField(u'CID' ,primary_key=True)
    contractname = models.CharField(u'合同名', max_length=255)
    installname = models.CharField(u'安装名义', max_length=50 , default=u'东莞光联')
    jtid = models.ForeignKey(Jituan,on_delete=models.PROTECT)
    sales  = models.EmailField(u'业务邮箱')
    mrtg = models.CharField(u'MRTG链接', max_length=120, blank=True)
    mrtgpass = models.CharField(u'MRTG账号密码', max_length=80, blank=True)
    netflow = models.CharField(u'Netflow链接', max_length=120, blank=True)
    netflowpass = models.CharField(u'Netflow账号密码', max_length=80, blank=True)
    apppass = models.CharField(u'APP账号密码', max_length=120, blank=True)
    status = models.CharField(u'状态', max_length=8,choices=STATUS_CHOICES,default=u'ON_TEST')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.cid,self.contractname)
    class Meta:
        ordering = ['-cid']

class Site(models.Model):
    cid = models.ForeignKey(Cid,on_delete=models.PROTECT)
    siteid = models.CharField(u'SiteID' ,max_length=20,primary_key=True)
    sitename = models.CharField(u'站点名', max_length=255)
    siteaddr = models.TextField(u'地址', blank=True)
    mastercontact = models.CharField(u'主联络人', max_length=20, blank=True)
    masterphone = models.CharField(u'主联络电话', max_length=20, blank=True)
    masteremail = models.EmailField(u'主联络Email', blank=True)
    ocontacts = models.TextField(u'更多联系信息/备注信息', blank=True)
    status = models.CharField(u'站点状态', max_length=8,choices=STATUS_CHOICES,default=u'ON_TEST')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s -- %s ' % (self.cid,self.siteid)
    class Meta:
        ordering = ['-siteid']

def imageurl_handler(instance,filename):
    return "static/image/{id}/{file}".format(id=instance.siteid,file=filename)

class Siteimage(models.Model):
    siteid = models.CharField(max_length=20)
    uploader = models.CharField(u'上传者',max_length=20,blank=True)
    imageurl = models.ImageField(upload_to=imageurl_handler)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    def __str__(self):
        return self.siteid

def reporturl_handler(instance,filename):
    return "static/report/{id}/{file}".format(id=instance.siteid,file=filename)

class Sitereport(models.Model):
    siteid = models.CharField(max_length=20)
    filename = models.CharField(max_length=255,blank=True)
    uploader = models.CharField(u'上传者',max_length=20,blank=True)
    fileurl = models.FileField(upload_to=reporturl_handler)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    def __str__(self):
        return self.siteid

class Fastline(models.Model):
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    svcid = models.CharField(u'FastID' ,max_length=20,primary_key=True)
    fastpe = models.CharField(u'FastPE', max_length=50)
    fastport = models.CharField(u'接口', max_length=50,blank=True)
    fastwanip = models.CharField(u'WAN_IP', max_length=128, blank=True)
    hkip = models.TextField(u'HK_IP', blank=True)
    bandwidth = models.CharField(u'带宽', max_length=50)
    bkpe = models.CharField(u'备PE', max_length=50,blank=True)
    bkport = models.CharField(u'备接口', max_length=50,blank=True)
    bkwanip = models.CharField(u'备WANIP', max_length=128, blank=True)
    servicenumber = models.CharField(u'公司服务编号', max_length=50, blank=True)
    contractnumber = models.CharField(u'合同编号', max_length=50, blank=True)
    engineer = models.CharField(u'工程师', max_length=100, blank=True)
    status = models.CharField(u'状态', max_length=8,choices=STATUS_CHOICES,default=u'ON_TEST')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.siteid,self.svcid)
    class Meta:
        ordering = ['-svcid']

class Flanline(models.Model):
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    svcid = models.CharField(u'组网ID' ,max_length=20,primary_key=True)
    flanpe = models.CharField(u'FlanPE', max_length=50)
    flanport = models.CharField(u'接口', max_length=50,blank=True)
    flanwanip = models.CharField(u'WAN_IP', max_length=128, blank=True)
    lanip = models.TextField(u'LAN_IP', blank=True)
    bandwidth = models.CharField(u'带宽', max_length=50)
    bkpe = models.CharField(u'备PE', max_length=50,blank=True)
    bkport = models.CharField(u'备接口', max_length=50,blank=True)
    bkwanip = models.CharField(u'备WANIP', max_length=128, blank=True)
    servicenumber = models.CharField(u'公司服务编号', max_length=120, blank=True)
    contractnumber = models.CharField(u'合同编号', max_length=120, blank=True)
    engineer = models.CharField(u'工程师', max_length=100, blank=True)
    status = models.CharField(u'状态', max_length=8,choices=STATUS_CHOICES,default=u'ON_TEST')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.siteid,self.svcid)
    class Meta:
        ordering = ['-svcid']

class Localline(models.Model):
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    svcid = models.CharField(u'ID', max_length=20,primary_key=True)
    bandwidth = models.CharField(u'上传/下载', max_length=50)
    localsp = models.CharField(u'厂商/线路类型', max_length=50, blank=True)
    localname = models.CharField(u'报障名义', max_length=255, blank=True)
    localguard = models.CharField(u'报障信息', max_length=255, blank=True)
    localaddra = models.CharField(u'A端地址', max_length=255, blank=True)
    localaddrb = models.CharField(u'B端地址', max_length=255, blank=True)
    servicenumber = models.CharField(u'公司服务编号', max_length=50, blank=True)
    contractnumber = models.CharField(u'合同编号', max_length=50, blank=True)
    localnumber = models.CharField(u'线路编号', max_length=50, blank=True)
    status = models.CharField(u'状态', max_length=8,choices=STATUS_CHOICES,default=u'ON_TEST')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.siteid,self.svcid)
    class Meta:
        ordering = ['-svcid']

class NNIline(models.Model):
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    svcid = models.CharField(u'ID' ,max_length=20,primary_key=True)
    pe = models.CharField(u'PE', max_length=50)
    port = models.CharField(u'接口', max_length=50,blank=True)
    wanip = models.CharField(u'WAN_IP', max_length=128, blank=True)
    bandwidth = models.CharField(u'带宽', max_length=50, blank=True)
    nnisp = models.CharField(u'运营商', max_length=50, blank=True)
    nniname = models.CharField(u'报障名义', max_length=255, blank=True)
    nniguard = models.CharField(u'报障信息', max_length=255, blank=True)
    nniaddr = models.CharField(u'POP地址', max_length=255, blank=True)
    nninumber = models.CharField(u'线路编号', max_length=50, blank=True)
    servicenumber = models.CharField(u'公司服务编号', max_length=50, blank=True)
    contractnumber = models.CharField(u'合同编号', max_length=50, blank=True)
    engineer = models.CharField(u'工程师', max_length=100, blank=True)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.siteid,self.svcid)
    class Meta:
        ordering = ['-svcid']

class Siline(models.Model):
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    svcid = models.CharField(u'SIID' ,max_length=20,primary_key=True)
    siname = models.CharField(u'SI名', max_length=50)
    sicontent = models.CharField(u'SI内容', max_length=255, blank=True)
    servicenumber = models.CharField(u'公司服务编号', max_length=50, blank=True)
    contractnumber = models.CharField(u'合同编号', max_length=50, blank=True)
    status = models.CharField(u'状态', max_length=8,choices=STATUS_CHOICES,default=u'ON_TEST')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.siteid,self.svcid)
    class Meta:
        ordering = ['-svcid']

class Fastnetline(models.Model):
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    svcid = models.CharField(u'ID' ,max_length=20,primary_key=True)
    pe = models.CharField(u'PE', max_length=50)
    usedip = models.CharField(u'使用的IP', max_length=128, blank=True)
    domain = models.CharField(u'域名', max_length=255, blank=True)
    description = models.TextField(u'描述', blank=True)
    servicenumber = models.CharField(u'公司服务编号', max_length=50, blank=True)
    contractnumber = models.CharField(u'合同编号', max_length=50, blank=True)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.siteid,self.svcid)
    class Meta:
        ordering = ['-svcid']

class Monitorline(models.Model):
    siteid = models.ForeignKey(Site,on_delete=models.PROTECT)
    svcid = models.CharField(u'ID' ,max_length=20,primary_key=True)
    monitorobj = models.CharField(u'对象', max_length=50)
    monitorip = models.CharField(u'IP', max_length=20)
    status = models.CharField(u'状态', max_length=8,choices=STATUS_CHOICES,default=u'ON_TEST')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.siteid,self.svcid)
    class Meta:
        ordering = ['-svcid']

class Monitortag(models.Model):
    svcid = models.ForeignKey(Monitorline,on_delete=models.PROTECT)
    tagname = models.CharField(u'标签名' ,max_length=50)
    tagvalue = models.CharField(u'标签值' ,max_length=255)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s --- %s ' % (self.svcid,self.tagname,self.tagvalue)
    class Meta:
        ordering = ['create_date']

class Fastnettag(models.Model):
    svcid = models.ForeignKey(Fastnetline,on_delete=models.PROTECT)
    tagname = models.CharField(u'标签名' ,max_length=50)
    tagvalue = models.CharField(u'标签值' ,max_length=255)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s --- %s ' % (self.svcid,self.tagname,self.tagvalue)
    class Meta:
        ordering = ['create_date']

class Sitag(models.Model):
    svcid = models.ForeignKey(Siline,on_delete=models.PROTECT)
    tagname = models.CharField(u'标签名' ,max_length=50)
    tagvalue = models.CharField(u'标签值' ,max_length=255)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s --- %s ' % (self.svcid,self.tagname,self.tagvalue)
    class Meta:
        ordering = ['create_date']

class Localtag(models.Model):
    svcid = models.ForeignKey(Localline,on_delete=models.PROTECT)
    tagname = models.CharField(u'标签名' ,max_length=50)
    tagvalue = models.CharField(u'标签值' ,max_length=255)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s --- %s ' % (self.svcid,self.tagname,self.tagvalue)
    class Meta:
        ordering = ['create_date']

class NNItag(models.Model):
    svcid = models.ForeignKey(NNIline,on_delete=models.PROTECT)
    tagname = models.CharField(u'标签名' ,max_length=50)
    tagvalue = models.CharField(u'标签值' ,max_length=255)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s --- %s ' % (self.svcid,self.tagname,self.tagvalue)
    class Meta:
        ordering = ['create_date']

class Flantag(models.Model):
    svcid = models.ForeignKey(Flanline,on_delete=models.PROTECT)
    tagname = models.CharField(u'标签名' ,max_length=50)
    tagvalue = models.CharField(u'标签值' ,max_length=255)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s --- %s ' % (self.svcid,self.tagname,self.tagvalue)
    class Meta:
        ordering = ['create_date']

class Fasttag(models.Model):
    svcid = models.ForeignKey(Fastline,on_delete=models.PROTECT)
    tagname = models.CharField(u'标签名' ,max_length=50)
    tagvalue = models.CharField(u'标签值' ,max_length=255)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s --- %s ' % (self.svcid,self.tagname,self.tagvalue)
    class Meta:
        ordering = ['create_date']

class Traceentry(models.Model):
    objname = models.CharField(u'对象名',max_length=20)
    objpk = models.CharField(u'对象id',max_length=20)
    type = models.CharField(u'类型',max_length=10)
    context = models.TextField(u'内容')
    oprater = models.CharField(u'操作人',max_length=30)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    class Meta:
        ordering = ['-create_date']

class Noc(models.Model):
    name = models.CharField(u'name',max_length=20,primary_key=True)

class Ticket(models.Model):
    name = models.CharField(u'name',max_length=20,primary_key=True)

class Pm(models.Model):
    name = models.CharField(u'name',max_length=20,primary_key=True)

class Psale(models.Model):
    name = models.CharField(u'name',max_length=20,primary_key=True)

