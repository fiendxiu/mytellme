from django import forms
from django.forms import ModelForm,Textarea,Select
from django.forms.fields import ChoiceField
from tellme.models import Jituan,Cid,Site,Fastline,Flanline,Localline,NNIline,Siline,Fastnetline,Monitorline,Fasttag,Flantag,Localtag,NNItag,Sitag,Fastnettag,Monitortag,Traceentry

SITEID=[]
ZM=['_A','_B','_C','_D','_E','_F','_G','_H','_I','_J','_K','_L','_M','_N','_O','_P','_Q','_R','_S','_T','_U','_V','_W','_X','_Y','_Z','_Aa','_Ab','_Ac','_Ad','_Ae','_Af','_Ag','_Ah','_Ai','_Aj','_Ak','_Al','_Am','_An','_Ao','_Ap','_Aq','_As','_At','_Au','_Av','_Aw','_Ax','_Ay','_Az','_Ba','_Bb','_Bc','_Bd','_Be','_Bf','_Bg','_Bh','_Bi','_Bj','_Bk','_Bl','_Bm','_Bn','_Bo','_Bp','_Bq','_Br','_Bs','_Bt','_Bu','_Bv','_Bw','_Bx','_By','_Bz']
for zm in ZM :
   SITEID.append((zm,zm))

FASTID=[]
FLANID=[]
LOCALID=[]
NNIID=[]
SIID=[]
FASTNETID=[]
MONITORID=[]
IDS=range(1,100)
for id in IDS:
    FASTID.append(('_F'+str(id),'_F'+str(id)))
    FLANID.append(('_M'+str(id),'_M'+str(id)))
    LOCALID.append(('_L'+str(id),'_L'+str(id)))
    NNIID.append(('_NNI'+str(id),'_NNI'+str(id)))
    SIID.append(('_SI'+str(id),'_SI'+str(id)))
    FASTNETID.append(('_FN'+str(id),'_FN'+str(id)))
    MONITORID.append(('_CM'+str(id),'_CM'+str(id)))

FASTPE=[]
FASTPES=['-','VPS','dga-fastip1','dga-fastip2','dgb-fastip1','dgb-fastip2','dgb-fastip3','dgb-flr1','dgb-flr2','dgb-bpflr1','szb-fastip1','szb-sfastip1','szb-flr1','szb-flr2','hkh-fastip1','hkh-flr1','hkh-flr2','hkh-us1','sza-flr3','sha-fastip1','sha-flr1','sha-flr2','sha-flr3','sha-flr4']
for pe in FASTPES:
    FASTPE.append((pe,pe))

FLANPE=[]
FLANPES=['-','dga-acvpnpe1','dga-vpnpe1','dgb-acvpnpe1','dgb-vpnpe1','sza-vpnpe1','szb-acvpnpe1','szb-vpnpe1','sha-acvpnpe1','sha-vpnpe1','hka-vpnpe1','hkh-acvpnpe1','hkh-vpnpe1','gza-vpnpe1','twb-vpnpe1','鹏博士PE']
for pe in FLANPES:
    FLANPE.append((pe,pe))

BKPE=[]
BKPES=['-','dga-vpnbk1','dgb-bk1','szb-bk1','鹏博士PE']
for bkpe in BKPES:
    BKPE.append((bkpe,bkpe))

FASTNETPE=[]
FASTNETPES=['-','dga-fastnet1','dgb-fastnet1']
for pe in FASTNETPES:
    FASTNETPE.append((pe,pe))

class Jituanform(ModelForm):
    class Meta:
        model = Jituan
        exclude = ['mod_date']

class Cidform(ModelForm):
    class Meta:
        model = Cid
        exclude = ['mod_date']

class Siteform(ModelForm):
    class Meta:
        model = Site
        exclude = ['mod_date']
        widgets = {
            'siteid': Select(choices=SITEID),
            'siteaddr': Textarea(attrs={'cols': 40, 'rows': 4}),
            'ocontacts': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class Photoform(forms.Form):
    siteid = forms.CharField(max_length=20)
    imageurl = forms.ImageField()

class Reportform(forms.Form):
    siteid = forms.CharField(max_length=20)
    fileurl = forms.FileField()

class Fastform(ModelForm):
    class Meta:
        model = Fastline
        exclude = ['mod_date']
        widgets = {
            'svcid': Select(choices=FASTID),
            'fastpe': Select(choices=FASTPE),
            'hkip': Textarea(attrs={'cols': 25, 'rows': 3}),
            'bkpe': Select(choices=BKPE),
        }

class Flanform(ModelForm):
    class Meta:
        model = Flanline
        exclude = ['mod_date']
        widgets = {
            'svcid': Select(choices=FLANID),
            'flanpe': Select(choices=FLANPE),
            'bkpe': Select(choices=BKPE),
            'lanip': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class Localform(ModelForm):
    class Meta:
        model = Localline
        exclude = ['mod_date']
        widgets = {
            'svcid': Select(choices=LOCALID),
        }

class NNIform(ModelForm):
    class Meta:
        model = NNIline
        exclude = ['mod_date']
        widgets = {
            'svcid': Select(choices=NNIID),
        }

class Siform(ModelForm):
    class Meta:
        model = Siline
        exclude = ['mod_date']
        widgets = {
            'svcid': Select(choices=SIID),
        }

class Fastnetform(ModelForm):
    class Meta:
        model = Fastnetline
        exclude = ['mod_date']
        widgets = {
            'svcid': Select(choices=FASTNETID),
            'pe': Select(choices=FASTNETPE),
        }

class Monitorform(ModelForm):
    class Meta:
        model = Monitorline
        exclude = ['mod_date']
        widgets = {
            'svcid': Select(choices=MONITORID),
        }

class Fasttagform(ModelForm):
    class Meta:
        model = Fasttag
        exclude = ['mod_date']
        widgets = {
            'tagname': Textarea(attrs={'cols': 40, 'rows': 1}),
            'tagvalue': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class Flantagform(ModelForm):
    class Meta:
        model = Flantag
        exclude = ['mod_date']
        widgets = {
            'tagname': Textarea(attrs={'cols': 40, 'rows': 1}),
            'tagvalue': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class Localtagform(ModelForm):
    class Meta:
        model = Localtag
        exclude = ['mod_date']
        widgets = {
            'tagname': Textarea(attrs={'cols': 40, 'rows': 1}),
            'tagvalue': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class NNItagform(ModelForm):
    class Meta:
        model = NNItag
        exclude = ['mod_date']
        widgets = {
            'tagname': Textarea(attrs={'cols': 40, 'rows': 1}),
            'tagvalue': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class Sitagform(ModelForm):
    class Meta:
        model = Sitag
        exclude = ['mod_date']
        widgets = {
            'tagname': Textarea(attrs={'cols': 40, 'rows': 1}),
            'tagvalue': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class Fastnettagform(ModelForm):
    class Meta:
        model = Fastnettag
        exclude = ['mod_date']
        widgets = {
            'tagname': Textarea(attrs={'cols': 40, 'rows': 1}),
            'tagvalue': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class Monitortagform(ModelForm):
    class Meta:
        model = Monitortag
        exclude = ['mod_date']
        widgets = {
            'tagname': Textarea(attrs={'cols': 40, 'rows': 1}),
            'tagvalue': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

class Traceform(ModelForm):
    class Meta:
        model = Traceentry
        fields = '__all__'
