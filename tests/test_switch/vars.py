import json
import logging

log = logging.getLogger(__name__)

with open("switch_details.json", "r") as j:
    data = json.load(j)

ip_address = data["ip_address"]
