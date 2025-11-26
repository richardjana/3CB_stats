import requests
from flask import Blueprint, request, Response

# Streamlit server location (internal, same container)
STREAMLIT_URL = "http://localhost:8501"

reverse_proxy = Blueprint("reverse_proxy", __name__)

@reverse_proxy.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@reverse_proxy.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    # Forward the incoming request to Streamlit
    url = f"{STREAMLIT_URL}/{path}"

    # Forward headers except Host (Streamlit handles its own host)
    headers = {key: value for key, value in request.headers if key.lower() != "host"}

    # Forward request based on method
    resp = requests.request(
        method=request.method,
        url=url,
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        headers=headers,
        stream=True,
    )

    # Filter out headers that would break Flask's Response object
    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    response_headers = [
        (name, value) for name, value in resp.raw.headers.items()
        if name.lower() not in excluded
    ]

    # Return proxied response
    return Response(
        resp.raw,
        status=resp.status_code,
        headers=response_headers
    )

