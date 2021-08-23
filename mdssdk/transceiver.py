import re

from .nxapikeys import interfacekeys
from .parsers.interface import ShowInterfaceTransceiverDetail
from .utility.utils import get_key
from .connection_manager.errors import UnsupportedSwitch
from .constants import VALID_PIDS_MDS


class Transceiver(object):
    """
    Transceiver module

    :param fcobj: Fc interface object
    :type fcobj: Fc

    """

    def __init__(self, fcobj):
        self.__fcobj = fcobj
        self._SW_VER = fcobj._SW_VER
        self.__swobj = fcobj._swobj
        if not self.__swobj.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )

    @property
    def sfp_present(self):
        """
        Returns if sfp is present on the Fc interface

        :return: True if sfp is present, False otherwise
        :rtype: bool
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.sfp_present)
            True
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.sfp_present
        retout = out.get(get_key(interfacekeys.SFP, self._SW_VER))
        return "sfp is present" in retout

    @property
    def name(self):
        """
        Returns the name of the sfp if present

        :return: the name of the sfp if present, None otherwise
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.name)
            CISCO-FINISAR
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.name
        name = get_key(interfacekeys.NAME, self._SW_VER)
        return out.get(name, None)

    @property
    def part_number(self):
        """
        Returns the part number of the sfp if present

         :return: the part number of the sfp if present
         :rtype: str
         :example:
             >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
             >>> trans_handler = fcobj.transceiver
             >>> print(trans_handler.part_number)
             FTLF8532P4BCV-C1
             >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.part_number
        partnum = get_key(interfacekeys.PART_NUM, self._SW_VER)
        return out.get(partnum, None)

    @property
    def cisco_id(self):
        """
        Returns the cisco id of the sfp if present

        :return: the cisco id of the sfp if present
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.cisco_id)
            SFP-H10GB-CU3M (0x81)
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.cisco_id
        ciscoid = get_key(interfacekeys.CISCO_ID, self._SW_VER)
        return out.get(ciscoid, None)

    @property
    def cisco_part_number(self):
        """
        Returns the cisco part number of the sfp if present

        :return: the cisco part number of the sfp if present
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.cisco_part_number)
            10-3206-01
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.cisco_part_number
        partnum = get_key(interfacekeys.CISCO_PART_NUM, self._SW_VER)
        return out.get(partnum, None)

    @property
    def cisco_product_id(self):
        """
        Returns the cisco product id of the sfp if present

        :return: the cisco product id of the sfp if present
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.cisco_product_id)
            DS-SFP-FC32G SW
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.cisco_product_id
        prod_id = get_key(interfacekeys.CISCO_PRODUCT_ID, self._SW_VER)
        return out.get(prod_id, None)

    @property
    def bit_rate(self):
        """
        Returns the bit rate of the sfp if present

        :return: the bit rate of the sfp if present
        :rtype: int
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.bit_rate)
            28000
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.bit_rate
        bitrate = get_key(interfacekeys.BIT_RATE, self._SW_VER)
        return out.get(bitrate, None)

    @property
    def min_speed(self):
        """
        Returns the min speed of the sfp if present

        :return: the min speed of the sfp if present
        :rtype: int
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.min_speed)
            8000
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return int(shintd.min_speed)
        supported_speed = get_key(interfacekeys.SUPP_SPEED, self._SW_VER)
        supp_speed = out.get(supported_speed, None)
        if supp_speed is not None:
            pat = "Min speed: (\d+) Mb/s, Max speed: (\d+) Mb/s"
            match = re.match(pat, supp_speed)
            if match:
                return int(match.group(1))
        return None

    @property
    def max_speed(self):
        """
        Returns the max speed of the sfp if present

        :return: the max speed of the sfp if present
        :rtype: int
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.max_speed)
            32000
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return int(shintd.max_speed)
        supported_speed = get_key(interfacekeys.SUPP_SPEED, self._SW_VER)
        supp_speed = out.get(supported_speed, None)
        if supp_speed is not None:
            pat = "Min speed: (\d+) Mb/s, Max speed: (\d+) Mb/s"
            match = re.match(pat, supp_speed)
            if match:
                return int(match.group(2))
        return None

    @property
    def temperature(self):
        """
        Returns the temperature of the sfp if present

        :return: the temperature of the sfp if present
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.temperature)
            47.65 C
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.temperature.strip()
        try:
            table_calibaration = out["TABLE_calibration"]["ROW_calibration"]
            if type(table_calibaration) is list:
                table_calibaration = table_calibaration[0]
            table_calibaration_detail = table_calibaration["TABLE_detail"]["ROW_detail"]
            if type(table_calibaration_detail) is list:
                table_calibaration_detail = table_calibaration_detail[0]
            temp = get_key(interfacekeys.TEMPERATURE, self._SW_VER)
            t = table_calibaration_detail.get(temp, None)
            if t is not None:
                return t.strip()
            return None
        except KeyError:
            return None

    @property
    def voltage(self):
        """
        Returns the voltage of the sfp if present

        :return: the voltage of the sfp if present
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.voltage)
            3.39 V
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.voltage.strip()
        try:
            table_calibaration = out["TABLE_calibration"]["ROW_calibration"]
            if type(table_calibaration) is list:
                table_calibaration = table_calibaration[0]
            table_calibaration_detail = table_calibaration["TABLE_detail"]["ROW_detail"]
            if type(table_calibaration_detail) is list:
                table_calibaration_detail = table_calibaration_detail[0]
            vol = get_key(interfacekeys.VOLTAGE, self._SW_VER)
            v = table_calibaration_detail.get(vol, None)
            if v is not None:
                return v.strip()
            return None
        except KeyError:
            return None

    @property
    def current(self):
        """
        Returns the current of the sfp if present

        :return: the current of the sfp if present
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.current)
            7.79 mA
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        # print(out)
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            return shintd.current.strip()
        try:
            # print(out)
            table_calibaration = out["TABLE_calibration"]["ROW_calibration"]
            if type(table_calibaration) is list:
                table_calibaration = table_calibaration[0]
            table_calibaration_detail = table_calibaration["TABLE_detail"]["ROW_detail"]
            if type(table_calibaration_detail) is list:
                table_calibaration_detail = table_calibaration_detail[0]
            # print(table_calibaration_detail)
            curr = get_key(interfacekeys.CURRENT, self._SW_VER)
            c = table_calibaration_detail.get(curr, None)
            if c is not None:
                return c.strip()
            return None
        except KeyError:
            return None

    @property
    def tx_power(self):
        """
        Returns the tx_power of the sfp if present

        :return: the tx_power of the sfp if present
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.tx_power)
            -0.88 dBm
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            tp = shintd.tx_power
            if tp is not None:
                return tp.strip()
            return None
        try:
            table_calibaration = out["TABLE_calibration"]["ROW_calibration"]
            if type(table_calibaration) is list:
                table_calibaration = table_calibaration[0]
            table_calibaration_detail = table_calibaration["TABLE_detail"]["ROW_detail"]
            if type(table_calibaration_detail) is list:
                table_calibaration_detail = table_calibaration_detail[0]
            txpow = get_key(interfacekeys.TX_POWER, self._SW_VER)
            tp = table_calibaration_detail.get(txpow, None)
            if tp is not None:
                return tp.strip()
            return None
        except KeyError:
            return None

    @property
    def rx_power(self):
        """
        Returns the rx_power of the sfp if present

        :return: the rx_power of the sfp if present
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>> print(trans_handler.rx_power)
            -10.66 dBm
            >>>
        """
        out = self.__fcobj._execute_transceiver_cmd()
        if self.__swobj.is_connection_type_ssh():
            shintd = ShowInterfaceTransceiverDetail(out)
            rp = shintd.rx_power
            if rp is not None:
                return rp.strip()
            return None
        try:
            table_calibaration = out["TABLE_calibration"]["ROW_calibration"]
            if type(table_calibaration) is list:
                table_calibaration = table_calibaration[0]
            table_calibaration_detail = table_calibaration["TABLE_detail"]["ROW_detail"]
            if type(table_calibaration_detail) is list:
                table_calibaration_detail = table_calibaration_detail[0]
            rxpow = get_key(interfacekeys.RX_POWER, self._SW_VER)
            rp = table_calibaration_detail.get(rxpow, None)
            if rp is not None:
                return rp.strip()
            return None
        except KeyError:
            return None
