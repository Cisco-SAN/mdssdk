import logging
import re

from .constants import PAT_PC, PAT_FC
from .nxapikeys import interfacekeys
from .utility.utils import get_key

log = logging.getLogger(__name__)


class Interface(object):
    """
    Interface module

    :param switch: switch object on which vsan operations need to be executed
    :type switch: Switch
    :param name: name of the interface
    :type name: str

    .. warning:: Interface class is a Base class and cannot be instantiated, please use specific interface classes(Child/Derived class)
                like Fc,PortChannel etc.. to instantiate
    """

    def __init__(self, switch, name):
        self.__swobj = switch
        self._name = name
        self._SW_VER = switch._SW_VER

    # Interface is the base class for Fc and PortChannel.
    # So you cannot instantiate the base class(Interface), you have to instantiate the derived/child class (Fc,PortChannel)
    def __new__(cls, *args, **kwargs):
        if cls is Interface:
            raise TypeError(
                "Interface class is a Base class and cannot be instantiated, "
                "please use specific interface classes(Child/Derived class) like Fc,PortChannel etc.. to instantiate")
        return object.__new__(cls)

    @property
    def name(self):
        """

        :return:
        """
        return self._name

    @property
    def description(self):
        """
        set description of the interface or
        get description of the interface

        :getter:
        :return: description of the interface
        :rtype: str
        :example:
            >>>
            >>> print(int_obj.description)
            This is an ISL connected to sw2
            >>>

        :setter:
        :param description: set description of the interface
        :type description: str
        :example:
            >>>
            >>> int_obj.description = "This is an ISL connected to sw2"
            >>>
        """

        out = self.__swobj.show("show interface  " + self._name + " description")
        desc = out['TABLE_interface']['ROW_interface']['description']
        # IF the string is a big one then the return element is of type list
        if type(desc) is list:
            retval = ''.join(desc)
        else:
            retval = desc
        return retval

    @description.setter
    def description(self, value):
        cmd = "interface " + self._name + " ; switchport description  " + value
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)
        log.debug(out)

    @property
    def mode(self):
        """
        set interface mode or
        get interface mode

        :getter:
        :return: interface mode
        :rtype: str
        :example:
            >>>
            >>> print(int_obj.mode)
            F
            >>>

        :setter:
        :param mode: set mode of the interface
        :type mode: str
        :example:
            >>>
            >>> int_obj.mode = "F"
            >>>
        """
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[get_key(interfacekeys.INT_OPER_MODE, self._SW_VER)]
        return None

    @mode.setter
    def mode(self, value):
        cmd = "interface " + self._name + " ; switchport mode  " + value
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)
        log.debug(out)

    @property
    def speed(self):
        """
        set speed of the interface or
        get speed of the interface

        :getter:
        :return: speed of the interface
        :rtype: int
        :example:
            >>>
            >>> print(int_obj.speed)
            32000
            >>>

        :setter:
        :param mode: set speed of the interface
        :type mode: int
        :example:
            >>>
            >>> int_obj.speed = 32000
            >>>
        """
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[get_key(interfacekeys.INT_OPER_SPEED, self._SW_VER)]
        return None

    @speed.setter
    def speed(self, value):
        cmd = "interface " + self._name + " ; switchport speed  " + str(value)
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)

    @property
    def trunk(self):
        """
        set trunk mode on the interface or
        get trunk mode on the interface

        :getter:
        :return: trunk mode of the interface
        :rtype: str
        :example:
            >>>
            >>> print(int_obj.trunk)
            on
            >>>

        :setter:
        :param mode: set trunk mode on the interface
        :type mode: str
        :example:
            >>>
            >>> int_obj.trunk = "on"
            >>>
        """
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[get_key(interfacekeys.INT_ADMIN_TRUNK_MODE, self._SW_VER)]
        return None

    @trunk.setter
    def trunk(self, value):
        cmd = "interface " + self._name + " ; switchport trunk mode  " + value
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)

    @property
    def status(self):
        """
        set status of the interface or
        get status of the interface

        :getter:
        :return: status of the interface
        :rtype: str
        :example:
            >>>
            >>> print(int_obj.status)
            trunking
            >>>

        :setter:
        :param mode: set status of the interface
        :type mode: str
        :values: "shutdown", "no shutdown"
        :example:
            >>>
            >>> int_obj.status = "no shutdown"
            >>>
        """
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[get_key(interfacekeys.INT_STATUS, self._SW_VER)]
        return None

    @status.setter
    def status(self, value):
        cmd = "terminal dont-ask ; interface " + self._name + " ; " + value + " ; no terminal dont-ask "
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)

    @property
    def counters(self):
        """
        Returns handler for counters module, using which we could get various counter details of the interface

        :return: counters handler
        :rtype: Counters
        :example:
            >>> intcounters = int_obj.counters
            >>>
        """
        return self.Counters(self)

    def __parse_show_int_brief(self):
        log.debug("Getting sh int brief output")
        out = self.__swobj.show("show interface brief ")
        log.debug(out)
        # print(out)
        fcmatch = re.match(PAT_FC, self._name)
        pcmatch = re.match(PAT_PC, self._name)
        if fcmatch:
            out = out['TABLE_interface_brief_fc']['ROW_interface_brief_fc']
            for eachout in out:
                if eachout[get_key(interfacekeys.INTERFACE, self._SW_VER)] == self._name:
                    return eachout
        elif pcmatch:
            # Need to check if "sh int brief" has PC info
            pcinfo = out.get('TABLE_interface_brief_portchannel', None)
            if pcinfo is None:
                return None
            out = pcinfo['ROW_interface_brief_portchannel']
            if type(out) is dict:
                outlist = [out]
            else:
                outlist = out
            for eachout in outlist:
                if eachout[get_key(interfacekeys.INTERFACE, self._SW_VER)] == self._name:
                    return eachout
        return None

    def _execute_counters_detailed_cmd(self):
        cmd = "show interface " + self._name + " counters detailed"
        log.debug("Sending the cmd")
        log.debug(cmd)
        out = self.__swobj.config(cmd)
        return out['body']['TABLE_counters']['ROW_counters']

    def _execute_counters_brief_cmd(self):
        cmd = "show interface " + self._name + " counters brief"
        log.debug("Sending the cmd")
        log.debug(cmd)
        out = self.__swobj.config(cmd)
        return out['body']["TABLE_counters_brief"]["ROW_counters_brief"]

    def _execute_clear_counters_cmd(self):
        cmd = "clear counters interface " + self._name
        log.debug("Sending the cmd")
        log.debug(cmd)
        out = self.__swobj.config(cmd)

    class Counters(object):
        def __init__(self, intobj):
            self.__intobj = intobj
            self._SW_VER = intobj._SW_VER

        def clear(self):
            """
            Clear the counters on the interface
            :return: None
            :example:
                >>>
                >>> intcounters = int_obj.counters
                >>> intcounters.clear()
                >>>
            """
            self.__intobj._execute_clear_counters_cmd()

        @property
        def brief(self):
            """
            Get brief counters details of the interface

            :return: brief: Returns brief counters details of the interface
            :rtype: dict (name:value)
            :example:
                >>>
                >>> intcounters = int_obj.counters
                >>> print(intcounters.brief)
                {'input_rate': 0, 'frames_in': 14970, 'output_rate': 0, 'frames_out': 14831}
                >>>
            """
            out = self.__intobj._execute_counters_brief_cmd()
            out.pop(get_key(interfacekeys.INTERFACE, self._SW_VER))
            return out

        @property
        def total_stats(self):
            """
            Get total stats from the detailed counters of the interface

            :return: total_stats: total stats from the detailed counters of the interface
            :rtype: dict (name:value)
            :example:
                >>>
                >>> intcounters = int_obj.counters
                >>> print(intcounters.total_stats)
                {'rx_total_frames': 14970, 'tx_total_frames': 14831, 'rx_total_bytes': 2235488, 'tx_total_bytes': 1733508, 'rx_total_multicast': 0,
                'tx_total_multicast': 0, 'rx_total_broadcast': 0, 'tx_total_broadcast': 0, 'rx_total_unicast': 14970, 'tx_total_unicast': 14831,
                'rx_total_discard': 0, 'tx_total_discard': 0, 'rx_total_error': 0, 'tx_total_error': 0, 'rx_c_2_frames': 0, 'tx_c_2_frames': 0,
                'rx_c_2_bytes': 0, 'tx_c_2_bytes': 0, 'rx_c_2_discards': 0, 'rx_c_2_port_rjt_frames': 0, 'rx_c_3_frames': 14962, 'tx_c_3_frames': 14823,
                'rx_c_3_bytes': 2235072, 'tx_c_3_bytes': 1733092, 'rx_c_3_discards': 0, 'rx_c_f_frames': 8, 'tx_c_f_frames': 8, 'rx_c_f_bytes': 416,
                'tx_c_f_bytes': 416, 'rx_c_f_discards': 0}
                >>>
            """
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_total', None)
            if total is not None:
                return total.get('ROW_total', None)
            return None

        @property
        def link_stats(self):
            """
            Get link stats from the detailed counters of the interface

            :return: link_stats: link stats from the detailed counters of the interface
            :rtype: dict (name:value)
            :example:
                >>>
                >>> intcounters = int_obj.counters
                >>> print(intcounters.link_stats)
                {'link_failures': 2, 'sync_loss': 0, 'signal_loss': 0, 'prm_seq_pro_err': 0, 'inv_trans_err': 0,
                'inv_crc': 0, 'delim_err': 0, 'frag_frames_rcvd': 0, 'frames_eof_abort': 0, 'unknown_class_frames_rcvd': 0,
                'runt_frames': 0, 'jabber_frames': 0, 'too_long': 0, 'too_short': 0, 'fec_corrected': 0, 'fec_uncorrected': 0,
                'rx_link_reset': 0, 'tx_link_reset': 0, 'rx_link_reset_resp': 4, 'tx_link_reset_resp': 2, 'rx_off_seq_err': 6,
                'tx_off_seq_err': 8, 'rx_non_oper_seq': 3, 'tx_non_oper_seq': 2}
                >>>
            """
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_link', None)
            if total is not None:
                return total.get('ROW_link', None)
            return None

        @property
        def loop_stats(self):
            """
            Get loop stats from the detailed counters of the interface

            :return: loop_stats: loop stats from the detailed counters of the interface
            :rtype: dict (name:value)
            :example:
                >>>
                >>> intcounters = int_obj.counters
                >>> print(intcounters.loop_stats)
                {'rx_f8_lip_seq_err': 0, 'tx_f8_lip_seq_err': 0, 'rx_non_f8_lip_seq_err': 0, 'tx_non_f8_lip_seq_err': 0}
                >>>
            """
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_loop', None)
            if total is not None:
                return total.get('ROW_loop', None)
            return None

        @property
        def congestion_stats(self):
            """
            Get congestion stats from the detailed counters of the interface

            :return: congestion_stats: congestion stats from the detailed counters of the interface
            :rtype: dict (name:value)
            :example:
                >>>
                >>> intcounters = int_obj.counters
                >>> print(intcounters.congestion_stats)
                {'timeout_discards': 0, 'credit_loss': 0, 'bb_scs_resend': 0, 'bb_scr_incr': 0, 'txwait': 0,
                'tx_wait_unavbl_1s': 0, 'tx_wait_unavbl_1m': 0, 'tx_wait_unavbl_1hr': 0, 'tx_wait_unavbl_72hr': 0,
                'rx_b2b_credit_remain': 1, 'tx_b2b_credit_remain': 0, 'tx_b2b_low_pri_cre': 0, 'rx_b2b_credits': 0, 'tx_b2b_credits': 0}
                >>>
            """
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_congestion', None)
            if total is not None:
                return total.get('ROW_congestion', None)
            return None

        @property
        def other_stats(self):
            """
            Get other stats from the detailed counters of the interface

            :return: other_stats: other stats from the detailed counters of the interface
            :rtype: dict (name:value)
            :example:
                >>>
                >>> intcounters = int_obj.counters
                >>> print(intcounters.other_stats)
                {'pg_acl_drops': 0, 'pg_fib_start': '1', 'pg_fib_end': '16', 'pg_fib_drops': 0, 'pg_xbar_start': '1',
                'pg_xbar_end': '16', 'pg_xbar_drops': 0, 'pg_other_drops': 0}
                >>>
            """
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_others', None)
            if total is not None:
                return total.get('ROW_others', None)
            return None
