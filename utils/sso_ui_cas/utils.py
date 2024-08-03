import os
import json
from utils.sso_ui_cas.cas import CASClient
from urllib.parse import urlunparse

SSO_UI_URL = "https://sso.ui.ac.id/cas2/"
SSO_UI_FORCE_SERVICE_HTTPS = False

def normalize_username(username):
    return username.lower()


def get_protocol(request):
    if request.url.is_secure or SSO_UI_FORCE_SERVICE_HTTPS:
        return "https"

    return "http"


def get_service_url(request):
    protocol = get_protocol(request)
    host = request.url.hostname
    port = request.url.port
    uri = host + ":" + str(port)
    service = urlunparse((protocol, uri, request.url.path, "", "", ""))

    return service


def get_cas_client(service_url=None, request=None):
    server_url = SSO_UI_URL
    if server_url and request and server_url.startswith("/"):
        scheme = request.headers.get("X-Forwarded-Proto", request.url.scheme)
        server_url = scheme + "://" + request.headers["host"] + server_url

    return CASClient(service_url=service_url, server_url=server_url, version=2)


def authenticate(ticket, client):
    username, attributes, _ = client.verify_ticket(ticket)

    if not username:
        return None

    if "kd_org" in attributes:
        attributes.update(get_additional_info(attributes["kd_org"]) or {})

    sso_profile = {"username": username, "attributes": attributes}
    return sso_profile


def get_additional_info(kd_org):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path, "additional-info.json")

    with open(filename, "r") as fd:
        as_json = json.load(fd)
        if kd_org in as_json:
            return as_json[kd_org]

    return None