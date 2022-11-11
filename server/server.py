import threading

from flask import Flask
from flask_sockets import Sockets, Rule
from storage.init_db import init_postgres

init_postgres()

from handlers.data_handler import ClientDataHandler
from service.authorization import Authorization
from api.auth import client
from api.server_self_status import self_server
from config.logger_config import logger
from config.settings import settings
from handlers.ws_message_handler import WebSocketMessageHandler
from server_state import write_server_system_load

app = Flask(__name__)
sockets = Sockets(app)

app.register_blueprint(self_server)
app.register_blueprint(client)


@app.route("/")
def welcome() -> str:
    return "<p>Welcome</p>"


@sockets.route("/echo", websocket=True)
def echo_socket(
    ws,
    auth: Authorization = Authorization(),
    data_handler: ClientDataHandler = ClientDataHandler(),
):
    """Open and handle websocket connections"""

    handler = WebSocketMessageHandler(ws, auth, data_handler)
    while not ws.closed:
        client_request = handler.receive()
        if client_request is None:
            continue
        handler.handle(client_request)


if __name__ == "__main__":
    thread_cpu_info = threading.Thread(
        target=write_server_system_load, daemon=True
    )
    thread_cpu_info.start()
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(
        (settings.app.host, settings.app.port),
        app,
        handler_class=WebSocketHandler,
    )
    sockets.url_map.add(Rule("/echo", endpoint=echo_socket, websocket=True))
    logger.info("app run")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
