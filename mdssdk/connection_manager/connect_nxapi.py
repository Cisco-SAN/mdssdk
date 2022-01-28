import base64
import json
import logging

import requests
from builtins import range
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

from .errors import NXOSError
from ..constants import CLI_CMD_TIMEOUT

log = logging.getLogger(__name__)


class ConnectNxapi(object):
    """ """

    def __init__(
            self, host, username, password, transport=u"https", port=None, verify_ssl=True
    ):

        if transport not in ["http", "https"]:
            raise NXOSError("'%s' is an invalid transport." % transport)

        if port is None:
            if transport == "http":
                port = 8081
            elif transport == "https":
                port = 8443

        self.url = u"%s://%s:%s/ins" % (transport, host, port)
        log.debug("URL is : " + self.url)
        self.headers = {u"content-type": u"application/json-rpc"}
        self.username = username
        self.__pw = base64.b64encode(password.encode("utf-8"))
        self.verify_ssl = verify_ssl
        if not self.verify_ssl:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            log.debug(
                "Warning!! 'verify_ssl' flag is set to False, hence ignoring the 'InsecureRequestWarning' exception"
            )
        else:
            log.debug(
                "'verify_ssl' flag is set to True, so hopefully SSL connections is setup"
            )
        self.send_request("show version")

    def _build_payload(self, commands, rpc_version, method):

        if rpc_version is not None:
            payload_list = []
            id_num = 1
            for command in commands:
                payload = dict(
                    jsonrpc=rpc_version,
                    method=method,
                    params=dict(cmd=command, version=1.2),
                    id=id_num,
                )

                payload_list.append(payload)
                id_num += 1
            log.debug("Payload list is :")
            log.debug(payload_list)
            return payload_list
        else:
            cmd = ";".join(commands)
            payload = dict(
                ins_api=dict(
                    version="1.2",
                    type=method,
                    chunk="0",
                    sid="1",
                    input=cmd.strip(),
                    output_format="json",
                )
            )
            log.debug("Payload is :")
            log.debug(payload)
            return payload

    def send_request(
            self, commands, rpc_version=u"2.0", method=u"cli", timeout=CLI_CMD_TIMEOUT
    ):
        """
        :param commands:
        :param rpc_version:
        :param method:
        :param timeout:
        :return:
        """
        timeout = int(timeout)
        payload = self._build_payload(commands, rpc_version, method)
        if rpc_version is None:
            header = {u"content-type": u"application/json"}
        else:
            header = self.headers
        log.debug(self.url)
        response = requests.post(
            self.url,
            timeout=timeout,
            data=json.dumps(payload),
            headers=header,
            auth=HTTPBasicAuth(
                self.username, base64.b64decode(self.__pw).decode("utf-8")
            ),
            verify=self.verify_ssl,
        )
        log.debug("req response")
        log.debug(response)
        # response.raise_for_status()
        response_list = response.json()

        if isinstance(response_list, dict):
            response_list = [response_list]

        for i in range(len(commands)):
            response_list[i][u"command"] = commands[i]

        return response_list
