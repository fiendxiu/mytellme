from tellme.models import Monitorline,Monitortag

class clsmonitor:
    def __init__(self,svcid):
        self.svcid = svcid
        self.objstate = False
        self.monitortag = {}
        monitorinfo = Monitorline.objects.filter(svcid=self.svcid)
        for monitor in monitorinfo:
            self.objstate = True
            self.monitorobj = monitor.monitorobj
            self.monitorip = monitor.monitorip
            self.status = monitor.status
            self.create_date = monitor.create_date
            self.mod_date = monitor.mod_date
            self.gettags()

    def gettags(self):
        tags = Monitortag.objects.filter(svcid=self.svcid)
        for tag in tags:
            self.monitortag[tag.tagname] = tag.tagvalue
