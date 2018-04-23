from tellme.models import Cid,Site
from tellme.clssite import clssite
import os

class clscid:
    def __init__(self,cid):
        self.cid = cid
        self.objstate = False
        self.site = []
        self.reports = self.getreports(cid)
        cidinfo = Cid.objects.filter(cid=self.cid)
        for cids in cidinfo:
            self.objstate = True
            self.contractname = cids.contractname
            self.installname = cids.installname
            self.jtid = cids.jtid
            self.sales = cids.sales
            self.mrtg = cids.mrtg
            self.mrtgpass = cids.mrtgpass
            self.netflow = cids.netflow
            self.netflowpass = cids.netflowpass
            self.apppass = cids.apppass
            self.status = cids.status
            self.create_date = cids.create_date
            self.mod_date = cids.mod_date
            self.getsiteinfo()

    def getsiteinfo(self):
        siteinfo = Site.objects.filter(cid=self.cid)
        for site in siteinfo:
            self.site.append(clssite(site.siteid))

    def getreports(self,cid):
        reportnum = 0
        path = "static/report/"+str(cid)+"/"
        try:
            for report in os.listdir(path):
                reportpath = os.path.join(path,report)
                if os.path.isfile(reportpath):
                    reportnum += 1
            return reportnum
        except:
            return reportnum
