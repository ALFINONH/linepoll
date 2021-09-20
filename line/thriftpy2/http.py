# -*- coding: utf-8 -*-

"""
# Run server:

"""

from __future__ import absolute_import

import os
import socket
import logging
import sys, base64
from contextlib import contextmanager
from io import BytesIO

from thriftpy2._compat import PY3

if PY3:
    import http.client as http_client
    import http.server as http_server
    import urllib
else:
    import httplib as http_client
    import BaseHTTPServer as http_server
    import urllib2 as urllib
    import urlparse
    urllib.parse = urlparse
    urllib.parse.quote = urllib.quote


from thriftpy2.thrift import TProcessor
from thriftpy2.server import TServer
from thriftpy2.transport import TTransportBase, TMemoryBuffer, TTransportException

from thriftpy2.protocol import TBinaryProtocolFactory, TCompactProtocol
from thriftpy2.transport import TBufferedTransportFactory, TBufferedTransport

HTTP_URI = '{scheme}://{host}:{port}/{path}'
DEFAULT_HTTP_CLIENT_TIMEOUT_MS = 30000  # 30 seconds


class TFileObjectTransport(TTransportBase):

    def __init__(self, fileobj):
        self.fileobj = fileobj

    def isOpen(self):
        return True

    def close(self):
        self.fileobj.close()

    def read(self, sz):
        return self.fileobj.read(sz)

    def write(self, buf):
        self.fileobj.write(buf)

    def flush(self):
        self.fileobj.flush()


class ResponseException(Exception):

    def __init__(self, handler):
        self.handler = handler


class THttpHeaderFactory(object):

    def __init__(self, headers=None):

        if headers:
            self.__headers = headers
        else:
            self.__headers = dict()

    def get_headers(self):
        return self.__headers


class THttpServer(TServer):

    def __init__(self,
                 processor,
                 server_address,
                 itrans_factory,
                 iprot_factory,
                 server_class=http_server.HTTPServer):

        TServer.__init__(self, processor, trans=None,
                         itrans_factory=itrans_factory,
                         iprot_factory=iprot_factory,
                         otrans_factory=None, oprot_factory=None)

        thttpserver = self

        class RequestHander(http_server.BaseHTTPRequestHandler):

            def do_POST(self):
                content_len = int(self.headers['Content-Length'])
                buf = BytesIO(self.rfile.read(content_len))
                itrans = TFileObjectTransport(buf)
                itrans = thttpserver.itrans_factory.get_transport(itrans)
                iprot = thttpserver.iprot_factory.get_protocol(itrans)

                otrans = TMemoryBuffer()
                oprot = thttpserver.oprot_factory.get_protocol(otrans)
                try:
                    thttpserver.processor.process(iprot, oprot)
                except ResponseException as exn:
                    exn.handler(self)
                else:
                    self.send_response(200)
                    self.send_header("content-type", "application/x-thrift")
                    self.end_headers()
                    self.wfile.write(otrans.getvalue())

        self.httpd = server_class(server_address, RequestHander)

    def serve(self):
        self.httpd.serve_forever()


