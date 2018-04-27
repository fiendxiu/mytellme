import os
from tellme.models import Site,Fastline,Flanline,Localline,NNIline,Siline,Fastnetline,Monitorline
from tellme.clsfast import clsfast
from tellme.clsflan import clsflan
from tellme.clslocal import clslocal
from tellme.clsnni import clsnni
from tellme.clssi import clssi
from tellme.clsfastnet import clsfastnet
from tellme.clsmonitor import clsmonitor

class clssite:
    def __init__(self,siteid):
        self.siteid = siteid
        self.objstate = False
        self.images = self.getimages(siteid)
        self.fast = []
        self.flan = []
        self.local = []
        self.nni = []
        self.si = []
        self.fastnet = []
        self.monitor = []
        siteinfo = Site.objects.filter(siteid=self.siteid)
        for site in siteinfo:
            self.objstate = True
            self.sitename = site.sitename
            self.siteaddr = site.siteaddr
            self.mastercontact = site.mastercontact
            self.masterphone = site.masterphone
            self.masteremail = site.masteremail
            self.ocontacts = site.ocontacts
            self.status = site.status
            self.create_date = site.create_date
            self.mod_date = site.mod_date
            self.getservices()

    def getimages(self,siteid):
        imagenum = 0
        path = "static/image/"+siteid+"/"
        try:
            for image in os.listdir(path):
                imagepath = os.path.join(path,image)
                if os.path.isfile(imagepath):
                    imagenum += 1
            return imagenum
        except:
            return imagenum

    def getservices(self):
        fastinfo = Fastline.objects.filter(siteid=self.siteid)
        for fast in fastinfo:
            self.fast.append(clsfast(fast.svcid))

        flaninfo = Flanline.objects.filter(siteid=self.siteid)
        for flan in flaninfo:
            self.flan.append(clsflan(flan.svcid))

        localinfo = Localline.objects.filter(siteid=self.siteid)
        for local in localinfo:
            self.local.append(clslocal(local.svcid))

        nniinfo = NNIline.objects.filter(siteid=self.siteid)
        for nni in nniinfo:
            self.nni.append(clsnni(nni.svcid))

        siinfo = Siline.objects.filter(siteid=self.siteid)
        for si in siinfo:
            self.si.append(clssi(si.svcid))

        fastnetinfo = Fastnetline.objects.filter(siteid=self.siteid)
        for fastnet in fastnetinfo:
            self.fastnet.append(clsfastnet(fastnet.svcid))

        monitorinfo = Monitorline.objects.filter(siteid=self.siteid)
        for monitor in monitorinfo:
            self.monitor.append(clsmonitor(monitor.svcid))
