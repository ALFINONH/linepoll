# -*- coding: UTF-8 -*-
"""
©
"""


from copy import deepcopy
from datetime import datetime

from pathlib import Path
from typing import Union, List, Dict, Any, Optional

from .linethrift.livejson import Database, CreateDatabase
from .linethrift.console import Console, make_client, make_clients, make_connect

from .Api.api import Api
from .Api.endpoint import Line_Endpoint
from .Api.liff import Liff
from .Api.poll import Poll
from .Api.talk import Talk
from .Api.timeline import Timeline
#from .Api.command import commands

__all__ =['Database', 'CreateDatabase', 'Path', 'Line_Endpoint']

class Linepoll(Api, Liff, Poll, Talk, Timeline,): #commands

    isLogin = False

    def __init__(self, authToken=None, authKey =None, email=None, password=None, lhost = 'gxx.line.naver.jp', device="IOS", version= None, system_name="Linepoll-Client", mod_name=None):
        assert device in Line_Endpoint.LA, 'Invalid Application types for %s \nCheck at app configuration types'%device

        self.console = Console
        self._func = Console.line_thrift
        self._client1 = make_client
        self._client2 = make_clients
        self._client3 = make_connect
        self.endpoint = Line_Endpoint
        
        self.host = f"https://{lhost}:443"
        self.url = f'https://{lhost}'

        self.APP_TYPE = device
        self.systemName = system_name

        Api.__init__(self)

        if not (authToken or email and password):
            self.secondaryQr(appType=device, systemName=os_name)

        if authToken:
            self.headers.update({'X-Line-Access': authToken})
            self.authToken = authToken
            self.login()

        elif authKey:
            self.generateAccessToken(authKey)
            
        elif(email and password):
            self.loginWithCredentialsForCrt(email,password)

        self.limit = False
        if(self.authToken and self.revision):
            self.initAll()

    def initAll(self):
        self.groups = self.talk.getGroupIdsJoined()
        self.friends = self.talk.getAllContactIds()
        self.profile = self.talk.getProfile()
        self.isLogin = True

        Liff.__init__(self)
        Poll.__init__(self)
        Talk.__init__(self)
        Timeline.__init__(self)
        #commands.__init__(self)
        self._loginLineTimeline()
        print(f"Name: {self.profile.displayName}\nMid: {self.profile.mid}\nAuthToken: {self.authToken}")
