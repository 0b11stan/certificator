from flask import Flask
from flask_simpleldap import LDAP
from flask_jwt import JWT
from user import User

def init_flask():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = "S3CR3T"
    return app

def init_ldap(app):
    app.config['LDAP_HOST'] = 'ad-crypto.epsi.intra'
    app.config['LDAP_BASE_DN'] = 'cn=Users,dc=epsi,dc=intra'
    app.config['LDAP_USERNAME'] = 'cn=Administrator,cn=Users,dc=epsi,dc=intra'
    app.config['LDAP_PASSWORD'] = 'P@ssw0rd'
    app.config['LDAP_USER_OBJECT_FILTER'] = '(sAMAccountName=%s)'
    return LDAP(app)

def init_jwt(app, ldap):

    def authenticate(username, password):
        binded = ldap.bind_user(username, password)
        if binded and password != '':
            user_groups = ldap.get_user_groups(user=username)
            user = User(username, user_groups)
            return user

    def identity(payload):
        user_name = payload['identity']
        user_groups = ldap.get_user_groups(user=user_name)
        return User(user_name, user_groups)

    return JWT(app, authenticate, identity)

def listfiles(path):
    with os.scandir(path) as directory:
        return [entry.name for entry in directory if entry.is_file()]

def list_certificates():
    if CertState.PENDING.value == state:
        return listfiles('certificates/pending')
    elif CertState.ISSUED.value == state:
        return listfiles('certificates/issued')
    elif CertState.REVOKED.value == state:
        return listfiles('certificates/revoked')
    elif state == None:
        return [
            list_certificates(CertState.PENDING.value),
            list_certificates(CertState.ISSUED.value),
            list_certificates(CertState.REVOKED.value)
        ]
