import logging
import re

from .connection_manager.errors import CLIError
from .connection_manager.errors import InvalidProfile

log = logging.getLogger(__name__)

# SAMPLE PROFILE
# protocol: scsi
# metrics: [port, total_read_io_time, total_write_io_time] - - default[] all
# view: scsi_initiator_it_flow
# where:[port,vsan]
# sort: vsan
# desc: False
# limit: 10

# Be extra careful while changing the patterns or the keys of the patten
METRICS = "metrics"
PROTOCOL = "protocol"
VIEW = "view"
WHERE = "where"
SORT = "sort"
DESC = "desc"
LIMIT = "limit"

VALID_PROTOCOLS = ["scsi", "nvme"]
MOD_PAT = (
    "^\|\s+(?P<module>\d+)\s+\|\s+(?P<scsi_npu_load>\d+)\s+(?P<nvme_npu_load>\d+)\s+(?P<total_npu_load>\d+)\s+\|"
    "\s+(?P<scsi_itls>\d+)\s+(?P<nvme_itns>\d+)\s+(?P<both_itls_itns>\d+)\s+\|"
    "\s+(?P<scsi_initiators>\d+)\s+(?P<nvme_initiators>\d+)\s+(?P<total_initiators>\d+)\s+\|"
    "\s+(?P<scsi_targets>\d+)\s+(?P<nvme_targets>\d+)\s+(?P<total_targets>\d+)\s+\|$"
)
MOD_PAT_COMP = re.compile(MOD_PAT)
TOTAL_PAT = (
    "^\| Total  \| n\/a  n\/a  n\/a   \|\s+(?P<scsi_itls>\d+)\s+(?P<nvme_itns>\d+)\s+(?P<both_itls_itns>\d+)\s+\|"
    "\s+(?P<scsi_initiators>\d+)\s+(?P<nvme_initiators>\d+)\s+(?P<total_initiators>\d+)\s+\|"
    "\s+(?P<scsi_targets>\d+)\s+(?P<nvme_targets>\d+)\s+(?P<total_targets>\d+)\s+\|$"
)
TOTAL_PAT_COMP = re.compile(TOTAL_PAT)
TIME_PAT = "As of (?P<collected_at>.*)"
TIME_PAT_COMP = re.compile(TIME_PAT)


