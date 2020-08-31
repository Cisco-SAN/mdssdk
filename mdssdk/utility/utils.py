import logging
import re
import threading
from functools import wraps

from ..constants import PAT_WWN
from ..parsers.switch.show_topology import ShowTopology
from ..fcns import Fcns

log = logging.getLogger()


def is_pwwn_valid(pwwn):
    newpwwn = pwwn.lower()
    match = re.match(PAT_WWN, newpwwn)
    if match:
        return True
    return False


def get_key(nxapikey, version=None):
    if version in nxapikey.keys():
        return nxapikey[version]
    else:
        return nxapikey["DEFAULT"]


def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''

    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()

    return backgrnd_func


def _run_show_topo_for_npiv(sw):
    peer_ip_list = []
    # Show topo
    log.debug("topo")
    out = sw.show("show topology")
    if sw.is_connection_type_ssh():
        shtopo = ShowTopology(out)
        # print(out)
        peer_ip_list = shtopo.get_all_peer_ip_addrs()
    else:
        alltopo = out['TABLE_topology_vsan']['ROW_topology_vsan']
        for eachvsan in alltopo:
            topolines = eachvsan['TABLE_topology']['ROW_topology']
            for eachline in topolines:
                peer_ip_list.append(eachline['peer_ip_address'])
    return list(set(peer_ip_list))


def _run_show_fcns_for_npv(sw):
    peer_ip_list = []
    # Show fcns
    log.debug("Fcns")
    if sw.is_connection_type_ssh():
        out = sw.show("show fcns database detail  | i node-ip | ex 0.0.0.0")
        if out:
            for eachline in out:
                peer_ip_list.append(eachline.split(':')[1])
    else:
        fcns = Fcns(sw)
        out = fcns.database(detail=True)
        for eachrow in out:
            z = eachrow['TABLE_fcns_database']['ROW_fcns_database']['node_ip_addr']
            if z == '0.0.0.0':
                continue
            peer_ip_list.append(z)
    return list(set(peer_ip_list))
