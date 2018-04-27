from tellme.models import Flanline,Flantag

class clsflan:
    def __init__(self,svcid):
        self.svcid = svcid
        self.objstate = False
        self.flantag = []
        flaninfo = Flanline.objects.filter(svcid=self.svcid)
        for flan in flaninfo:
            self.objstate = True
            self.flanpe = flan.flanpe
            self.flanport = flan.flanport
            self.flanwanip = flan.flanwanip
            self.lanip = flan.lanip
            self.bandwidth = flan.bandwidth
            self.bkpe = flan.bkpe
            self.bkport = flan.bkport
            self.bkwanip = flan.bkwanip
            self.servicenumber = flan.servicenumber
            self.status = flan.status
            self.create_date = flan.create_date
            self.mod_date = flan.mod_date
            self.gettags()

    def gettags(self):
        tags = Flantag.objects.filter(svcid=self.svcid)
        for tag in tags:
            self.flantag.append([tag.tagname, tag.tagvalue])
