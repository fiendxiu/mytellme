from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from tellme.models import *
from django.db import IntegrityError
from tellme.clscid import clscid
from tellme.clsform import Jituanform,Cidform,Siteform,Fastform,Flanform,Localform,NNIform,Siform,Monitorform,Fasttagform,Flantagform,Localtagform,NNItagform,Sitagform,Monitortagform,Photoform,Reportform
from tellme.tracemodel import trace_add,trace_edit,trace_del
import os,re

# Create your views here.

@csrf_exempt
def login_view(request):
    error = True
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/')
        else:
            return render(request,'login.html',{'error':error})
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@csrf_exempt
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user,request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        form = PasswordChangeForm(user=request.user)
        return render(request,'changepass.html',{'form':form})
    errors = "你好像无权访问吧?"
    return HttpResponseRedirect('/login/') 

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def paging(data,page):
        paginator = Paginator(data,30)
        try:
                newpage=int(page)
        except ValueError:
                newpage=1
        try:
                contacts = paginator.page(newpage)
        except PageNotAnInteger:
                contacts = paginator.page(1)
        except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
        return contacts

def search(request):
    curl = request.get_full_path()
    filterOff = "off"
    if request.user.is_authenticated:
        error = True
        if request.user.has_perm('tellme.change_noc'):
            group = "noc/"
        elif request.user.has_perm('tellme.change_ticket'):
            group = "ticket/"
        elif request.user.has_perm('tellme.change_pm'):
            group = "pm/"
        else:
            group = ""
        if 'q' in request.GET:
            q = request.GET['q']
            if '酒店' in q:
                q=''
            info = request.GET['info']
            if q:
                if info == "cid" :
                    if filterOff == "on":
                        tempdata = Cid.objects.filter(cid__icontains=q)
                        data = tempdata.exclude(status__exact="OFF")
                    else:
                        data = Cid.objects.filter(cid__icontains=q)
                    room = paging(data,request.GET.get('page','1'))
                    type = 'cid'
                elif info == "contractname":
                    if filterOff == "on":
                        tempdata = Cid.objects.filter(contractname__icontains=q)
                        data = tempdata.exclude(status__exact="OFF")
                    else:
                        data = Cid.objects.filter(contractname__icontains=q)
                    room = paging(data,request.GET.get('page','1'))
                    type = 'cid'
                elif info == "sitename" :
                    if filterOff == "on":
                        tempdata = Site.objects.filter(sitename__icontains=q)
                        data = tempdata.exclude(status__exact="OFF")
                    else:
                        data = Site.objects.filter(sitename__icontains=q)
                    room = paging(data,request.GET.get('page','1'))
                    type = 'site'
                elif info == "servicenumber":
                    if filterOff == "on":
                        tempdata = Fastline.objects.filter(servicenumber__icontains=q)
                        data['fast'] = tempdata.exclude(status__exact="OFF")
                        tempdata = Flanline.objects.filter(servicenumber__icontains=q)
                        data['flan'] = tempdata.exclude(status__exact="OFF")
                        tempdata = Localline.objects.filter(servicenumber__icontains=q)
                        data['local'] = tempdata.exclude(status__exact="OFF")
                        tempdata = NNIline.objects.filter(servicenumber__icontains=q)
                        data['nni'] = tempdata.exclude(status__exact="OFF")
                        tempdata = Siline.objects.filter(servicenumber__icontains=q)
                        data['si'] = tempdata.exclude(status__exact="OFF")
                    else:
                        data = []
                        data += Fastline.objects.filter(servicenumber__icontains=q)
                        data += Flanline.objects.filter(servicenumber__icontains=q)
                        data += Localline.objects.filter(servicenumber__icontains=q)
                        data += NNIline.objects.filter(servicenumber__icontains=q)
                        data += Siline.objects.filter(servicenumber__icontains=q)
                    room = paging(data,request.GET.get('page','1'))
                    type = 'service'
                elif info == "localnumber":
                    if filterOff == "on":
                        tempdata = Localline.objects.filter(localnumber__icontains=q)
                        data = tempdata.exclude(status__exact="OFF")
                    else:
                        data = Localline.objects.filter(localnumber__icontains=q)
                    room = paging(data,request.GET.get('page','1'))
                    type = 'local'
                elif info == "tag":
                    data = []
                    data += Fasttag.objects.filter(tagvalue__icontains=q)
                    data += Flantag.objects.filter(tagvalue__icontains=q)
                    data += Localtag.objects.filter(tagvalue__icontains=q)
                    data += NNItag.objects.filter(tagvalue__icontains=q)
                    data += Sitag.objects.filter(tagvalue__icontains=q)
                    data += Monitortag.objects.filter(tagvalue__icontains=q)
                    room = paging(data,request.GET.get('page','1'))
                    type = 'tag'
                if len(room):
                    return render(request,'searchlist.html',{'curl':curl,'room':room,'data':data,'group':group,'type':type})
        return render(request,'index.html',{'error':error})
    return HttpResponseRedirect('/login/')

