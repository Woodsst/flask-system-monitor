from typing import Union

from flask import Blueprint, Response, request, jsonify

from config.logger_config import logger
from handlers.data_handler import ClientDataHandler
from handlers.request_handler import RequestHandler
from service.authorization import Authorization

client = Blueprint("client", __name__, url_prefix="/client")


@client.route("/<string:username>", methods=["POST"])
def route_for_client(
    username: str,
    auth: Authorization = Authorization(),
    data_handler: ClientDataHandler = ClientDataHandler(),
) -> Union[tuple[Response, int], tuple[any, int]]:
    """Route to POST request for added client data in database and return"""

    if auth.verification(request.headers.get("Authorization"), username):
        data = request.form.to_dict()
        if len(data) > 0:
            data_handler.write_client_data(data, username)
            return data_handler.to_json_for_client_data(data), 202
        logger.info("client - %s incorrect data size", username)
        return jsonify({"error": "incorrect data size"}), 400
    logger.info("authorization error %s", username)
    return jsonify({"error": "authorization error"}), 401


@client.route("/", methods=["POST"])
def client_registration(
    auth: Authorization = Authorization(),
) -> Response or dict:
    """Route to POST request for login,
    if the client is not registered, it registers"""

    username = request.get_json()["username"]
    password = request.get_json()["pass"]
    if username is None or len(username) == 0:
        return jsonify({"error": "unsupportable username"}), 401
    if not username[0].isalpha():
        return jsonify({"error": "unsupportable username"}), 401
    if auth.user_verification(username):
        client_id = auth.authorization(username=username, password=password)
        if client_id:
            logger.info("client: %s, authorization", username)
            return jsonify({"client_id": client_id})
        return jsonify({"error": "authorization error"}), 401
    client_id = auth.add_client(username, password)
    logger.info("client: %s, registered", username)
    return jsonify({"registration": username, "client_id": client_id})


@client.route("/<string:username>/time", methods=["POST"])
def client_log_time_work(
    username: str,
    auth: Authorization = Authorization(),
    request_handler: RequestHandler = RequestHandler(),
) -> Response:
    """Route to request for return logging time work"""

    if auth.verification(request.headers.get("Authorization"), username):
        response_js = request_handler.time_write_log(username)
        if response_js.get("error"):
            return jsonify(response_js), 406
        return jsonify(response_js), 200
    return jsonify({"error": "authorization error"}), 401


@client.route("/<string:username>/time/report", methods=["POST"])
def split_client_log(
    username: str,
    auth: Authorization = Authorization(),
    request_handler: RequestHandler = RequestHandler(),
) -> Response:
    """Route to request for return log slice"""

    if auth.verification(request.headers.get("Authorization"), username):
        start = request.args.get("start", "")
        end = request.args.get("end", "")
        if (len(end) and len(start)) == 0:
            start = 0
            end = 0
        try:
            payload = request_handler.client_log_request(
                username, int(start), int(end)
            )
        except ValueError:
            return jsonify({"error": "value error"}), 400
        return payload, 200
    return jsonify({"error": "authorization error"}), 401
