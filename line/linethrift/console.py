from ..thriftpy2 import load
from ..thriftpy2.thrift import TApplicationException
from ..thriftpy2.http import THttpClient as tclient
from ..thriftpy2.protocol import TCompactProtocol as tproto
from ..thriftpy2.transport import TBufferedTransport as tbuffer
from .service import Client

from thrift.protocol import TCompactProtocol


from itertools import zip_longest

import functools
import os, sys, copy


def args_to_kwargs(thrift_spec, *args, **kwargs):
    for item, value in zip_longest(sorted(thrift_spec.items()), args):
        arg_name = item[1][1]
        required = item[1][-1]
        if value is not None:
            kwargs[item[1][1]] = value
        if required and arg_name not in kwargs:
            raise ValueError(arg_name)
    return kwargs

class Console:

    line_thrift = load(
        os.path.dirname(__file__) + "/line.thrift",
        module_name="linepoll_thrift"
    )

    LiffService = line_thrift.LiffService
    TalkService = line_thrift.TalkService
    AuthService = line_thrift.AuthService
    ChannelService = line_thrift.ChannelService
    LoginService = line_thrift.SecondaryQrCodeLoginService
    LoginPermitService = line_thrift.SecondaryQrCodeLoginPermitService
    LoginPermitNoticeService = line_thrift.SecondaryQrCodeLoginPermitNoticeService
    LoginPrimaryAccountInitService = line_thrift.PrimaryAccountInitService

    operations = {
        0: "END_OF_OPERATION",
        1: "UPDATE_PROFILE",
        36: "UPDATE_SETTINGS",
        2: "NOTIFIED_UPDATE_PROFILE",
        3: "REGISTER_USERID",
        4: "ADD_CONTACT",
        5: "NOTIFIED_ADD_CONTACT",
        6: "BLOCK_CONTACT",
        7: "UNBLOCK_CONTACT",
        8: "NOTIFIED_RECOMMEND_CONTACT",
        9: "CREATE_GROUP",
        10: "UPDATE_GROUP",
        11: "NOTIFIED_UPDATE_GROUP",
        12: "INVITE_INTO_GROUP",
        13: "NOTIFIED_INVITE_INTO_GROUP",
        31: "CANCEL_INVITATION_GROUP",
        32: "NOTIFIED_CANCEL_INVITATION_GROUP",
        14: "LEAVE_GROUP",
        15: "NOTIFIED_LEAVE_GROUP",
        16: "ACCEPT_GROUP_INVITATION",
        17: "NOTIFIED_ACCEPT_GROUP_INVITATION",
        34: "REJECT_GROUP_INVITATION",
        35: "NOTIFIED_REJECT_GROUP_INVITATION",
        18: "KICKOUT_FROM_GROUP",
        19: "NOTIFIED_KICKOUT_FROM_GROUP",
        20: "CREATE_ROOM",
        21: "INVITE_INTO_ROOM",
        22: "NOTIFIED_INVITE_INTO_ROOM",
        23: "LEAVE_ROOM",
        24: "NOTIFIED_LEAVE_ROOM",
        25: "SEND_MESSAGE",
        26: "RECEIVE_MESSAGE",
        27: "SEND_MESSAGE_RECEIPT",
        28: "RECEIVE_MESSAGE_RECEIPT",
        29: "SEND_CONTENT_RECEIPT",
        40: "SEND_CHAT_CHECKED",
        41: "SEND_CHAT_REMOVED",
        30: "RECEIVE_ANNOUNCEMENT",
        38: "INVITE_VIA_EMAIL",
        37: "NOTIFIED_REGISTER_USER",
        33: "NOTIFIED_UNREGISTER_USER",
        39: "NOTIFIED_REQUEST_RECOVERY",
        42: "NOTIFIED_FORCE_SYNC",
        43: "SEND_CONTENT",
        44: "SEND_MESSAGE_MYHOME",
        45: "NOTIFIED_UPDATE_CONTENT_PREVIEW",
        46: "REMOVE_ALL_MESSAGES",
        47: "NOTIFIED_UPDATE_PURCHASES",
        48: "DUMMY",
        49: "UPDATE_CONTACT",
        50: "NOTIFIED_RECEIVED_CALL",
        51: "CANCEL_CALL",
        52: "NOTIFIED_REDIRECT",
        53: "NOTIFIED_CHANNEL_SYNC",
        54: "FAILED_SEND_MESSAGE",
        55: "NOTIFIED_READ_MESSAGE",
        56: "FAILED_EMAIL_CONFIRMATION",
        59: "NOTIFIED_PUSH_NOTICENTER_ITEM",
        58: "NOTIFIED_CHAT_CONTENT",
        60: "NOTIFIED_JOIN_CHAT",
        61: "NOTIFIED_LEAVE_CHAT",
        62: "NOTIFIED_TYPING",
        63: "FRIEND_REQUEST_ACCEPTED",
        64: "DESTROY_MESSAGE",
        65: "NOTIFIED_DESTROY_MESSAGE",
        66: "UPDATE_PUBLICKEYCHAIN",
        67: "NOTIFIED_UPDATE_PUBLICKEYCHAIN",
        68: "NOTIFIED_BLOCK_CONTACT",
        69: "NOTIFIED_UNBLOCK_CONTACT",
        70: "UPDATE_GROUPPREFERENCE",
        71: "NOTIFIED_PAYMENT_EVENT",
        72: "REGISTER_E2EE_PUBLICKEY",
        73: "NOTIFIED_E2EE_KEY_EXCHANGE_REQ",
        74: "NOTIFIED_E2EE_KEY_EXCHANGE_RESP",
        75: "NOTIFIED_E2EE_MESSAGE_RESEND_REQ",
        76: "NOTIFIED_E2EE_MESSAGE_RESEND_RESP",
        77: "NOTIFIED_E2EE_KEY_UPDATE",
        78: "NOTIFIED_BUDDY_UPDATE_PROFILE",
        79: "NOTIFIED_UPDATE_LINEAT_TABS",
        80: "UPDATE_ROOM",
        81: "NOTIFIED_BEACON_DETECTED",
        82: "UPDATE_EXTENDED_PROFILE",
        83: "ADD_FOLLOW",
        84: "NOTIFIED_ADD_FOLLOW",
        85: "DELETE_FOLLOW",
        86: "NOTIFIED_DELETE_FOLLOW",
        87: "UPDATE_TIMELINE_SETTINGS",
        88: "NOTIFIED_FRIEND_REQUEST",
        89: "UPDATE_RINGBACK_TONE",
        90: "NOTIFIED_POSTBACK",
        91: "RECEIVE_READ_WATERMARK",
        92: "NOTIFIED_MESSAGE_DELIVERED",
        93: "NOTIFIED_UPDATE_CHAT_BAR",
        94: "NOTIFIED_CHATAPP_INSTALLED",
        95: "NOTIFIED_CHATAPP_UPDATED",
        96: "NOTIFIED_CHATAPP_NEW_MARK",
        97: "NOTIFIED_CHATAPP_DELETED",
        98: "NOTIFIED_CHATAPP_SYNC",
        99: "NOTIFIED_UPDATE_MESSAGE",
        100: "UPDATE_CHATROOMBGM",
        101: "NOTIFIED_UPDATE_CHATROOMBGM",
        102: "UPDATE_RINGTONE",
        118: "UPDATE_USER_SETTINGS",
        119: "NOTIFIED_UPDATE_STATUS_BAR",
        120: "CREATE_CHAT",
        121: "UPDATE_CHAT",
        122: "NOTIFIED_UPDATE_CHAT",
        123: "INVITE_INTO_CHAT",
        124: "NOTIFIED_INVITE_INTO_CHAT",
        125: "CANCEL_CHAT_INVITATION",
        126: "NOTIFIED_CANCEL_CHAT_INVITATION",
        127: "DELETE_SELF_FROM_CHAT",
        128: "NOTIFIED_DELETE_SELF_FROM_CHAT",
        129: "ACCEPT_CHAT_INVITATION",
        130: "NOTIFIED_ACCEPT_CHAT_INVITATION",
        131: "REJECT_CHAT_INVITATION",
        132: "DELETE_OTHER_FROM_CHAT",
        133: "NOTIFIED_DELETE_OTHER_FROM_CHAT"
    }
