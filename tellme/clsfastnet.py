from tellme.models import Fastnetline,Fastnettag

class clsfastnet:
    def __init__(self,svcid):
        self.svcid = svcid
        self.objstate = False
        self.fastnettag = []
        fastnetinfo = Fastnetline.objects.filter(svcid=self.svcid)
        for fastnet in fastnetinfo:
            self.objstate = True
            self.pe = fastnet.pe
            self.usedip = fastnet.usedip
            self.domain = fastnet.domain
            self.description = fastnet.description
            self.servicenumber = fastnet.servicenumber
            self.create_date = fastnet.create_date
            self.mod_date = fastnet.mod_date
            self.gettags()

    def gettags(self):
        tags = Fastnettag.objects.filter(svcid=self.svcid)
        for tag in tags:
            self.fastnettag.append([tag.tagname, tag.tagvalue])
