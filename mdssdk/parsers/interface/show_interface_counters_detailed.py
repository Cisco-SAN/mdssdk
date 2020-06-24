import logging
import re

log = logging.getLogger(__name__)

PAT_TS = "Total Stats:\s+Rx total frames:\s+(?P<rx_total_frames>\d+)\s+ \
Tx total frames:\s+(?P<tx_total_frames>\d+)\s+ \
Rx total bytes:\s+(?P<rx_total_bytes>\d+)\s+ \
Tx total bytes:\s+(?P<tx_total_bytes>\d+)\s+ \
Rx total multicast:\s+(?P<rx_total_multicast>\d+)\s+ \
Tx total multicast: \s+(?P<tx_total_multicast>\d+)\s+ \
Rx total broadcast:\s+(?P<rx_total_broadcast>\d+)\s+ \
Tx total broadcast:\s+(?P<tx_total_broadcast>\d+)\s+ \
Rx total unicast:\s+(?P<rx_total_unicast>\d+)\s+ \
Tx total unicast:\s+(?P<tx_total_unicast>\d+)\s+ \
Rx total discards:\s+(?P<rx_total_discard>\d+)\s+ \
Tx total discards:\s+(?P<tx_total_discard>\d+)\s+ \
Rx total errors:\s+(?P<rx_total_error>\d+)\s+ \
Tx total errors:\s+(?P<tx_total_error>\d+)\s+ \
Rx class-2 frames:\s+(?P<rx_c_2_frames>\d+)\s+ \
Tx class-2 frames:\s+(?P<tx_c_2_frames>\d+)\s+ \
Rx class-2 bytes:\s+(?P<rx_c_2_bytes>\d+)\s+ \
Tx class-2 bytes:\s+(?P<tx_c_2_bytes>\d+)\s+ \
Rx class-2 frames discards:\s+(?P<rx_c_2_discards>\d+)\s+ \
Rx class-2 port reject frames:\s+(?P<rx_c_2_port_rjt_frames>\d+)\s+ \
Rx class-3 frames:\s+(?P<rx_c_3_frames>\d+)\s+ \
Tx class-3 frames:\s+(?P<tx_c_3_frames>\d+)\s+ \
Rx class-3 bytes:\s+(?P<rx_c_3_bytes>\d+)\s+ \
Tx class-3 bytes:\s+(?P<tx_c_3_bytes>\d+)\s+ \
Rx class-3 frames discards:\s+(?P<rx_c_3_discards>\d+)\s+ \
Rx class-f frames:\s+(?P<rx_c_f_frames>\d+)\s+ \
Tx class-f frames:\s+(?P<tx_c_f_frames>\d+)\s+ \
Rx class-f bytes:\s+(?P<rx_c_f_bytes>\d+)\s+ \
Tx class-f bytes:\s+(?P<tx_c_f_bytes>\d+)\s+ \
Rx class-f frames discards:\s+(?P<rx_c_f_discards>\d+)"

PAT_LS = "Link Stats:\s+Rx Link failures:\s+(?P<link_failures>\d+)\s+ \
Rx Sync losses:\s+(?P<sync_loss>\d+)\s+ \
Rx Signal losses:\s+(?P<signal_loss>\d+)\s+ \
Rx Primitive sequence protocol errors:\s+(?P<prm_seq_pro_err>\d+)\s+ \
Rx Invalid transmission words:\s+(?P<inv_trans_err>\d+)\s+ \
Rx Invalid CRCs:\s+(?P<inv_crc>\d+)\s+ \
Rx Delimiter errors:\s+(?P<delim_err>\d+)\s+ \
Rx fragmented frames:\s+(?P<frag_frames_rcvd>\d+)\s+ \
Rx frames with EOF aborts:\s+(?P<frames_eof_abort>\d+)\s+ \
Rx unknown class frames:\s+(?P<unknown_class_frames_rcvd>\d+)\s+ \
Rx Runt frames:\s+(?P<runt_frames>\d+)\s+ \
Rx Jabber frames:\s+(?P<jabber_frames>\d+)\s+ \
Rx too long:\s+(?P<too_long>\d+)\s+ \
Rx too short:\s+(?P<too_short>\d+)\s+ \
Rx FEC corrected blocks:\s+(?P<fec_corrected>\d+)\s+ \
Rx FEC uncorrected blocks:\s+(?P<fec_uncorrected>\d+)\s+ \
Rx Link Reset\(LR\) while link is active:\s+(?P<rx_link_reset>\d+)\s+ \
Tx Link Reset\(LR\) while link is active:\s+(?P<tx_link_reset>\d+)\s+ \
Rx Link Reset Responses\(LRR\):\s+(?P<rx_link_reset_resp>\d+)\s+ \
Tx Link Reset Responses\(LRR\):\s+(?P<tx_link_reset_resp>\d+)\s+ \
Rx Offline Sequences\(OLS\):\s+(?P<rx_off_seq_err>\d+)\s+ \
Tx Offline Sequences\(OLS\):\s+(?P<tx_off_seq_err>\d+)\s+ \
Rx Non-Operational Sequences\(NOS\):\s+(?P<rx_non_oper_seq>\d+)\s+ \
Tx Non-Operational Sequences\(NOS\):\s+(?P<tx_non_oper_seq>\d+)"

