from tellme.models import Siline,Sitag

class clssi:
    def __init__(self,svcid):
        self.svcid = svcid
        self.objstate = False
        self.sitag = []
        siinfo = Siline.objects.filter(svcid=self.svcid)
        for si in siinfo:
            self.objstate = True
            self.siname = si.siname
            self.sicontent = si.sicontent
            self.servicenumber = si.servicenumber
            self.contractnumber = si.contractnumber
            self.status = si.status
            self.create_date = si.create_date
            self.mod_date = si.mod_date
            self.gettags()

    def gettags(self):
        tags = Sitag.objects.filter(svcid=self.svcid)
        for tag in tags:
            self.sitag.append([tag.tagname, tag.tagvalue])
