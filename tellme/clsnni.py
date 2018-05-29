from tellme.models import NNIline,NNItag

class clsnni:
    def __init__(self,svcid):
        self.svcid = svcid
        self.objstate = False
        self.nnitag = []
        nniinfo = NNIline.objects.filter(svcid=self.svcid)
        for nni in nniinfo:
            self.objstate = True
            self.pe = nni.pe
            self.port = nni.port
            self.wanip = nni.wanip
            self.bandwidth = nni.bandwidth
            self.nnisp = nni.nnisp
            self.nniname = nni.nniname
            self.nniguard = nni.nniguard
            self.nniaddr = nni.nniaddr
            self.nninumber = nni.nninumber
            self.servicenumber = nni.servicenumber
            self.engineer = nni.engineer
            self.create_date = nni.create_date
            self.mod_date = nni.mod_date
            self.gettags()

    def gettags(self):
        tags = NNItag.objects.filter(svcid=self.svcid)
        for tag in tags:
            self.nnitag.append([tag.tagname, tag.tagvalue])
