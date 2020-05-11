__author__ = 'Suhas Bharadwaj (subharad)'

import logging
import threading
from functools import wraps

from .switch import Switch

log = logging.getLogger(__name__)


def wait_till_connect_threads_complete(fn):
    """
    Decorator which will check if all the threads are complete by doing a join
    :param fn: Function that needs to be decorated.
                This function 'fn' is called and after which we wait till all the child threads with the name 'connect' are finished
    :return: None
    """

    @wraps(fn)
    def th_complete(*a, **kw):
        # Call the function which was decorated mostly it will be the 'connect' method of 'Switch' class
        ret = fn(*a, **kw)
        # Wait till all 'connect' threads are complete
        for t in threading.enumerate():
            # print t.getName()
            if t.getName() == 'connect':
                t.join()
        return ret

    return th_complete


class Fabric(object):
    """
    Fabric class
    """

    def __init__(self, name="New Fabric"):
        """

        :param name: Name of the fabric
        """
        # Fabric name
        self.__fab_name = name

        # Switch related variables
        self.__fab_seed_sw_ip = ""
        self.__fab_swuser = ""
        self.__fab_swpassword = ""
        self.__fab_swconntype = ""
        self.__sw_obj_dict = {}
        self.discovered_switches = None

    @property
    def name(self):
        """
        Returns name of the fabric
        :return: Returns name of the fabric
        """
        return self.__fab_name

    @property
    def connected_switches(self):
        """

        :return:
        """
        return self.__sw_obj_dict

    def connect_to_switches(self, switch_list, username, password, connection_type='https', port=None, timeout=30,
                            verify_ssl=True):
        """

        :param switch_list: List of switch ips that needs to be connected to
        :type switch_list: list
        :param username: username of the switches
        :type username: str
        :param password: password of the switches
        :type password: str
        :param connection_type: type of the connection http or https default is https
        :type connection_type:str
        :param port: http or https port, default is 8443
        :type port:int
        :param timeout: connection or command timeout in secs, default is 30s
        :type timeout:int
        :param verify_ssl: Default is True, please set it to False if there is no SSL defined between the switches and the host
        :type verify_ssl:bool
        :return: Dictionary with key value pair as switch ip and Switch object
        :rtype: dict
        """
        for eachsw_ip in switch_list:
            swobj = Switch(eachsw_ip, username=username, password=password, connection_type=connection_type, port=port,
                           timeout=timeout, verify_ssl=verify_ssl)
            self.__sw_obj_dict[eachsw_ip] = swobj
        return self.__sw_obj_dict

    def discover_all_switches_in_fabric(self, seed_switch_ip, username, password, connection_type='https', port=8443,
                                        timeout=30, verify_ssl=True, discover_npv=True):
        """
        Discover all the switches in the fabric using the seed switch ip

        :param seed_switch_ip: Seed switch ip that needs to be used to discover the fabric
        :type seed_switch_ip: list
        :param username: username of the switches
        :type username: str
        :param password: password of the switches
        :type password: str
        :param connection_type: type of the connection http or https default is https
        :type connection_type:str
        :param port: http or https port, default is 8443
        :type port:int
        :param timeout: connection or command timeout in secs, default is 30s
        :type timeout:int
        :param verify_ssl: Default is True, please set it to False if there is no SSL defined between the switches and the host
        :type verify_ssl:bool
        :param discover_npv: discover NPV switches in the fabric, default us True
        :type discover_npv: bool
        :return: Returns True if discovery is successful
        :rtype: bool
        """
        discovered_switches = {}
        log.info("Discovering all switches in the fabric with the seed switch : " + seed_switch_ip)
        swobj = Switch(seed_switch_ip, username=username, password=password, connection_type=connection_type, port=port,
                       timeout=timeout, verify_ssl=verify_ssl)

        if swobj.can_connect:
            discovered_switches[swobj.ipaddr] = swobj
        else:
            msg = "ERROR!! Unable to connect to the seed switch : " + swobj.ipaddr + \
                  " via " + swobj.connection_type + " with port " + str(
                swobj.port) + " . Make sure that NXAPI is enabled."
            log.error(msg)
            return False

        if (swobj.__is_npv_switch()):
            log.error(
                "The seed switch({0}) is a NPV switch, please provide a NPIV switch as seed switch to discover the entire fabric".
                    format(swobj.ipaddr))
            return False

        peer_switches = swobj.get_peer_switches()
        # print(peer_switches)

        i = 0
        while i < len(peer_switches):
            each_ip = peer_switches[i]
            i = i + 1
            # for each_ip in peer_switches:
            if each_ip in discovered_switches.keys():
                continue
            else:
                # print(discovered_switches)
                swobj = Switch(each_ip, username=username, password=password, connection_type=connection_type,
                               port=port,
                               timeout=timeout, verify_ssl=verify_ssl)

                if swobj.can_connect:
                    discovered_switches[swobj.ipaddr] = swobj
                    peers = swobj.get_peer_switches()
                    peer_switches = peer_switches + peers
                else:
                    msg = "ERROR!! Unable to connect to the switch : " + swobj.ipaddr + \
                          " via " + swobj.connection_type + " with port " + str(
                        port) + " . Make sure that NXAPI is enabled."
                    log.debug(msg)

        # print(discovered_switches)

        if discover_npv:
            allswlist = list(discovered_switches.keys())
            for swobj in discovered_switches.values():
                allswlist = allswlist + swobj.get_peer_npv_switches()
            allswlist = list(dict.fromkeys(allswlist))
            for eachswip in allswlist:
                if eachswip not in discovered_switches.keys():
                    swobj = Switch(eachswip, username=username, password=password, connection_type=connection_type,
                                   port=port,
                                   timeout=timeout, verify_ssl=verify_ssl)
                    if swobj.can_connect:
                        discovered_switches[swobj.ipaddr] = swobj
                    else:
                        msg = "ERROR!! Unable to connect to the seed switch : " + swobj.ipaddr + \
                              " via " + swobj.connection_type + " with port " + str(
                            port) + " . Make sure that NXAPI is enabled."
                        log.debug(msg)

        self.discovered_switches = discovered_switches
        return True