PAT_LOS = "Loop Stats:\s+Rx F8 type LIP sequence errors:\s+(?P<rx_f8_lip_seq_err>\d+)\s+ \
Tx F8 type LIP sequence errors:\s+(?P<tx_f8_lip_seq_err>\d+)\s+ \
Rx Non F8 type LIP sequence errors:\s+(?P<rx_non_f8_lip_seq_err>\d+)\s+ \
Tx Non F8 type LIP sequence errors:\s+(?P<tx_non_f8_lip_seq_err>\d+)"

PAT_CS = "Congestion Stats:\s+Tx Timeout discards:\s+(?P<timeout_discards>\d+)\s+\
Tx Credit loss:\s+(?P<credit_loss>\d+)\s+\
BB_SCs credit resend actions:\s+(?P<bb_scs_resend>\d+)\s+\
BB_SCr Tx credit increment actions:\s+(?P<bb_scr_incr>\d+)\s+\
(TxWait 2.5us due to lack of transmit credits:\s+(?P<txwait>\d+)\s+)?\
Percentage TxWait not available for last 1s\/1m\/1h\/72h:\s+(?P<tx_wait_unavbl_1s>\d+)%\/\
(?P<tx_wait_unavbl_1m>\d+)%\/(?P<tx_wait_unavbl_1hr>\d+)%\/(?P<tx_wait_unavbl_72hr>\d+)%\s*\
(Rx B2B credit remaining:\s+(?P<rx_b2b_credit_remain>\d+)\s*)?\
(Tx B2B credit remaining:\s+(?P<tx_b2b_credit_remain>\d+)\s*)?\
(Tx Low Priority B2B credit remaining:\s+(?P<tx_b2b_low_pri_cre>\d+)\s*)?\
(Rx B2B credit transitions to zero:\s+(?P<rx_b2b_credits>\d+)\s*)?\
(Tx B2B credit transitions to zero:\s+(?P<tx_b2b_credits>\d+)\s*)?"

PAT_OS = "Other Stats:\s+Zone drops:\s+(?P<pg_acl_drops>\d+)\s+ \
FIB drops for ports\s+(?P<pg_fib_start>\d+)-(?P<pg_fib_end>\d+):\s+(?P<pg_fib_drops>\d+)\s+ \
XBAR errors for ports\s+(?P<pg_xbar_start>\d+)-(?P<pg_xbar_end>\d+):\s+(?P<pg_xbar_drops>\d+)\s+ \
Other drop count:\s+(?P<pg_other_drops>\d+)"


class ShowInterfaceCountersDetailed(object):
    def __init__(self, outlines):
        self._group_dict = {}
        self.process_all(outlines)

    def process_all(self, outlines):
        outlines = "".join([eachline.strip("\n") for eachline in outlines])
        match = re.search(PAT_TS, outlines)
        if match:
            self._group_dict["total_stats"] = {
                k: int(v) for k, v in match.groupdict().items()
            }
        match = re.search(PAT_LS, outlines)
        if match:
            self._group_dict["link_stats"] = {
                k: int(v) for k, v in match.groupdict().items()
            }
        match = re.search(PAT_LOS, outlines)
        if match:
            self._group_dict["loop_stats"] = {
                k: int(v) for k, v in match.groupdict().items()
            }
        match = re.search(PAT_CS, outlines)
        if match:
            self._group_dict["congestion_stats"] = {
                k: int(v) for k, v in match.groupdict().items() if v is not None
            }
        match = re.search(PAT_OS, outlines)
        if match:
            self._group_dict["other_stats"] = {
                k: int(v) for k, v in match.groupdict().items()
            }
        log.debug(self._group_dict)

    @property
    def total_stats(self):
        return self._group_dict.get("total_stats", None)

    @property
    def link_stats(self):
        return self._group_dict.get("link_stats", None)

    @property
    def loop_stats(self):
        return self._group_dict.get("loop_stats", None)

    @property
    def congestion_stats(self):
        return self._group_dict.get("congestion_stats", None)

    @property
    def other_stats(self):
        return self._group_dict.get("other_stats", None)
