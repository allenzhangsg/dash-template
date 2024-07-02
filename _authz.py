import json
import logging
import os
from urllib.parse import urlparse

from werkzeug.wrappers import Request, Response

# user access control stored as an environment variable
# example: {"dashboard1":{"user":[], "group":[]}, ...}
access_control: str = os.getenv("ACCESS_CONTROL")

if not access_control:
    logging.error("Unable to load the access control list. Exiting...")
    exit(-1)

access_control: dict = json.loads(access_control)


class AuthMiddleware:
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        user = request.headers.get("x-user")
        group = request.headers.get("x-group")

        request_path = request.path.strip("/").split("/")[-1]
        if request.referrer is not None:
            referrer_path = urlparse(request.referrer).path.strip("/").split("/")[-1]
        else:
            referrer_path = ""

        # for dashboards under protection
        if (request_path == "_dash-update-component" and referrer_path in access_control.keys()
                or request_path in access_control.keys()):
            dashboard_path = referrer_path if request_path == "_dash-update-component" else request_path
            users_allowed = access_control[dashboard_path]
            groups_allowed = access_control[dashboard_path]
            if user in users_allowed or group in groups_allowed:
                return self._app(environ, start_response)
            else:
                res = Response("Authorization failed", status=401)
                return res(environ, start_response)
        # for other kind of requests
        else:
            return self._app(environ, start_response)
