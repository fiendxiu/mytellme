from tellme.models import Localline,Localtag

class clslocal:
    def __init__(self,svcid):
        self.svcid = svcid
        self.objstate = False
        self.localtag = []
        localinfo = Localline.objects.filter(svcid=self.svcid)
        for local in localinfo:
            self.objstate = True
            self.localsp = local.localsp
            self.localname = local.localname
            self.localguard = local.localguard
            self.localaddra = local.localaddra
            self.localaddrb = local.localaddrb
            self.bandwidth = local.bandwidth
            self.servicenumber = local.servicenumber
            self.contractnumber = local.contractnumber
            self.localnumber = local.localnumber
            self.status = local.status
            self.create_date = local.create_date
            self.mod_date = local.mod_date
            self.gettags()

    def gettags(self):
        tags = Localtag.objects.filter(svcid=self.svcid)
        for tag in tags:
            self.localtag.append([tag.tagname, tag.tagvalue])
