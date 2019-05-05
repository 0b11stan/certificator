import datetime
import os

from enum import Enum
from utils import listfiles

class CertState(Enum):
    PENDING = 'PENDING'
    ISSUED  = 'ISSUED'
    REVOKED = 'REVOKED'

class User(object):

    def __init__(self, id, groups):
        self.id = id
        self.groups = groups

    def __str__(self):
        return "username : {}\ngroups : {}".format(self.id, self.groups)

    def create_certificates(self, content):
        script_dir = os.path.dirname(__file__)
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        rel_path = "certificates/pending/" + self.id + "_" + date + ".csr"
        abs_file_path = os.path.join(script_dir, rel_path)
        f = open(abs_file_path, "w+")
        f.write(content)
        f.close()

    def list_certificates(self, state=None):
        if CertState.PENDING.value == state:
            return listfiles('certificates/pending')
        elif CertState.ISSUED.value == state:
            return listfiles('certificates/issued')
        elif CertState.REVOKED.value == state:
            return listfiles('certificates/revoked')
        else:
            return [
                self.list_certificates(CertState.PENDING.value),
                self.list_certificates(CertState.ISSUED.value),
                self.list_certificates(CertState.REVOKED.value)
            ]
