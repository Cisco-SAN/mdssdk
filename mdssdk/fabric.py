__author__ = 'Suhas Bharadwaj (subharad)'

import logging
import multiprocessing
import re
# import ConfigParser
import os
from functools import wraps
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import wait

from .switch import Switch

# from .utility.utils import _wait_till_connect_threads_complete

log = logging.getLogger(__name__)


class Fabric(object):
    """
    :param ip_address: mgmt ip address of switch
    :type ip_address: str
    :param username: username
    :type id: str
    :param password: password
    :type password: str
    :param connection_type: connection type 'http' or 'https'(optional, default: 'https')
    :type connection_type: str
    :param port: port number (optional, default: 8443)
    :type port: int
    :param timeout: timeout period in seconds (optional, default: 30)
    :type timeout: int
    :param verify_ssl: SSL verification (optional, default: True)
    :type verify_ssl: bool

    :example:
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)

    """

    def __init__(
            self,
            ip_address,
            username,
            password,
            connection_type="https",
            port=8443,
            timeout=30,
            verify_ssl=True,
    ):
        log.debug("Fabric init method " + ip_address + " connection_type: " + connection_type)
        self.__ip_address = ip_address
        self.__username = username
        self.__password = password
        self.connection_type = connection_type
        self.port = port
        self.timeout = timeout
        self.__verify_ssl = verify_ssl
        self.switches = {}
        self.ips_to_be_discovered = [ip_address]

    def all_switches_in_fabric(self, discover_npv=True):
        while self.ips_to_be_discovered.__len__() != 0:
            m = multiprocessing.Manager()
            lock = m.Lock()
            allfutures = []
            executor = ThreadPoolExecutor(len(self.ips_to_be_discovered))
            for ip in self.ips_to_be_discovered:
                fut = executor.submit(self.__connect_to_switch, lock, ip, self.__username, self.__password,
                                      self.connection_type, self.port, self.timeout, self.__verify_ssl, discover_npv)
                allfutures.append(fut)
            wait(allfutures)
            for fut in allfutures:
                try:
                    log.debug(fut.result())
                except Exception as e:
                    log.exception("Executor Exception")
                    # log.debug(str(e))
                    # print("Got exception")
                    # print(str(e))
                    # print(type(e))
                    z = self._extract_ip_from_exception_str(e)
                    if z is not None:
                        log.info("Not Discovered : " + z + " (Not reachable)")
                        self.ips_to_be_discovered.remove(z)
                    # log.debug("Got exception")
                    # print(e)
                    # print(e.args)

            self.ips_to_be_discovered = list(set(self.ips_to_be_discovered))
            for eachip in self.switches.keys():
                if eachip in self.ips_to_be_discovered:
                    self.ips_to_be_discovered.remove(eachip)
        log.info("Done discovering all the switches in the fabric")

    def __connect_to_switch(self, lock,
                            ip_address,
                            username,
                            password,
                            connection_type="https",
                            port=8443,
                            timeout=30,
                            verify_ssl=True, discover_npv=True):

        switch = Switch(ip_address, username, password, connection_type, port, timeout, verify_ssl)
        npv = switch.npv
        if not npv:
            peerlist = switch.discover_peer_switches()
            if discover_npv:
                peerlist = peerlist + switch.discover_peer_npv_switches()
            peerlist = list(set(peerlist))
        with lock:
            log.info("Discovered : " + ip_address)
            # print(ip_address + " - " + ",".join(peerlist))
            # print(" Before : " + ",".join(self.ips_to_be_discovered))
            self.switches[ip_address] = switch
            self.ips_to_be_discovered.remove(ip_address)
            if not npv:
                self.ips_to_be_discovered = self.ips_to_be_discovered + peerlist
            # print(" After : " + ",".join(self.ips_to_be_discovered))

    def _extract_ip_from_exception_str(self, e):
        # Example: Authentication failure: unable to connect cisco_nxos 10.126.95.203:22
        # Authentication failed.
        z = str(e)
        m = re.search(r'((\d+\.){3}\d+)', z)
        if m:
            found = m.group(1)
            return found