def jtid(request,jituanid):
    if request.user.is_authenticated:
        if jituanid:
            jtlist = True
            tempdata = Cid.objects.filter(jtid=jituanid)
            data =  tempdata.exclude(status__exact="OFF")
            room = paging(data,request.GET.get('page','1'))
            if request.user.has_perm('tellme.change_noc'):
                return render(request,'noc/jituan.html',{'room':room,'data':data,'jtlist':jtlist})
            else:
                return render(request,'jituan.html',{'room':room,'data':data,'jtlist':jtlist})
        else:
            jtlist = False
            data = Jituan.objects.exclude(status__icontains='OFF').all()
            room = paging(data,request.GET.get('page','1'))
            if request.user.has_perm('tellme.change_noc'):
                return render(request,'noc/jituan.html',{'room':room,'data':data,'jtlist':jtlist})
            else:
                return render(request,'jituan.html',{'room':room,'data':data,'jtlist':jtlist})
    return HttpResponseRedirect('/login/')

def cid(request,cid):
    cid = clscid(cid)
    if request.user.is_authenticated:
        if cid.objstate:
            if request.user.has_perm('tellme.change_noc'):
                if 'collapse' in request.GET:
                    return render(request,'noc/display.html',{'cid':cid,'collapse':request.GET['collapse']})
                return render(request,'noc/cid.html',{'cid':cid})
            elif request.user.has_perm('tellme.change_ticket'):
                if 'collapse' in request.GET:
                    return render(request,'ticket/display.html',{'cid':cid,'collapse':request.GET['collapse']})
                return render(request,'ticket/cid.html',{'cid':cid})
            elif request.user.has_perm('tellme.change_pm'):
                if 'collapse' in request.GET:
                    return render(request,'pm/display.html',{'cid':cid,'collapse':request.GET['collapse']})
                return render(request,'pm/cid.html',{'cid':cid})
            else:
                return render(request,'index.html')
        else:
            error = True
            return render(request,'index.html',{'error':error})
    return HttpResponseRedirect('/login/')

