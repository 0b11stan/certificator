import sys
import json
import utils
import cert_utils

from flask import request, Response
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app  = utils.init_flask()
ldap = utils.init_ldap(app)
jwt  = utils.init_jwt(app, ldap)


@app.route("/")
@jwt_required()
def index():
    return "%s\n" % current_identity


@app.route("/cert", methods=['GET', 'POST'])
@jwt_required()
def certificates():

    if request.method == 'GET':
        body = json.dumps(utils.list_certificates(state=request.args.get('filter')))
        return Response(body, status=200)

    elif request.method == 'POST':
        current_identity.create_cert_request(request.get_data().decode('utf-8'))
        return Response("created", status=201)


@app.route("/cert/<cert_id>", methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def certificate_details(cert_id):

    if request.method == 'GET':
        csr = cert_utils.get_pending_cert(cert_id)
        body = json.dumps(cert_utils.detail_csr(csr))
        return Response(body, status=200)

    elif request.method == 'POST':
        if 'Domain Admins' in current_identity.groups:
            client_csr = cert_utils.get_pending_cert(cert_id)
            ca_private_key = cert_utils.get_ca_private_key()
            ca_cert = cert_utils.get_ca_cert()
            cert_utils.create_certificate(ca_private_key, ca_cert, client_csr)
            return Response(status=204)
        else: return Response("forbidden", status=403)

    elif request.method == 'DELETE':
        revoke_certificates(cert_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)
