from tellme.models import Fastline,Fasttag

class clsfast:
    def __init__(self,svcid):
        self.svcid = svcid
        self.objstate = False
        self.fasttag = []
        fastinfo = Fastline.objects.filter(svcid=self.svcid)
        for fast in fastinfo:
            self.objstate = True
            self.fastpe = fast.fastpe
            self.fastport = fast.fastport
            self.fastwanip = fast.fastwanip
            self.hkip = fast.hkip
            self.bkpe = fast.bkpe
            self.bkport = fast.bkport
            self.bkwanip = fast.bkwanip
            self.bandwidth = fast.bandwidth
            self.servicenumber = fast.servicenumber
            self.contractnumber = fast.contractnumber
            self.engineer = fast.engineer
            self.status = fast.status
            self.create_date = fast.create_date
            self.mod_date = fast.mod_date
            self.gettags()

    def gettags(self):
        tags = Fasttag.objects.filter(svcid=self.svcid)
        for tag in tags:
            self.fasttag.append([tag.tagname, tag.tagvalue])