class TClient(object):

    #Thriftpy2
    def __init__(self, service, iprot, oprot=None):
        self._service = service
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def __getattr__(self, _api):
        if _api in self._service.thrift_services:
            return functools.partial(self._req, _api)
        if _api == 'tclose':
            return functools.partial(self._req, 'close')
        raise AttributeError("{} instance has no attribute '{}'".format(
            self.__class__.__name__, _api))

    def __dir__(self):
        return self._service.thrift_services

    def _req(self, _api, *args, **kwargs):
        try:
            kwargs = args_to_kwargs(getattr(self._service, _api + "_args").thrift_spec,
                          *args, **kwargs)
        except ValueError as e:
            raise TApplicationException(1,
                    '{arg} is required argument for {service}.{api}'.format(
                     arg=e.args[0], service=self._service.__name__, api=_api))

        result_cls = getattr(self._service, _api + "_result")
        self._send(_api, **kwargs)
        if not getattr(result_cls, "oneway"):
            return self._recv(_api)

    def _send(self, _api, **kwargs):
        self._oprot.write_message_begin(_api, 1, self._seqid)
        args = getattr(self._service, _api + "_args")()
        for k, v in kwargs.items():
            setattr(args, k, v)
        args.write(self._oprot)
        self._oprot.write_message_end()
        self._oprot.trans.flush()

    def _recv(self, _api):
        fname, mtype, rseqid = self._iprot.read_message_begin()
        if mtype == 3:
            x = TApplicationException()
            x.read(self._iprot)
            self._iprot.read_message_end()
            raise x

        result = getattr(self._service, _api + "_result")()
        result.read(self._iprot)
        self._iprot.read_message_end()
        if hasattr(result, "success") and result.success is not None:
            return result.success
        if len(result.thrift_spec) == 0:
            return
        for k, v in result.__dict__.items():
            if k != "success" and v:
                raise v

        if hasattr(result, "success"):
            raise TApplicationException(5)

    def close(self):
        self._iprot.trans.close()
        if self._iprot != self._oprot:
            self._oprot.trans.close()

def make_client(service, uri, path='', Headers={}, auth=None, isOpen=True):
    headers = copy.deepcopy(Headers)
    if auth != None:
        headers.update({'X-Line-Access': auth})

    http_socket = tclient(uri)
    http_socket.setCustomHeaders(headers)
    transport = tbuffer(http_socket)
    iprot = tproto(transport)
    if isOpen == True:
        transport.open()

    client = TClient(service, iprot)
    http_socket.path = path
    return client

def make_clients(service, url, path='', http_header_factory=None):
    http_socket = tclient(url)
    if path:
        http_socket.path = path

    http_socket.setCustomHeaders(http_header_factory)
    transport = tbuffer(http_socket)
    iprot = tproto(transport)
    return TClient(service, iprot)

def make_connect(uri, path='', Headers={}, auth=None, isOpen=True):
    headers = copy.deepcopy(Headers)
    if auth != None:
        headers.update({'X-Line-Access': auth})

    http_socket = tclient(uri+path)
    http_socket.setCustomHeaders(headers)
    iprot = TCompactProtocol.TCompactProtocol(http_socket)
    if isOpen == True:
        http_socket.open()

   
    return Client(iprot)