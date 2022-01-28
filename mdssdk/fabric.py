__author__ = "Suhas Bharadwaj (subharad)"

import logging
import multiprocessing
import re
from concurrent.futures import wait
from concurrent.futures.thread import ThreadPoolExecutor

from .connection_manager.errors import UnsupportedSeedSwitch
from .switch import Switch

# from .utility.utils import _wait_till_connect_threads_complete

log = logging.getLogger(__name__)


class Fabric(object):
    """
    Fabric module

    :param ip_address: mgmt ip address of the seed switch
    :type ip_address: str
    :param username: username
    :type id: str
    :param password: password
    :type password: str
    :param connection_type: connection type 'http' or 'https' or 'ssh' (default: 'https')
    :type connection_type: str
    :param port: port number (default: 8443 for https and 8080 for http) , ignored when connection type is ssh
    :type port: int
    :param timeout: timeout period in seconds (default: 30)
    :type timeout: int
    :param verify_ssl: SSL verification (default: True)
    :type verify_ssl: bool

    :example:
        >>> fabric_obj = Fabric(ip_address = switch_ip, username = switch_username, password = switch_password)

    """

    def __init__(self, ip_address, username, password, timeout=30):
        # log.debug("Fabric init method " + ip_address + " connection_type: " + connection_type)
        self.__ip_address = ip_address
        self.__username = username
        self.__password = password
        self.connection_type = "ssh"
        # self.port = port
        self.timeout = timeout
        # self.__verify_ssl = verify_ssl
        self._switches = {}
        self._ips_to_be_discovered = [ip_address]
        self._ips_not_considered = {}
        self.seed_switch = Switch(
            ip_address,
            username,
            password,
            connection_type=self.connection_type,
            timeout=timeout,
        )

    def discover_all_switches(self, npv_discovery=True):
        """
        Discovers all the switches in the fabric

        :param npv_discovery: Set to true if npv switches needs to be discovered
        :type npv_discovery: bool (default True)
        :return: Returns all switches in the fabric
        :rtype: dict

        :example:
            >>> from mdssdk.fabric import Fabric
            >>> f = Fabric(ip, user, pw, verify_ssl=False)
            >>> out= f.discover_all_switches(npv_discovery=True)
            >>> print(out)
            Discovering all switches in the fabric(seed ip: 10.127.190.34). Please wait...
            10.127.190.55: is not an MDS switch, hence skipping it.
            {'10.127.190.34': <mdssdk.switch.Switch object at 0x10f14e978>, '10.127.190.50': <mdssdk.switch.Switch object at 0x10f14e908>}
            >>>
            >>>
        """
        print(
            "Discovering all switches in the fabric(seed ip: "
            + self.__ip_address
            + "). Please wait..."
        )
        npv = self.seed_switch.npv
        if npv:
            raise UnsupportedSeedSwitch(
                "Cannot discover the fabric using an NPV switch, Please use an NPIV switch for discovery"
            )
        while self._ips_to_be_discovered.__len__() != 0:
            m = multiprocessing.Manager()
            lock = m.Lock()
            allfutures = []
            executor = ThreadPoolExecutor(len(self._ips_to_be_discovered))
            for ip in self._ips_to_be_discovered:
                fut = executor.submit(
                    self.__connect_to_switch,
                    lock,
                    ip,
                    self.__username,
                    self.__password,
                    self.connection_type,
                    self.timeout,
                    npv_discovery,
                )
                allfutures.append(fut)
            wait(allfutures)
            for fut in allfutures:
                self._ips_to_be_discovered = list(set(self._ips_to_be_discovered))
                # print(self._ips_to_be_discovered)
                try:
                    log.debug(fut.result())
                except Exception as e:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(e).__name__, e.args)
                    # print(message)
                    # log.exception("Executor Exception")
                    z = self._extract_ip_from_exception_str(e)
                    if z is not None:
                        self._ips_to_be_discovered.remove(z)
                    if "UnsupportedSwitch" == type(e).__name__:
                        msg = z + ": is not an MDS switch, hence skipping it."
                        self._ips_not_considered[z] = msg
                    elif "NetmikoAuthenticationException" == type(e).__name__:
                        msg = z + ": invalid username or password, hence skipping it."
                        self._ips_not_considered[z] = msg
                    elif "NetmikoTimeoutException" == type(e).__name__:
                        msg = z + ": unable to reach the switch, hence skipping it."
                        self._ips_not_considered[z] = msg
                    elif "ConnectionError" == type(e).__name__:
                        msg = (
                                z
                                + ": failed to establish http/https connection(check if nxapi is enabled), hence skipping it."
                        )
                        self._ips_not_considered[z] = msg

            for eachip in self._switches.keys():
                if eachip in self._ips_to_be_discovered:
                    self._ips_to_be_discovered.remove(eachip)
            for eachip in self._ips_not_considered.keys():
                if eachip in self._ips_to_be_discovered:
                    self._ips_to_be_discovered.remove(eachip)
        if self._ips_not_considered:
            for val in self._ips_not_considered.values():
                # print("_ips_not_considered")
                print(val)
        return self._switches

    def __connect_to_switch(
            self,
            lock,
            ip_address,
            username,
            password,
            connection_type="ssh",
            timeout=30,
            discover_npv=True,
    ):

        switch = Switch(
            ip_address,
            username,
            password,
            connection_type=connection_type,
            timeout=timeout,
        )
        # print(ip_address)
        npv = switch.npv
        if not npv:
            peerlist = switch.discover_peer_switches()
            if discover_npv:
                peerlist = peerlist + switch.discover_peer_npv_switches()
            peerlist = list(set(peerlist))
            # print(peerlist)
        with lock:
            # print("Discovered : " + ip_address)
            # print(ip_address + " - " + ",".join(peerlist))
            # print(" Before : " + ",".join(self._ips_to_be_discovered))
            self._switches[ip_address] = switch
            self._ips_to_be_discovered.remove(ip_address)
            if not npv:
                self._ips_to_be_discovered = self._ips_to_be_discovered + peerlist
            # print(" After : " + ",".join(self._ips_to_be_discovered))

    def _extract_ip_from_exception_str(self, e):
        # Example: Authentication failure: unable to connect cisco_nxos 10.126.95.203:22
        # Authentication failed.
        z = str(e)
        m = re.search(r"((\d+\.){3}\d+)", z)
        if m:
            found = m.group(1)
            return found
        return "NONE"

#######################################
# ----- Placeholder for notes -----
########################################
# -- Invalid user name password
#    NetmikoAuthenticationException
#    ('Authentication to device failed.\n\nCommon causes of this problem are:\n1. Invalid username and password\n2. Incorrect SSH-key file\n3. Connecting to the wrong device\n\nDevice settings: cisco_nxos 10.127.190.4:22\n\n\nAuthentication failed.',)
#
# -- Not Reachable
#    NetmikoTimeoutException
#    ('TCP connection to device failed.\n\nCommon causes of this problem are:\n1. Incorrect hostname or IP address.\n2. Wrong TCP port.\n3. Intermediate firewall blocking access.\n\nDevice settings: cisco_nxos 10.126.94.116:22\n\n',)
#
# -- UnsupportedSwitch Non MDS switches
#    UnsupportedSwitch
#    ('SDK supports only MDS switches. 10.126.94.130(N7K-C7009) is not a supported switch ',)
#
# -- ConnectionError when nxapi is not enabled
#    ConnectionError
#    requests.exceptions.ConnectionError: HTTPSConnectionPool(host='10.127.190.34', port=8443): Max retries exceeded with url: /ins (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x1097addd8>: Failed to establish a new connection: [Errno 61] Connection refused'))
