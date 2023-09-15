import json

from flask import Flask, jsonify, request
from uuid import uuid4


app = Flask(__name__)


ALLOWED_OAUTH2_SCOPES = ["xapi:write"]


def error_json(message, status=400):
    response = jsonify({"status": "error", "message": message})
    response.status = status
    return response


@app.route("/")
def index():
    return "edcast-mock"


@app.route("/api/lrs/v1/xapi/oauth2/token", methods=["POST"])
def get_oauth2_token():
    if request.form["scope"] not in ALLOWED_OAUTH2_SCOPES:
        return error_json(
            "Invalid Scope. Only supports " + ",".join(ALLOWED_OAUTH2_SCOPES)
        )
    if request.form["grant_type"] != "client_credentials":
        return error_json("Invalid Grant type. Only supports `client_credentials`.")

    client_id = request.form["client_id"]
    client_secret = request.form["client_secret"]
    app.logger.info(
        "OAuth2 Token requested by client with ID: %s Secret: %s",
        client_id,
        client_secret,
    )

    return jsonify(
        {
            "access_token": str(uuid4()).replace("-", ""),
            "token_type": "bearer",
            "expires_in": 3600,
        }
    )


@app.route("/api/lrs/v1/xapi/statements", methods=["POST"])
def xapi_statements():
    if (
        not request.authorization
        or not request.authorization.token
        or not request.authorization.type == "bearer"
    ):
        return error_json("Missing Bearer Token in authorization.", 401)

    xapi_statement = request.get_json()
    if not xapi_statement:
        return error_json("No xAPI statement recieved.", 400)

    app.logger.info("Received xAPI Statement: %s", json.dumps(xapi_statement, indent=2))
    response = jsonify({"message": "Successfully inserted"})
    response.status_code = 201
    return response