class Analytics:
    """
    Analytics Module

    :example:
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
        >>> ana_hand = switch_obj.analytics
        >>> print(ana_hand)
        <mdslib.analytics.Analytics object at 0x10ad710d0>

    """

    def __init__(self, switch):
        self._sw = switch

    def _show_analytics_system_load(self):

        """
        Sample output of this proc is as follows

        sw129-Luke(config-if)# show analytics system-load
         n/a - not applicable
         ----------------------------------- Analytics System Load Info -------------------------------
         | Module | NPU Load (in %) | ITLs   ITNs   Both  |        Hosts        |       Targets       |
         |        | SCSI NVMe Total | SCSI   NVMe   Total | SCSI   NVMe   Total | SCSI   NVMe   Total |
         ----------------------------------------------------------------------------------------------
         |   1    | 0    43   43    | 0      15     15    | 0      10     10    | 0      1      1     |
         |   7    | 0    8    8     | 0      5      5     | 0      5      5     | 0      0      0     |
         | Total  | n/a  n/a  n/a   | 0      20     20    | 0      15     15    | 0      1      1     |
         ----------------------------------------------------------------------------------------------

        As of Fri Mar  6 17:12:22 2020
        sw129-Luke(config-if)#

        [{'both_itls_itns': 15,
          'module': '1',
          'nvme_initiators': 10,
          'nvme_itns': 15,
          'nvme_npu_load': '43',
          'nvme_targets': 1,
          'scsi_initiators': 0,
          'scsi_itls': 0,
          'scsi_npu_load': '0',
          'scsi_targets': 0,
          'total_initiators': 0,
          'total_npu_load': '43',
          'total_targets': 15},
         {'both_itls_itns': 8,
          'module': '7',
          'nvme_initiators': 8,
          'nvme_itns': 8,
          'nvme_npu_load': '8',
          'nvme_targets': 5,
          'scsi_initiators': 0,
          'scsi_itls': 0,
          'scsi_npu_load': '0',
          'scsi_targets': 0,
          'total_initiators': 8,
          'total_npu_load': '8',
          'total_targets': 5},
         {'both_itls_itns': '20',
          'nvme_initiators': '15',
          'nvme_itns': '20',
          'nvme_targets': '1',
          'scsi_initiators': '0',
          'scsi_itls': '0',
          'scsi_targets': '0',
          'total_initiators': '15',
          'total_targets': '1'},
         {'collected_at': 'Fri Mar  6 17:12:22 2020'}]
        """

        all = []
        try:
            cmd = "show analytics system-load"
            out = self._sw.show(cmd, use_ssh=True)
        except CLIError as c:
            if "Invalid command" in c.message:
                return None
            else:
                raise CLIError(cmd, c.message)
        for eachout in out:
            eachout = eachout.strip()
            if any(char.isdigit() for char in eachout):
                result_mod = MOD_PAT_COMP.match(eachout)
                if result_mod:
                    # print(result_mod.group())
                    d = result_mod.groupdict()
                    all.append(d)
                    continue
                result_tot = TOTAL_PAT_COMP.match(eachout)
                if result_tot:
                    d = result_tot.groupdict()
                    all.append(d)
                    continue
                result_time = TIME_PAT_COMP.match(eachout)
                if result_time:
                    d = result_time.groupdict()
                    all.append(d)
                    continue
        if len(all) == 0:
            return None
        else:
            return all

    def _validate_profile(self, profile):
        # TODO
        # LIMITATIONS:
        # Does not support where clause/sort/limit for now
        proto = profile.get(PROTOCOL, None)
        metrics = profile.get(PROTOCOL, None)
        view = profile.get(PROTOCOL, None)
        where = profile.get(WHERE, None)
        sort = profile.get(SORT, None)
        desc = profile.get(DESC, False)
        limit = profile.get(LIMIT, None)

        if proto is None:
            raise InvalidProfile(
                "'"
                + PROTOCOL
                + "' key is missing from the profile, this is mandatory and it needs to one of "
                + ",".join(VALID_PROTOCOLS)
            )
        if metrics is None:
            raise InvalidProfile(
                "'"
                + METRICS
                + "' key is missing from the profile, this is mandatory. A blank list represents 'all'"
            )
        if view is None:
            raise InvalidProfile(
                "'" + VIEW + "' key is missing from the profile, this is mandatory"
            )
        if proto not in VALID_PROTOCOLS:
            raise InvalidProfile(
                "'" + PROTOCOL + "' key needs to one of " + ",".join(VALID_PROTOCOLS)
            )
        if where is not None:
            if type(where) is not dict:
                raise InvalidProfile(
                    "where clause details must be in dict format. Example where = {'port': 'fc1/1', 'vsan': '100'}"
                )
        if sort is not None:
            if type(sort) is not str:
                raise InvalidProfile("sort can only be done on one coloumn")
        if desc is not None:
            if type(desc) is not bool:
                raise InvalidProfile("'" + DESC + "' key needs to either True or False")
        if limit is not None:
            if type(limit) is not int:
                raise InvalidProfile("'" + LIMIT + "' key needs to an integer")

        return True

    def _get_select_query_string(self, profile, ignore_metrics=False):
        if ignore_metrics:
            metrics = None
        else:
            metrics = profile.get(METRICS, None)
        where = profile.get(WHERE, None)
        sort = profile.get(SORT, None)
        desc = profile.get(DESC, None)
        limit = profile.get(LIMIT, None)

        if (metrics is None) or (len(metrics) == 0):
            selq = (
                    "select all from fc-" + profile.get(PROTOCOL) + "." + profile.get(VIEW)
            )
        else:
            allmetrics = ",".join(metrics)
            selq = (
                    "select "
                    + allmetrics
                    + " from fc-"
                    + profile.get(PROTOCOL)
                    + "."
                    + profile.get(VIEW)
            )
        return selq

    def create_query(self, name, profile, clear=False, differential=False, interval=30):
        """
        Create analytics query

        :param name: name of the query to create
        :type name: str
        :param profile: profile for the query
        :type profile: dict('protocol': value , 'metrics': [values], 'view': value)
        :param clear: set to True to add clear option to the query else set to False
        :type clear: bool (Default = False)
        :param differential: set to True to add differential option to the query else set to False
        :type differential: bool (Default = False)
        :param interval: query interval that needs to be set
        :type interval: interval (Default = 30)
        :raises InvalidProfile: If the profile passed is not correct

        :return: switch response to the create query cli and the error if any
        :rtype: tuple: (output, error)

        :example:
            >>>
            >>> port_scsi_profile = {
            ... 'protocol': 'scsi',
            ... 'metrics': [],  # default, which is all
            ... 'view': 'port'
            ... }
            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.create_query("port_query",port_scsi_profile)
            >>>

        """
        if self._validate_profile(profile):
            selq = self._get_select_query_string(profile)
            cmd = (
                    'analytics query "'
                    + selq
                    + '" name '
                    + name
                    + " type periodic interval "
                    + str(interval)
            )
            if clear:
                if differential:
                    cmd = cmd + " clear differential"
                else:
                    cmd = cmd + " clear"
            elif differential:
                cmd = cmd + " differential"
            return self._sw.config(cmd, use_ssh=True)

    def delete_query(self, name):
        """

        :param name: name of the query to delete
        :type name: str
        :return: switch response to the delete query cli and the error if any
        :rtype: tuple: (output, error)
        :example:
            >>>
            >>> ana_hand.delete_query(port_scsi_profile)
        """
        cmd = "no analytics name " + name
        return self._sw.config(cmd)

    def show_query(self, name=None, profile=None, clear=False, differential=False):
        """

        Get result for installed query or do a pull query

        :param name: name of the query installed for which result needs to be pulled out
        :type name: str
        :param profile: profile to get the pull query result
        :type profile: dict('protocol': value , 'metrics': [values], 'view': value)
        :param clear: set to True to add clear option to the pull query else set to False
        :type clear: bool (Default = False)
        :param differential: set to True to add differential option to the pull query else set to False
        :type differential: bool (Default = False)
        :raises InvalidProfile: If the profile passed is not correct

        :return: switch response to the show query cli and the error if any
        :rtype: tuple: (output, error)

        :example:
            >>>
            >>> port_scsi_profile = {
            ... 'protocol': 'scsi',
            ... 'metrics': [],  # default, which is all
            ... 'view': 'port'
            ... }
            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.create_query("port_query",port_scsi_profile)
            >>> out_install = ana_hand.show_query("port_query")
            >>> print(out_install)
            {'1': {'port': 'fc1/48', 'scsi_target_count': '2', 'scsi_initiator_count': '0', 'io_app_count': '1',
             'logical_port_count': '2', 'scsi_target_app_count': '2',...}
            >>> out_pullq = ana_hand.show_query(profile=port_scsi_profile)
            >>> print(out_pullq)
            {'1': {'port': 'fc1/48', 'scsi_target_count': '2', 'scsi_initiator_count': '0', 'io_app_count': '1',
             'logical_port_count': '2', 'scsi_target_app_count': '2',...}
        """
        if (name is not None) and (profile is not None):
            raise TypeError(
                "Need to pass either query name(for installed query) or profile(for pull query) not both"
            )
        if name is None:
            # Profile is set so its a pull query
            if self._validate_profile(profile):
                selq = self._get_select_query_string(profile)
                cmd = 'show analytics query "' + selq + '"'
                if clear:
                    cmd = cmd + " clear "
                    if differential:
                        cmd = cmd + " differential "
                elif differential:
                    cmd = cmd + " differential "
                return self._sw.show(cmd, use_ssh=True)
        else:
            # Name is set, so its an install query
            cmd = "show analytics query name " + name + " result"
            return self._sw.show(cmd, use_ssh=True)

    def clear(self, profile):
        """
        clear analytics query

        :param profile: profile to get the pull query result
        :type profile: dict('protocol': value , 'metrics': [values], 'view': value)
        :raises InvalidProfile: If the profile passed is not correct

        :return: switch response to the show query cli and the error if any
        :rtype: tuple: (output, error)

        :example:
            >>>
            >>> scsi_profile_few = {
            ... 'protocol': 'scsi',
            ... 'metrics': ['port', 'total_read_io_count', 'total_write_io_count'],
            ... 'view': 'port'
            ... }
            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.clear(port_scsi_profile)
            >>>
        """

        # BUG: mdslib.connection_manager.errors.CLIError: The command " clear analytics query "select port,total_read_io_count,total_write_io_count from fc-scsi.port" " gave the error " Column selection is not allowed for clear ".

        if self._validate_profile(profile):
            selq = self._get_select_query_string(profile, ignore_metrics=True)
            cmd = 'clear analytics query "' + selq + '"'
            return self._sw.config(cmd, use_ssh=True)

    def purge(self, profile):
        """
        purge analytics query

        :param profile: profile to get the pull query result
        :type profile: dict('protocol': value , 'metrics': [values], 'view': value)
        :raises InvalidProfile: If the profile passed is not correct

        :return: switch response to the show query cli and the error if any
        :rtype: tuple: (output, error)

        :example:
            >>>
            >>> scsi_profile_few = {
            ... 'protocol': 'scsi',
            ... 'metrics': ['port', 'total_read_io_count', 'total_write_io_count'],
            ... 'view': 'port'
            ... }
            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.purge(port_scsi_profile)
            >>>
        """
        # BUG: mdslib.connection_manager.errors.CLIError: The command " terminal dont-ask ; purge analytics query "select port,total_read_io_count,total_write_io_count from fc-scsi.port" ; no terminal dont-ask " gave the error " Column selection is not allowed for purge ".

        if self._validate_profile(profile):
            selq = self._get_select_query_string(profile, ignore_metrics=True)
            purgecmd = 'purge analytics query "' + selq + '"'
            cmd = "terminal dont-ask ; " + purgecmd + " ; no terminal dont-ask"
            return self._sw.config(cmd, use_ssh=True)

    def npu_load(self, module, protocol=None):
        """
        Get NPU load for a module

        :param module: module number for which we need to get NPU load
        :type module: int
        :param protocol: protocol for which NPU load needs to be fetched, options are ‘scsi’, ‘name’ or ‘None’(both scsi and nvme)
        :type protocol: str (Default = None)
        :values: 'scsi,'nvme',None

        :return: NPU load
        :rtype: str

        :example:
            >>>
            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.npu_load(2)
            30%
            >>> ana_hand.npu_load(2,'scsi')
            10%
            >>> ana_hand.npu_load(2,'nvme')
            20%
            >>>
        """
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get("module", None)
            if mod_str == str(module):
                if protocol == "scsi":
                    return str(eachrow.get("scsi_npu_load")) + "%"
                if protocol == "nvme":
                    return str(eachrow.get("nvme_npu_load")) + "%"
                if protocol is None:
                    return str(eachrow.get("total_npu_load")) + "%"

    def itls(self, module=None):
        """
        Get total switch scsi ITLs or total per module scsi ITLs

        :param module: module number for which we need to get scsi ITLs, if set to None, get total ITLs of the switch
        :type module: int (Default = None)

        :return: total ITLs
        :rtype: int

        :example:

            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.itls()
            1248
            >>> ana_hand.itls(2)
            1000
            >>> ana_hand.itls(4)
            248
            >>>
        """
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get("module", None)
            if module is None:
                if mod_str is None:
                    return eachrow.get("scsi_itls")
            else:
                if mod_str == str(module):
                    return eachrow.get("scsi_itls")

    def itns(self, module=None):
        """
        Get total switch nvme ITNs or total per module nvme ITNs

        :param module: module number for which we need to get nvme ITNs, if None gets switch nvme ITNs
        :type module: int (Default = None)

        :return: total ITNs
        :rtype: int

        :example:

            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.itns()
            200
            >>> ana_hand.itns(2)
            150
            >>> ana_hand.itns(4)
            50
            >>>
        """
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get("module", None)
            if module is None:
                if mod_str is None:
                    return eachrow.get("nvme_itns")
            else:
                if mod_str == str(module):
                    return eachrow.get("nvme_itns")

    def itls_itns(self, module=None):
        """
        Get total switch scsi ITLs and nvme ITNs or total per module scsi ITLs and nvme ITNs

        :param module: module number for which we need to get scsi ITLs and nvme ITNs, if None gets switch ITLs and ITNs
        :type module: int (Default = None)

        :return: total scsi ITLs and nvme ITNs
        :rtype: int

        :example:

            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.itls_itns()
            1448
            >>> ana_hand.itls_itns(2)
            1150
            >>> ana_hand.itls_itns(4)
            298
            >>>
        """
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get("module", None)
            if module is None:
                if mod_str is None:
                    return eachrow.get("both_itls_itns")
            else:
                if mod_str == str(module):
                    return eachrow.get("both_itls_itns")

    def initiators(self, module=None, protocol=None):
        """
        Get total initiators on the switch or per module

        :param module: module number for which we need to get total initiators
        :type module: int (Default = None)
        :param protocol: protocol for which we need to get total initiators
                if 'scsi' gets scsi initiators, if 'nvme', gets nvme initiators, if None, gets total initiators
        :type protocol: str (Default = None)
        :values: 'scsi,'nvme',None

        :return: total initiators
        :rtype: str

        :example:
            >>>
            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.initiators()
            30
            >>> ana_hand.initiators(2,'scsi')
            10
            >>> ana_hand.initiators(2,'nvme')
            20
            >>>
        """
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get("module", None)
            if module is None:
                if mod_str is None:
                    if protocol == "scsi":
                        return eachrow.get("scsi_initiators")
                    if protocol == "nvme":
                        return eachrow.get("nvme_initiators")
                    if protocol is None:
                        return eachrow.get("total_initiators")
            else:
                if mod_str == str(module):
                    if protocol == "scsi":
                        return eachrow.get("scsi_initiators")
                    if protocol == "nvme":
                        return eachrow.get("nvme_initiators")
                    if protocol is None:
                        return eachrow.get("total_initiators")

    def targets(self, module=None, protocol=None):
        """
        Get total targets on the switch or per module

        :param module: module number for which we need to get total targets
        :type module: int (Default = None)
        :param protocol: protocol for which we need to get total targets, options are 'scsi','nvme',None(both scsi and nvme)
        :type protocol: str (Default = None)
        :values: 'scsi,'nvme',None

        :return: total targets
        :rtype: str

        :example:
            >>>
            >>> ana_hand = switch_obj.analytics
            >>> ana_hand.targets()
            30
            >>> ana_hand.targets(2,'scsi')
            10
            >>> ana_hand.targets(2,'nvme')
            20
            >>>
        """
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get("module", None)
            if module is None:
                if mod_str is None:
                    if protocol == "scsi":
                        return eachrow.get("scsi_targets")
                    if protocol == "nvme":
                        return eachrow.get("nvme_targets")
                    if protocol is None:
                        return eachrow.get("total_targets")
            else:
                if mod_str == str(module):
                    if protocol == "scsi":
                        return eachrow.get("scsi_targets")
                    if protocol == "nvme":
                        return eachrow.get("nvme_targets")
                    if protocol is None:
                        return eachrow.get("total_targets")
