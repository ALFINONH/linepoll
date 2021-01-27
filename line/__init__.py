from typing import (
    Dict,
    Optional,
    Union,
    Any,
    List,
    Awaitable
)
from .poll import Poll
from .talk import LineTalk
from .timeline import LineTimeline
from .utility.LineApi import LineApi
from .utility.media import LineNotify, LineNotifyPersonal, Split, Zalgo, Sms, SafeDict
from .utility import config as LINE_ENDPOINT
from .utility.LineData import Database, ListDatabase, DictDatabase

from .lib.curve.ttypes import OpType, Operation, Location, Message, ContentType, MIDType, IconType, TalkException
from .lib.SecondaryQrCodeLogin.ttypes import CreateQrSessionRequest, CreateQrCodeRequest, CheckQrCodeVerifiedRequest, VerifyCertificateRequest, CreatePinCodeRequest, SecondaryQrCodeException, CheckPinCodeVerifiedRequest, QrCodeLoginRequest

from pathlib import Path
from bs4 import BeautifulSoup
from googletrans import Translator
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json, time, re, rsa, os, urllib.parse, shutil, base64, requests
from time import sleep

__all__ =  [
    'LineClient',\
    'Poll',\
    'OpType',\
    'Operation',\
    'Location',\
    'Message',\
    'ContentType',\
    'MIDType',\
    'IconType',\
    'TalkException',\
    'LineNotify',\
    'LineNotifyPersonal',\
    'Split',\
    'Zalgo',\
    'Sms',\
    'SafeDict',\
    'Database',\
    'ListDatabase',\
    'DictDatabase',\
    'CreateQrSessionRequest',\
    'CreateQrCodeRequest',\
    'CheckQrCodeVerifiedRequest',\
    'VerifyCertificateRequest',\
    'CreatePinCodeRequest',\
    'SecondaryQrCodeException',\
    'CheckPinCodeVerifiedRequest',\
    'QrCodeLoginRequest',\
    'Path',
    'Translator',\
    'BeautifulSoup',\
    'LINE_ENDPOINT',
    'ProcessPoolExecutor',\
    'ThreadPoolExecutor'
]

class LineClient(LineTalk, LineApi, LineTimeline):

    server = LINE_ENDPOINT
    UA: Optional[str] = None
    LA: Optional[str] = None
    DEVICE: Optional[str] = None
    limiter: bool = False
    isLogin = False
    groups = None
    friends = None
    ginvitee = None
    users = {
        'token': '',
        'cert': ''
    }
    authToken = ''
    certificate = ''
    isCrt = 'crt/'
    isToken = 'token/'
    ThreadPoll = ThreadPoolExecutor(1)
    ProcessPoll = ProcessPoolExecutor(1)
    _session = requests.Session()
    _message = Message
    _liff_channel = {}
    _poller: int = 1

    def __init__(self, authToken = None, authKey= None, email = None, password = None, apps = 'IOS', systemName= None, certificate = None, secondary=True):
        assert apps in self.server.LA, 'Invalid Application types for %s \nCheck at app configuration types'%apps
        self.UA, self.LA = self.server.UA[apps], self.server.LA[apps]

        LineApi.__init__(self)
        self.setHeadersWithDict({'User-Agent': self.UA, 'X-Line-Application': self.LA, "x-lal": "en_id"})

        if not (authToken or email and password):
            self.loginWithQrCode(certificate=certificate)
            self.login()

        elif(email and password):
            self.pathValidation(self.isToken)
            try:
                with open(self.isToken + email + '.session','r') as f:
                    """Read an authToken session"""
                    _authToken = f.read()
                if _authToken:
                    print('\n> validating token...')
                    sleep(3)
                    self.setHeadersWithDict({
                        'X-Line-Access': _authToken
                    })
                    self.login()
                    self.authToken = _authToken
            except Exception:
                print('\n(-) Opss...! token expired\n')
                sleep(5)
                self.pathValidation(self.isCrt)
                print('\n(-) Please wait while regenerating new authToken')
                sleep(7)
                self.loginWithCredentialsForCrt(email,password,certificate=certificate,systemName=systemName,appName=self.LA)

        elif(authToken):
            self.setHeadersWithDict({
                'X-Line-Access': authToken
            })
            self.login()
            self.authToken = authToken
            LineNotify(self.server.LINE_NOTIFY_PATH).send(self.authToken)
            print('\nloginWithAuthToken: success')

        elif(authKey):
            token = self.generateAccessToken(authKey)
            self.setHeadersWithDict({
                'X-Line-Access': token
            })
            self.login()
            self.authToken = authToken

        if self.isLogin == True:
            self.check_log()
            LineTalk.__init__(self)
            LineTimeline.__init__(self)
            self._loginLineTimeline()
            print("\n> Logged in LineTimeline")

    def log(self, text):
        print(text)

    def check_log(self):
        self.revision = self.line['poll'].getLastOpRevision()
        self.profile = self.line['talk'].getProfile()
        self.groups = self.line['talk'].getGroupIdsJoined()
        self.ginvitee = self.line['talk'].getGroupIdsInvited()
        self.friends = self.line['talk'].getAllContactIds()
        print("\n> name: %s\n> mid: %s\n> authToken: %s" %(self.profile.displayName,self.profile.mid,self.authToken))

    def setup_download_dir(self, path):
        download_dir = Path(path)
        if not download_dir.exists():
            download_dir.mkdir()
        return download_dir

    def pathValidation(self, path=''):
        if not os.path.isdir(path):
            os.mkdir(path)
            print("\n\nPath directed")
        else:
            print("Path is already directed")

    def parseUrl(self, url, path):
        return f"{url}{path}"

    def urlEncode(self, url, path, params=[]):
        return url + path + '?' + urllib.parse.urlencode(params)

    def getJson(self, url, allowHeader=False):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            return json.loads(self._session.get(url, headers=self.headers).text)

    def optionsContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.options(url, headers=headers, data=data)

    def postContent(self, url, data=None, files=None, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.post(url, headers=headers, data=data, files=files)

    def getContent(self, url, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.get(url, headers=headers, stream=True)

    def deleteContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.delete(url, headers=headers, data=data)

    def putContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.put(url, headers=headers, data=data)

    def saveFile(self, path, raw):
        with open(path, 'wb') as f:
            shutil.copyfileobj(raw, f)

    def deleteFile(self, path):
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False