def delete(request,url,id):
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            if url == "jtid":
                Del = get_object_or_404(Jituan,pk=id)
            elif url == "cid":
                Del = get_object_or_404(Cid,pk=id)
                cid = Del.cid
            elif url == "site":
                Del = get_object_or_404(Site,pk=id)
                cid = Del.cid.cid
            elif url == "fast":
                Del = get_object_or_404(Fastline,pk=id)
                cid = Del.siteid.cid.cid
            elif url == "flan":
                Del = get_object_or_404(Flanline,pk=id)
                cid = Del.siteid.cid.cid
            elif url == "local":
                Del = get_object_or_404(Localline,pk=id)
                cid = Del.siteid.cid.cid
            elif url == "nni":
                Del = get_object_or_404(NNIline,pk=id)
                cid = Del.siteid.cid.cid
            elif url == "si":
                Del = get_object_or_404(Siline,pk=id)
                cid = Del.siteid.cid.cid
            elif url == "monitor":
                Del = get_object_or_404(Monitorline,pk=id)
                cid = Del.siteid.cid.cid
            elif url == "fasttag":
                Del = get_object_or_404(Fasttag,pk=id)
                svc = "fast"
                svcid = Del.svcid.svcid
            elif url == "flantag":
                Del = get_object_or_404(Flantag,pk=id)
                svc = "flan"
                svcid = Del.svcid.svcid
            elif url == "localtag":
                Del = get_object_or_404(Localtag,pk=id)
                svc = "local"
                svcid = Del.svcid.svcid
            elif url == "nnitag":
                Del = get_object_or_404(NNItag,pk=id)
                svc = "nni"
                svcid = Del.svcid.svcid
            elif url == "sitag":
                Del = get_object_or_404(Sitag,pk=id)
                svc = "si"
                svcid = Del.svcid.svcid
            elif url == "monitortag":
                Del = get_object_or_404(Monitortag,pk=id)
                svc = "monitor"
                svcid = Del.svcid.svcid
            else:
                Del = ""
            try:
                trace_del(Del,request.user.username)
                Del.delete()
            except IntegrityError:
                errors = "底下有分类数据未清空！无法删除"
                return render(request,'noc/error.html',{'errors':errors})
            else:
                if url in ["jtid"]:
                    return HttpResponseRedirect('/jtid/')
                elif url in ["cid","site"]:
                    return HttpResponseRedirect('/cid/'+str(cid))
                elif url in ["fast","flan","local","nni","si","monitor"]:
                    return HttpResponseRedirect('/cid/'+str(cid)+'/?collapse='+Del.siteid.siteid)
                else:
                    return HttpResponseRedirect('/tag/'+svc+'/'+svcid+'/')
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def trashfile(request,type,id):
    if request.user.is_authenticated:
        if type == "report":
            file = get_object_or_404(Sitereport,pk=id)
            filepath = file.fileurl
            siteid = file.siteid
        elif type == "photo":
            file = get_object_or_404(Siteimage,pk=id)
            filepath = file.imageurl
            siteid = file.siteid
        else:
            file = ""
        try:
            trace_del(file,request.user.username)
            os.remove(str(filepath))
            file.delete()
        except:
            errors = "删除数据库或文件的操作，异常！"
            return render(request,'noc/error.html',{'errors':errors})
        else:
            return HttpResponseRedirect('/'+type+'/'+siteid)
    return HttpResponseRedirect('/login/')

