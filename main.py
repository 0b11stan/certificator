import sys
import json

from utils import init_flask, init_ldap, init_jwt, list_certificates

from flask import request
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app  = init_flask()
ldap = init_ldap(app)
jwt  = init_jwt(app, ldap)


@app.route("/")
@jwt_required()
def index():
    return "%s\n" % current_identity


@app.route("/cert", methods=['GET', 'POST'])
@jwt_required()
def certificates():
    if request.method == 'GET':
        return json.dumps(list_certificates(state=request.args.get('filter')))
    elif request.method == 'POST':
        content = json.loads(request.data['request'])
        current_identity.create_cert_request(content)
        return Response("success", status=200)


@app.route("/cert/<cert_id>", methods=['GET', 'DELETE'])
@jwt_required()
def certificate_details(cert_id):
    if request.method == 'GET':
        list_certificates(cert_id)
    elif request.method == 'DELETE':
        revoke_certificates(cert_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)
