# coding=utf-8

from django.db.models.fields.related import ForeignKey
from tellme.models import Traceentry

def trace_del(ins,user):
    try:
        mname = ins.__class__.__name__
        pkid = ""
        change_fields = {}
        for field in ins._meta.fields:
            if field.name in ['create_date','mod_date']:
                continue
            if str(getattr(ins,field.name,None)):
                if ins._meta.get_field(field.name).primary_key:
                    pkid = str(getattr(ins,field.name,None))
                elif field.name == 'svcid':
                    pkid = str(getattr(ins,field.name,None)).split()[-1]
                    print(pkid)
                elif not isinstance(ins._meta.get_field(field.name),ForeignKey):
                    change_fields[field.name] = {
                        'new':'',
                        'old':str(getattr(ins,field.name,None)),
                    }
        if change_fields:
            entry = Traceentry(objname=mname,objpk=pkid,type='Del',context=change_fields,oprater=user)
            entry.save()
    except:
        return 0

def trace_edit(f,ins,user):
    try:
        M = f.instance.__class__
        mname = M.__name__
        pkid = ""
        change_fields = {}
        for field in M._meta.fields:
            if field.name in ['create_date','mod_date']:
                continue
            if M._meta.get_field(field.name).primary_key:
                pkid = str(f.cleaned_data[field.name])
            elif str(f.cleaned_data[field.name]) != str(getattr(ins,field.name,None)):
                change_fields[field.name] = {
                    'new':str(f.cleaned_data[field.name]),
                    'old':str(getattr(ins,field.name,None)),
                }
        if change_fields:
            entry = Traceentry(objname=mname,objpk=pkid,type='Edit',context=change_fields,oprater=user)
            entry.save()
    except:
        return 0

def trace_add(f,user):
    try:
        M = f.instance.__class__
        mname = M.__name__
        pkid = ""
        change_fields = {}
        for field in M._meta.fields:
            if field.name in ['create_date','mod_date','id']:
                continue
            if f.cleaned_data[field.name]:
                if M._meta.get_field(field.name).primary_key:
                    pkid = str(f.cleaned_data[field.name])
                elif field.name == 'svcid':
                    pkid = str(f.data['svcid'])
                elif not isinstance(M._meta.get_field(field.name),ForeignKey):
                    change_fields[field.name] = {
                        'new':str(f.cleaned_data[field.name]),
                        'old':'',
                    }
        if change_fields:
            entry = Traceentry(objname=mname,objpk=pkid,type='Add',context=change_fields,oprater=user)
            entry.save()
    except:
        return 0

def abc(f,t,user):
    c = ""
    pkid = ""
    name = f.instance.__class__.__name__
    for key in f.cleaned_data:
        if 'id' in key:
            pkid = str(f.cleaned_data[key])
        elif key != 'create_date':
            c += key +':'+ str(f.cleaned_data[key]) +';'
    entry = Traceentry(objname=name,objpk=pkid,type=t,context=c,oprater=user)
    entry.save()