class THttpClient(object):

    def __init__(self, uri, timeout=None, ssl_context_factory=None, http_header_factory=None):
        parsed = urllib.parse.urlparse(uri)
        self.scheme = parsed.scheme
        assert self.scheme in ('http', 'https')

        if self.scheme == 'http':
            self.port = parsed.port or http_client.HTTP_PORT
        elif self.scheme == 'https':
            self.port = parsed.port or http_client.HTTPS_PORT

        self.host = parsed.hostname
        self.path = parsed.path
        if parsed.query:
            self.path += '?%s' % parsed.query

        try:
            proxy = urllib.request.getproxies()[self.scheme]
        except KeyError:
            proxy = None
        else:
            if urllib.request.proxy_bypass(self.host):
                proxy = None

        if proxy:
            parsed = urllib.parse.urlparse(proxy)
            self.realhost = self.host
            self.realport = self.port
            self.host = parsed.hostname
            self.port = parsed.port
            self.proxy_auth = self.basic_proxy_auth_header(parsed)
        else:
            self.realhost = self.realport = self.proxy_auth = None

        self.__wbuf = BytesIO()
        self.__http = None
        self.response = None
        self.__timeout = None
        self._http_header_factory = http_header_factory or THttpHeaderFactory()

        if timeout:
            self.setTimeout(timeout)
        self._ssl_context_factory = ssl_context_factory

    @staticmethod
    def basic_proxy_auth_header(proxy):
        if proxy is None or not proxy.username:
            return None
        ap = "%s:%s" % (urllib.parse.unquote(proxy.username),
                        urllib.parse.unquote(proxy.password))
        cr = base64.b64encode(ap).strip()
        return "Basic " + cr

    def using_proxy(self):
        return self.realhost is not None

    def open(self):
        if self.scheme == 'http':
            self.__http = http_client.HTTPConnection(self.host, self.port)

        elif self.scheme == 'https':
            self.__http = http_client.HTTPSConnection(self.host, self.port)

            if self.using_proxy():
                self.__http.set_tunnel(self.realhost, self.realport,{"Proxy-Authorization": self.proxy_auth})

    def close(self):
        self.__http.close()
        self.__http = None
        self.response = None

    def isOpen(self):
        return self.__http is not None

    def setTimeout(self, ms):
        if not hasattr(socket, 'getdefaulttimeout'):
            raise NotImplementedError

        self.__timeout = ms / 1000.0 if (ms and ms > 0) else None

    def setCustomHeaders(self, headers):
        self._http_header_factory = THttpHeaderFactory(headers)

    def read(self, sz):
        return self.response.read(sz)

    def readAll(self, sz):
        buff = b''
        have = 0
        while (have < sz):
            chunk = self.read(sz - have)
            have += len(chunk)
            buff += chunk

            if len(chunk) == 0:
                raise EOFError()

        return buff

    def write(self, buf):
        self.__wbuf.write(buf)

    def flush(self):

        data = self.__wbuf.getvalue()
        self.__wbuf = BytesIO()

        if not data:  # No data to flush, ignore
            return

        if self.isOpen():
            self.close()
        self.open()

        if self.using_proxy() and self.scheme == "http":
            self.__http.putrequest('POST', "http://%s:%s%s" %(self.realhost, self.realport, self.path))
        else:
            self.__http.putrequest('POST', self.path)
        #self.__http.putrequest('POST', self.path, skip_host=True)

        self.__http.putheader('Host', self.host)
        self.__http.putheader('Content-Type', 'application/x-thrift')
        self.__http.putheader('Content-Length', str(len(data)))
        if self.using_proxy() and self.scheme == "http" and self.proxy_auth is not None:
            self.__http.putheader("Proxy-Authorization", self.proxy_auth)

        custom_headers = self._http_header_factory.get_headers()

        if (not custom_headers or
                'User-Agent' not in custom_headers):
            user_agent = 'Python/THttpClient'
            script = os.path.basename(sys.argv[0])
            if script:
                user_agent = '%s (%s)' % (
                    user_agent, urllib.parse.quote(script))
                self.__http.putheader('User-Agent', user_agent)

        if custom_headers:
            for key, val in self._http_header_factory.get_headers().items():
                self.__http.putheader(key, val)

        self.__http.endheaders()

        self.__http.send(data)

        self.response = self.__http.getresponse()
        self.code = self.response.status
        self.message = self.response.reason
        self.headers = self.response.msg #getheaders()
        
        #(response.status, response.msg, response.getheaders())
        # Saves the cookie sent by the server response
        if 'Set-Cookie' in self.headers:
            self.__http.putheader('Cookie', self.headers['Set-Cookie'])
            print("cookies", str(self.headers))

    def __with_timeout(f):

        def _f(*args, **kwargs):
            orig_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(args[0].__timeout)
            result = None
            try:
                result = f(*args, **kwargs)
            finally:
                socket.setdefaulttimeout(orig_timeout)
            return result
        return _f

    if hasattr(socket, 'getdefaulttimeout'):
        flush = __with_timeout(flush)