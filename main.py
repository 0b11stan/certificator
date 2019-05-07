import sys
import json
import utils

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
        return json.dumps(utils.list_certificates(state=request.args.get('filter')))
    elif request.method == 'POST':
        current_identity.create_cert_request(request.get_data().decode('utf-8'))
        return Response("success", status=200)


@app.route("/cert/<cert_id>", methods=['GET', 'DELETE'])
@jwt_required()
def certificate_details(cert_id):
    if request.method == 'GET':
        return json.dumps(utils.detail_certificate(cert_id))
    elif request.method == 'DELETE':
        revoke_certificates(cert_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)
