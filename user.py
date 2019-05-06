import time
import os
import utils

from enum import Enum

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

    def create_cert_request(self, content):
        path = "certificates/pending/" + self.id + "_" + int(time.time()) + ".csr"
        f = open(utils.absolute_path(path), "w+")
        f.write(content)
        f.close()

