# -*- encoding: UTF-8 -*-
from io import BytesIO
import os
import socket
import sys
import warnings
import base64
import urllib
from six.moves import http_client
import six
from .TTransport import TTransportBase


class THttpClient(TTransportBase):

    def __init__(self, uri_or_host, port=None, path=None):

        if port is not None:
            warnings.warn(
                "Please use the THttpClient('http://host:port/path') syntax",
                DeprecationWarning,
                stacklevel=2)
            self.host = uri_or_host
            self.port = port
            assert path
            self.path = path
            self.scheme = 'http'
        else:
            parsed = urllib.parse.urlparse(uri_or_host)
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
        self.__http_response = None
        self.__timeout = None
        self.__custom_headers = None

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
        self.__http_response = None

    def isOpen(self):
        return self.__http is not None

    def setTimeout(self, ms):
        if not hasattr(socket, 'getdefaulttimeout'):
            raise NotImplementedError

        if ms is None:
            self.__timeout = None
        else:
            self.__timeout = ms / 1000.0

    def setCustomHeaders(self, headers):
        self.__custom_headers = headers

    def read(self, sz):
        return self.__http_response.read(sz)

    def write(self, buf):
        try:
            self.__wbuf.write(buf)
        except Exception as e:
            self.__wbuf = BufferIO()
            raise e


    def __withTimeout(f):
        def _f(*args, **kwargs):
            orig_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(args[0].__timeout)
            try:
                result = f(*args, **kwargs)
            finally:
                socket.setdefaulttimeout(orig_timeout)
            return result
        return _f

    def flush(self):
        data = self.__wbuf.getvalue()
        self.__wbuf = BytesIO()
        if not data:
            return

        if self.isOpen():
            self.close()
        self.open()

        if self.using_proxy() and self.scheme == "http":
            self.__http.putrequest('POST', "http://%s:%s%s" %(self.realhost, self.realport, self.path))
        else:
            self.__http.putrequest('POST', self.path)

        self.__http.putheader('Host', self.host)
        self.__http.putheader('Connection', "Keep-Alive")
        self.__http.putheader('Content-Type', 'application/x-thrift')
        self.__http.putheader('Content-Length', str(len(data)))
        if self.using_proxy() and self.scheme == "http" and self.proxy_auth is not None:
            self.__http.putheader("Proxy-Authorization", self.proxy_auth)

        if not self.__custom_headers or 'User-Agent' not in self.__custom_headers:
            user_agent = 'Python/THttpClient'
            script = os.path.basename(sys.argv[0])
            if script:
                user_agent = '%s (%s)' % (user_agent, urllib.parse.quote(script))
            self.__http.putheader('User-Agent', user_agent)

        if self.__custom_headers:
            for key, val in six.iteritems(self.__custom_headers):
                self.__http.putheader(key, val)

        self.__http.endheaders()

        self.__http.send(data)

        self.__http_response = self.__http.getresponse()
        self.code = self.__http_response.status
        self.message = self.__http_response.reason
        self.headers = self.__http_response.msg

       # Saves the cookie sent by the server response
        if 'Set-Cookie' in self.headers:
            self.__http.putheader('Cookie', self.headers['Set-Cookie'])