def jtid_add(request):
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            if request.method == 'POST':
                form = Jituanform(request.POST)
                if form.is_valid():
                    trace_add(form,request.user.username)
                    form.save()
                    return HttpResponseRedirect('/jtid/')
            form = Jituanform() 
            return render(request,'noc/jtidadd.html',{'form':form})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def cid_add(request):
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            if request.method == 'POST':
                form = Cidform(request.POST)
                if form.is_valid():
                    m=form.save(commit=False)
                    if m.sales.endswith('@fnetlink.com'):
                        cid = request.POST['cid']
                        trace_add(form,request.user.username)
                        form.save()
                        return HttpResponseRedirect('/cid/'+cid)
                    else:
                        error = "业务员邮箱格式错误"
                        return render(request,'noc/cidadd.html',{'form':form,'error':error,'newcid':request.POST['cid']})
            form = Cidform()
            form.fields['jtid'].initial = Jituan.objects.filter(jtid=1000)[0].jtid
            try: 
               max_id = Cid.objects.filter(jtid_id=1000).order_by("-cid")[0].cid
            except:             
               newcid=8000
            else:
               newcid=max_id+1
            return render(request,'noc/cidadd.html',{'form':form,'newcid':newcid})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def cid_edit(request,id):
    cid = clscid(id)
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            Modelsurl = get_object_or_404(Cid,pk=id)
            if request.method == 'POST':
                form = Cidform(request.POST,instance=Modelsurl)
                if form.is_valid():
                    m=form.save(commit=False)
                    if m.sales.endswith('@fnetlink.com'):
                        trace_edit(form,get_object_or_404(Cid,pk=id),request.user.username)
                        form.save()
                        return HttpResponseRedirect('/cid/'+id)
                    else:
                        error = "业务员邮箱格式错误"
                        return render(request,'noc/cidedit.html',{'form':form,'error':error,'newcid':request.POST['cid'],'cid':cid})
            form = Cidform(instance=Modelsurl)
            return render(request,'noc/cidedit.html',{'form':form,'newcid':id,'cid':cid})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def site_add(request,id):
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            if request.method == 'POST':
                request.POST=request.POST.copy()
                request.POST['siteid']=id+request.POST['siteid']
                form = Siteform(request.POST)
                if form.is_valid():
                    trace_add(form,request.user.username)
                    form.save()
                    return HttpResponseRedirect('/cid/'+id+'/?collapse='+request.POST['siteid'])
                else:
                    return render(request,'noc/siteadd.html',locals())
            form = Siteform()
            form.fields['cid'].queryset = Cid.objects.filter(cid=id)
            form.fields['cid'].initial = Cid.objects.filter(cid=id)[0].cid
            return render(request,'noc/siteadd.html',{'form':form})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def site_edit(request,id):
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            Modelsurl = get_object_or_404(Site,pk=id)
            cid = Modelsurl.cid
            if request.method == 'POST':
                form = Siteform(request.POST,instance=Modelsurl)
                if form.is_valid():
                    trace_edit(form,get_object_or_404(Site,pk=id),request.user.username)
                    form.save()
                    return HttpResponseRedirect('/cid/'+str(cid.cid)+'/?collapse='+id)
            form = Siteform(instance=Modelsurl)
            return render(request,'noc/siteedit.html',{'form':form,'siteid':id,'cid':cid})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def photo(request,id):
    if request.user.is_authenticated:
        form = Photoform
        imageurl = Siteimage.objects.filter(siteid=id)
        if request.method == "POST":
            photoform = Photoform(request.POST, request.FILES)
            if photoform.is_valid():
                photo = Siteimage()
                photo.siteid = photoform.cleaned_data["siteid"]
                photo.uploader = request.user
                photo.imageurl = photoform.cleaned_data["imageurl"]
                photo.save()
            else:
                return HttpResponseRedirect('/photo/'+id)
            return HttpResponseRedirect('/photo/'+id)
        return render(request,'parent/base_photo.html',{'form':form,'imageurl':imageurl,'id':id})
    return HttpResponseRedirect('/login/')

def report(request,id):
    if request.user.is_authenticated:
        form = Reportform
        fileurl = Sitereport.objects.filter(siteid=id)
        if request.method == "POST":
            reportform = Reportform(request.POST, request.FILES)
            if reportform.is_valid():
                report = Sitereport()
                report.siteid = reportform.cleaned_data["siteid"]
                report.filename = reportform.cleaned_data["fileurl"].name
                report.uploader = request.user
                report.fileurl = reportform.cleaned_data["fileurl"]
                report.save()
            else:
                return HttpResponseRedirect('/report/'+id)
            return HttpResponseRedirect('/report/'+id)
        return render(request,'parent/base_report.html',{'form':form,'fileurl':fileurl,'id':id})
    return HttpResponseRedirect('/login/')

