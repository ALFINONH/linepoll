# -*- coding: UTF-8 -*-

"""
    ~~~~~~~~~~~
    Simple linebot
    created by: 
    ©finbot alfino~nh
    ~~~~~~~~~~~
"""
from typing import (
    Dict,
    Any,
    Awaitable,
    List
)
from . import LineTransport
from . import config as LINE_ENDPOINT
from ..lib.curve import (
    AuthService,
    ChannelService,
    CallService,
    LiffService,
    MessageService,
    ShopService,
    TalkService
)

from thrift.protocol import TCompactProtocol
from thrift.transport import TTransport
from thrift.transport import THttpClient

import json, requests, random, time

class LineServer(object):

    """Connect to Line python server"""

    def __init__(self, headers: Dict[str, Any]):

        self.headers = headers

    def set_headers(self, oldValue, newValue):
        self.headers[oldValue] = newValue

    def update_headers(self, newValueDict):
        self.headers.update(newValueDict)

    def _make_thttp_client(self, url, service, connect: bool = True):
        self.http_response = THttpClient.THttpClient(url)
        self.http_response.setCustomHeaders(self.headers)
        transport_factory = TTransport.TBufferedTransportFactory()
        self.transport = transport_factory.getTransport(self.http_response)
        protocol_factory = TCompactProtocol.TCompactProtocolFactory()
        self.protocol = protocol_factory.getProtocol(self.transport)
        self._line_impl = service(self.protocol, TCompactProtocol.TCompactProtocol(self.transport))
        if(connect == True):
            self.transport.open()

        return self._line_impl

    def _make_thttp_client2(self, url, service, customThrift=False, request='httplib', http2 = True, connect: bool = True):
        self.transport = LineTransport.LineTransport(url, customThrift=customThrift, request=request, http2=http2)
        self.transport.setCustomHeaders(self.headers)
        protocol_factory = TCompactProtocol.TCompactProtocolFactory()
        self.protocol = protocol_factory.getProtocol(self.transport)
        self.http_client2 = service(self.protocol, TCompactProtocol.TCompactProtocol(self.transport))
        if(connect == True):
            self.transport.open()

        return self.http_client2

    def LCR(self):
        content = requests.get(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.CERTIFICATE_PATH,headers=self.headers).text
        getAccessKey = json.loads(content)
        return getAccessKey

    def LTSD(self):
        """path: /api/v4/TalkService.do"""
        return self._make_thttp_client(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.AUTH_QUERY_PATH, AuthService.Client, connect = False)

    def LLR(self):
        """path: /api/v4p/rs"""
        return self._make_thttp_client(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.LOGIN_QUERY_PATH, AuthService.Client, connect = False)

    def LS(self):
        """path: /SHOP4"""
        return self._make_thttp_client(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.SHOP_PATH, ShopService.Client)

    def LC(self):
        """path: /V4"""
        return self._make_thttp_client(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.CALL_PATH, CallService.Client)

    def LCH(self):
        """path: /CH4"""
        return self._make_thttp_client(LINE_ENDPOINT.GD2_HOST+LINE_ENDPOINT.CHANNEL_PATH, ChannelService.Client)

    def LL(self):
        """path: /LIFF1"""
        return self._make_thttp_client(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.LIFF_PATH, LiffService.Client)

    def LT(self):
        """path: /S4"""
        return self._make_thttp_client2(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.TALK_PATH, TalkService.Client, customThrift=False, request='httplib', http2 = False)

    def LP(self):
        """path: /P4"""
        return self._make_thttp_client2(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.POLL_PATH, TalkService.Client, customThrift=False, request='httplib', http2 = False)

    def LM(self):
        """path: /F4"""
        return self._make_thttp_client2(LINE_ENDPOINT.GXX_HOST+LINE_ENDPOINT.MESSAGE_PATH, MessageService.Client, customThrift=False, request='httplib', http2 = True)

def LineConnect(type, headers: Dict[str, Any]=None):
    assert type in ['talk','poll','message','call','channel','liff','shop'], 'Invalid value type %s'%(type)
    if(type=='talk'):
        return LineServer(headers).LT()
    elif(type=='poll'):
        return LineServer(headers).LP()
    elif(type=='message'):
        return LineServer(headers).LM()
    elif(type=='call'):
        return LineServer(headers).LC()
    elif(type=='channel'):
        return LineServer(headers).LCH()
    elif(type=='liff'):
        return LineServer(headers).LL()
    elif(type=='shop'):
        return LineServer(headers).LS()