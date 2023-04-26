import json
import os

import requests
from flask import Flask

app = Flask(__name__)

ALLOWED_SERVICES = ['b', 'c']


@app.route("/")
def health_check():
    return "Hi from a service"


@app.route("/<service_chain>")
def route_a(service_chain):
    root = {
        "a": f"hello from a"
    }

    return build_response(root, service_chain)


def build_response(root_message, service_chain):
    services_responses = dict()
    for requested_service in service_chain:
        for service_name in ALLOWED_SERVICES:
            if requested_service == service_name:
                try:
                    response = requests.get(f'http://{service_name}:8080/{service_name}')
                    s_rs = json.loads(response.text)
                    services_responses[service_name] = s_rs[service_name]
                except:
                    print(f"Error during calling service {requested_service}. Check the connection or port")

    return root_message | services_responses


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('listenport', 8080))