def svc_add(request,svc,id):
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            portformat=True
            if request.method == 'POST':
                Modelsurl = get_object_or_404(Site,pk=id)
                cid = Modelsurl.cid.cid
                request.POST=request.POST.copy()
                if svc == 'fast':
                    request.POST['svcid']=id+request.POST['svcid']
                    form = Fastform(request.POST)
                elif svc == 'flan':
                    request.POST['svcid']=id+request.POST['svcid']
                    form = Flanform(request.POST)
                elif svc == 'local':
                    request.POST['svcid']=id+request.POST['svcid']
                    form = Localform(request.POST)
                elif svc == 'nni':
                    request.POST['svcid']=id+request.POST['svcid']
                    form = NNIform(request.POST)
                elif svc == 'si':
                    request.POST['svcid']=id+request.POST['svcid']
                    form = Siform(request.POST)
                elif svc == 'monitor':
                    request.POST['svcid']=id+request.POST['svcid']
                    form = Monitorform(request.POST)
                if form.is_valid():
                    m=form.save(commit=False)
                    if svc == 'fast':
                        if 'tun' in m.fastport.lower():
                            if re.compile(r'^Tunnel\d+$').match(m.fastport):
                                portformat=True
                            elif re.compile(r'^vtun\d+$').match(m.fastport):
                                portformat=True
                            elif re.compile(r'^tun\d+$').match(m.fastport):
                                portformat=True
                            else:
                                portformat=False
                        else:
                            portformat=True
                    elif svc == 'flan':
                        if 'tun' in m.flanport.lower():
                            if re.compile(r'^Tunnel\d+$').match(m.flanport):
                                portformat=True
                            elif re.compile(r'^vtun\d+$').match(m.flanport):
                                portformat=True
                            elif re.compile(r'^tun\d+$').match(m.flanport):
                                portformat=True
                            else:
                                portformat=False
                        else:
                            portformat=True
                    else:
                        portformat=True
                    if portformat:
                        trace_add(form,request.user.username)
                        form.save()
                        return HttpResponseRedirect('/cid/'+str(cid)+'/?collapse='+Modelsurl.siteid)
                    else:
                        return render(request,'noc/svcadd.html',locals())
                else:
                    return render(request,'noc/svcadd.html',locals())
            if svc == 'fast':
                form = Fastform()
            elif svc == 'flan':
                form = Flanform()
            elif svc == 'local':
                form = Localform()
            elif svc == 'nni':
                form = NNIform()
            elif svc == 'si':
                form = Siform()
            elif svc == 'monitor':
                form = Monitorform()
            else:
                form = ""
            if form:
                form.fields['siteid'].queryset = Site.objects.filter(siteid=id)
                form.fields['siteid'].initial = Site.objects.filter(siteid=id)[0].siteid
                return render(request,'noc/svcadd.html',{'form':form,'portformat':portformat})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def svc_edit(request,svc,id):
    portformat=True
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            if svc == 'fast':
                Modelsurl = get_object_or_404(Fastline,pk=id)
                mb = get_object_or_404(Fastline,pk=id)
            elif svc == 'flan':
                Modelsurl = get_object_or_404(Flanline,pk=id)
                mb = get_object_or_404(Flanline,pk=id)
            elif svc == 'local':
                Modelsurl = get_object_or_404(Localline,pk=id)
                mb = get_object_or_404(Localline,pk=id)
            elif svc == 'nni':
                Modelsurl = get_object_or_404(NNIline,pk=id)
                mb = get_object_or_404(NNIline,pk=id)
            elif svc == 'si':
                Modelsurl = get_object_or_404(Siline,pk=id)
                mb = get_object_or_404(Siline,pk=id)
            elif svc == 'monitor':
                Modelsurl = get_object_or_404(Monitorline,pk=id)
                mb = get_object_or_404(Monitorline,pk=id)
            else:
                Modelsurl = ""
            cidnumber = Modelsurl.siteid.cid.cid
            cid = clscid(cidnumber)
            if request.method == 'POST':
                if svc == 'fast':
                    form = Fastform(request.POST,instance=Modelsurl)
                elif svc == 'flan':
                    form = Flanform(request.POST,instance=Modelsurl)
                elif svc == 'local':
                    form = Localform(request.POST,instance=Modelsurl)
                elif svc == 'nni':
                    form = NNIform(request.POST,instance=Modelsurl)
                elif svc == 'si':
                    form = Siform(request.POST,instance=Modelsurl)
                elif svc == 'monitor':
                    form = Monitorform(request.POST,instance=Modelsurl)
                if form.is_valid():
                    m=form.save(commit=False)
                    if svc == 'fast':
                        if 'tun' in m.fastport.lower():
                            if re.compile(r'^Tunnel\d+$').match(m.fastport):
                                portformat=True
                            elif re.compile(r'^vtun\d+$').match(m.fastport):
                                portformat=True
                            elif re.compile(r'^tun\d+$').match(m.fastport):
                                portformat=True
                            else:
                                portformat=False
                        else:
                            portformat=True
                    elif svc == 'flan':
                        if 'tun' in m.flanport.lower():
                            if re.compile(r'^Tunnel\d+$').match(m.flanport):
                                portformat=True
                            elif re.compile(r'^vtun\d+$').match(m.flanport):
                                portformat=True
                            elif re.compile(r'^tun\d+$').match(m.flanport):
                                portformat=True
                            else:
                                portformat=False
                        else:
                            portformat=True
                    else:
                        portformat=True
                    if portformat:
                        trace_edit(form,mb,request.user.username)
                        form.save()
                        return HttpResponseRedirect('/cid/'+str(cidnumber)+'/?collapse='+Modelsurl.siteid.siteid)
                    else:
                        return render(request,'noc/svcedit.html',locals())
                else:
                    return render(request,'noc/svcedit.html',locals())
            if svc == 'fast':
                form = Fastform(instance=Modelsurl)
            elif svc == 'flan':
                form = Flanform(instance=Modelsurl)
            elif svc == 'local':
                form = Localform(instance=Modelsurl)
            elif svc == 'nni':
                form = NNIform(instance=Modelsurl)
            elif svc == 'si':
                form = Siform(instance=Modelsurl)
            elif svc == 'monitor':
                form = Monitorform(instance=Modelsurl)
            else:
                form = ""
            if form:
                return render(request,'noc/svcedit.html',{'form':form,'id':id,'cid':cid,'portformat':portformat})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def tag(request,svc,id):
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            if request.method == 'POST':
                request.POST=request.POST.copy()
                if svc == 'fast':
                    form = Fasttagform(request.POST)
                elif svc == 'flan':
                    form = Flantagform(request.POST)
                elif svc == 'local':
                    form = Localtagform(request.POST)
                elif svc == 'nni':
                    form = NNItagform(request.POST)
                elif svc == 'si':
                    form = Sitagform(request.POST)
                elif svc == 'monitor':
                    form = Monitortagform(request.POST)
                if form.is_valid():
                    trace_add(form,request.user.username)
                    form.save()
                    return HttpResponseRedirect('/tag/'+svc+'/'+id+'/')
                else:
                    return render(request,'noc/tag.html',locals())
            if svc == 'fast':
                tagdata = Fasttag.objects.filter(svcid=id).all()
                svcdata = Fastline.objects.get(svcid=id)
                form = Fasttagform()
                form.fields['svcid'].queryset = Fastline.objects.filter(svcid=id)
            elif svc == 'flan':
                tagdata = Flantag.objects.filter(svcid=id).all()
                svcdata = Flanline.objects.get(svcid=id)
                form = Flantagform()
                form.fields['svcid'].queryset = Flanline.objects.filter(svcid=id)
            elif svc == 'local':
                tagdata = Localtag.objects.filter(svcid=id).all()
                svcdata = Localline.objects.get(svcid=id)
                form = Localtagform()
                form.fields['svcid'].queryset = Localline.objects.filter(svcid=id)
            elif svc == 'nni':
                tagdata = NNItag.objects.filter(svcid=id).all()
                svcdata = NNIline.objects.get(svcid=id)
                form = NNItagform()
                form.fields['svcid'].queryset = NNIline.objects.filter(svcid=id)
            elif svc == 'si':
                tagdata = Sitag.objects.filter(svcid=id).all()
                svcdata = Siline.objects.get(svcid=id)
                form = Sitagform()
                form.fields['svcid'].queryset = Siline.objects.filter(svcid=id)
            elif svc == 'monitor':
                tagdata = Monitortag.objects.filter(svcid=id).all()
                svcdata = Monitorline.objects.get(svcid=id)
                form = Monitortagform()
                form.fields['svcid'].queryset = Monitorline.objects.filter(svcid=id)
            else:
                svcdata = ""
            if svcdata:
                return render(request,'noc/tag.html',{'svc':svc,'svcdata':svcdata,'tagdata':tagdata,'form':form})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

def history(request):
    if request.user.is_authenticated:
        if request.user.has_perm('tellme.change_noc'):
            if 'q' in request.GET:
                q = request.GET['q']
                if q:
                    data = Traceentry.objects.filter(objpk__icontains=q)
                else:
                    error = True
                    return render(request,'noc/history.html',{'error':error})
            else:
                data = Traceentry.objects.all()
            room = paging(data,request.GET.get('page','1'))
            return render(request,'noc/history.html',{'room':room,'data':data})
        else:
            return render(request,'index.html')
    return HttpResponseRedirect('/login/')

