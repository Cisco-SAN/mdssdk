import json
import logging

from mdssdk.switch import Switch

log = logging.getLogger(__name__)

with open("switch_details.json", "r") as j:
    data = json.load(j)

log.info("Creating switch object")

sw = Switch(
    ip_address=data["ip_address"],
    username=data["username"],
    password=data["password"],
    connection_type=data["connection_type"],
    port=data["port"],
    timeout=data["timeout"],
    verify_ssl=False,
)
