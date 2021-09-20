import requests, json, sys, os

from typing import Union, List, Dict, Any, Optional

class LineNotify:
    def __init__(self, access_token, name=None):
        self.name = name
        self.accessToken = access_token

        if access_token:
            self.enable = True
            self.headers = {"Authorization": "Bearer " + access_token}
        else:
            self.enable = False
            self.headers = {}

    def on(self):
        self.enable = True

    def off(self):
        self.enable = False

    def format(self, message):
        if self.name:
            message = '[{0}] {1}'.format(self.name, message)

        return message

    def send(self, message, image_path=None, sticker_id=None, package_id=None):
        if not self.enable:
            return

        params = {"message": self.format(message)}
        if image_path and os.path.isfile(image_path):
            files = {"imageFile": open(image_path, "rb")}
            kirim = requests.post("https://notify-api.line.me/api/notify", headers=self.headers, params=params, files=files)
        elif sticker_id and package_id:
            params = {**params, "stickerId": sticker_id, "stickerPackageId": package_id}
            kirim = requests.post("https://notify-api.line.me/api/notify", headers=self.headers, params=params)
        else:
            kirim = requests.post("https://notify-api.line.me/api/notify", headers=self.headers, params=params)
        return kirim

class LineApiNotify:
    def __init__(self, token):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'notify-bot.line.me',
            'Referer': 'https://notify-bot.line.me/my/'
        }
        self.token = token

    def sendNotify(self, message):
        return self.session.post('https://notify-api.line.me/api/notify', headers={**self.headers, **{'Authorization': 'Bearer %s' % (self.token)}}, params={'message': message}).json()

    def revokeToken(self):
        return self.session.post('https://notify-api.line.me/api/revoke', headers={**self.headers, **{'Authorization': 'Bearer %s' % (self.token)}}).json()
        
class LineNotifyPersonal:
    def __init__(self, token, SESSION):
        self.token = token
        self.session = requests.session()
        for key, value in {'XSRF-TOKEN': token, 'SESSION': SESSION}.items():
            self.session.cookies.set_cookie(requests.cookies.create_cookie(key, value))

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'notify-bot.line.me',
            'Referer': 'https://notify-bot.line.me/my/'
        }

    def groupList(self, page=1):
        return self.session.get('https://notify-bot.line.me/api/groupList', headers=self.headers, params={'page': page}).json()

    def issuePersonalAcessToken(self, description, targetMid, targetType="GROUP"):
        data = {
            "action": "issuePersonalAcessToken",
            "description": description,
            "targetType": targetType,
            "targetMid": targetMid,
            "_csrf": self.token
        }
        return self.session.post('https://notify-bot.line.me/my/personalAccessToken', headers=self.headers, data=data).json()

    def createLineNotify(self, name, groupName):
        mid = [group['mid'] for group in self.groupList()['results'] if group['name'] == groupName]
        if not mid:
            raise Exception('can\' find group name')
        return LineApiNotify(self.issuePersonalAcessToken(name, mid[0])['token'])

    def send_to(self, token, session):
        client = LineNotifyPersonal(token, session)
        cl = client.createLineNotify('This is line notify api', 'chat')
        cl.sendNotify(cl.token)
        cl.revokeToken()

class View(object):
    def __init__(self, type=None, url=None):
        self.type, self.url = type, url

    def read(self, map_array):
        try:
            self.type = map_array.get('type',None)
            self.url  = map_array.get('url', None)
        except:
            self.type, self.url = type, url

    def write(self):
        return {'type':self.type, 'url':self.url}

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

class LiffApp(object):
    def __init__(self, liffId=None, view=None):
        self.liffId, self.view = liffId, view

    def read(self, map_array):
        try:
            view = View(); view.read(map_array.get('view',{}))
            self.liffId,self.view=map_array.get('liffId',None),view
        except:
            self.liffId,self.view = liffId,view

    def write(self):
        return {'liffId':self.liffId, 'view': self.view.write()}

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

class ChannelLoginResult(object):
    def __init__(self, access_token=None,expires_in=None,token_type=None):
        self.access_token,self.expires_in,self.token_type=access_token,expires_in,token_type

    def read(self, map_array):
        try:
            self.access_token = map_array.get('access_token', None)
            self.expires_in   = map_array.get('expires_in', None)
            self.token_type   = map_array.get('token_type', None)
        except:
            self.access_token,self.expires_in,self.token_type=access_token,expires_in,token_type

    def write(self):
        return {'access_token':self.access_token,'expires_in':self.expires_in,'token_type':self.token_type}

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

class LiffException(Exception):
    if (2, 6, 0) <= sys.version_info < (3, 0):

        def _get_message(self):
            return self._message

        def _set_message(self, message):
            self._message = message
        message = property(_get_message, _set_message)

    def __init__(self, code, headers, message=None):
        Exception.__init__(self, code, headers, message)

class LINELiff(object):
    channelId = None
    channelSecret = None
    liffId = []
    headers = {}
    _logged_in = False

    def __init__(self, log=True, debug=True):
        self.en_log,self.en_debug = log, debug

    def _error(self, *args, **kws):
        f = '->'
        x = ['[Error]']
        for arg in args:
            x += [arg]
            if args.index(arg) < len(args) - 1:
                x += [f]
        if self.en_debug == True:
            print(*x)

    def _log(self, *args, **kws):
        f = '->'
        x = ['[Log]']
        for arg in args:
            x += [arg]
            if args.index(arg) < len(args) - 1:
                x += [f]
        if self.en_log == True:
            print(*x)

    def issueChannelAccessToken(self, channelId, channelSecret=None):
        api = 'https://api.line.me/v2/oauth/accessToken'
        ret = requests.post(api, 
            data={
                'grant_type':'client_credentials', 
                'client_id'    : channelId,
                'client_secret': channelSecret
        })
        if ret.status_code != 200:
            self._error('login respose code != 200', ret.status_code)
            try:
                raise LiffException(ret.status_code, ret.headers, ret.json())
            except:
                raise LiffException(ret.status_code, ret.headers, ret.content)
        try:
            jsn = ret.json()
            access_token = jsn.get('access_token', '')
            if access_token == '':
                self._error('No access_token returned', ret.content)
            else:
                self.headers.update({
                    'Authorization': f'Bearer {access_token}'
                    })
                self.channelId, self.channelSecret = channelId, channelSecret
                self._logged_in = True
                rx = ChannelLoginResult()
                rx.read(jsn)
                self._log('AccessToken', access_token)
                self._log('Expires', jsn.get('expires_in', 'null'))
        except Exception as e:
            self._error(e)

        return rx

    login = issueChannelAccessToken
    def updateLiffApp(self, LiffAppReq):
        liffId = LiffAppReq.liffId
        assert liffId != None, 'LiffId is null'
        api = f'https://api.line.me/liff/v1/apps/{liffId}/view'
        assert self._logged_in, 'You must be logged in.'
        assert LiffAppReq.view.type in ('compact', 'tall', 'full'), f'Invalid type "{type}". Only compact, tall, or full'
        ret = requests.put(api, 
            headers=self.headers,
            json=LiffAppReq.view.write())
        if ret.status_code != 200:
            self._error('updateLiffApp respose code != 200', ret.status_code)
            try: raise LiffException(ret.status_code, ret.headers, ret.json())
            except: raise LiffException(ret.status_code, ret.headers, ret.content)
        return True

    def getLiffApp(self):
        api = 'https://api.line.me/liff/v1/apps'
        assert self._logged_in, 'You must be logged in.'
        ret = requests.get(api, 
            headers=self.headers)
        if ret.status_code != 200:
            self._error('getLiffApp respose code != 200', ret.status_code)
            try: raise LiffException(ret.status_code, ret.headers, ret.json())
            except: raise LiffException(ret.status_code, ret.headers, ret.content)
        rx = []
        try:
            jsn = ret.json()
            apps = jsn.get('apps', [])
            if apps == []:
                pass
            else:
                for app in apps:
                    fx = LiffApp()
                    fx.read(app)
                    rx += [fx]
        except Exception as e:
            self._error(e)
        return rx

    def deleteLiffApp(self, liffId):
        api = f'https://api.line.me/liff/v1/apps/{liffId}'
        assert self._logged_in, 'You must be logged in.'
        ret = requests.delete(api, 
            headers=self.headers)
        if ret.status_code != 200:
            self._error('deleteLiffApp respose code != 200', ret.status_code)
            try: raise LiffException(ret.status_code, ret.headers, ret.json())
            except: raise LiffException(ret.status_code, ret.headers, ret.content)
        return True

    def createLiffApp(self, type, view_url):
        api = 'https://api.line.me/liff/v1/apps'
        assert self._logged_in, 'You must be logged in.'
        assert type in ('compact', 'tall', 'full'), f'Invalid type "{type}". Only compact, tall, or full'
        ret = requests.post(api,
            headers=self.headers,
            json={
                'view': {
                    'type': type,
                    'url' : view_url,
                }
        })
        if ret.status_code != 200:
            self._error('createLiffApp respose code != 200', ret.status_code)
            try: raise LiffException(ret.status_code, ret.headers, ret.json())
            except: raise LiffException(ret.status_code, ret.headers, ret.content)
        try:
            jsn = ret.json()
            liffId = jsn.get("liffId", '')
            if liffId == '':
                self._error('No liffId returned', ret.content)
            else:
                self._log('LiffId', liffId)
                self.liffId.append(liffId)
                fx = LiffApp()
                fx.read(jsn)
        except Exception as e:
            self._error(e)
        return fx

class Liff:

    _liff_channel = {}

    def __init__(self):
        self.isLoggin = True

    def setLiffHeaders(self, token):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token),
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; X9009 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36 Line/11.5.1 LIFF",
            "X-Requested-With": "jp.naver.line.android"
        }
        return headers

    def refreshLiffChannelAccessToken(self, id):
        liff_struct = self._func.LiffViewRequest(
                '1654055086-BoD0ExEX',
                self._func.LiffContext(chat = self._func.LiffChatContext(id))
        )
        self._liff_channel[id] = self.liff.issueLiffView(liff_struct).accessToken
        return self._liff_channel[id]

    def createLiffChannelId(self, type, authToken, url):
        data = {
            "view": {
                "type": type,
                "url": url
            }
        }
        req = requests.post("https://api.line.me/liff/v1/apps", json=data, headers=self.setLiffHeaders(authToken))
        result = json.loads(req.text)
        liffid = result["liffId"]
        return liffid

    def issueLiffLogin(self, channelId, channelScreet):
        data = {
            "grant_type": "client_credentials",
            "client_id": channelId,
            "client_secret": channelSecret
        }
        req = requests.post("https://api.line.me/v2/oauth/accessToken", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        result = json.loads(req.text)
        authToken = result["access_token"]
        return authToken

    def getLiffVerifierPermission(self, channelId: Optional[str] = None):
        if channelId is None:
            channelId = self.endpoint.CHANNEL_ID['LIFF']

        headers = deepcopy(self.headers)
        headers["User-Agent"] ="Mozilla/5.0 (Linux; Android 5.1; X9009 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36"
        headers["Content-Type"] = "application/json"
        headers["X-Requested-With"] = "jp.naver.line.android"
        headers["X-Line-ChannelId"] = channelId
        r = requests.post('https://access.line.me/dialog/api/permissions', json={'on': ['P','CM'],'off': []}, headers=headers)
        return r

    def issueLiffChannelToken(self, channelId=None, channelScreet=None):
        if(channelId == None):
            channelId = self.endpoint.CHANNEL_ID['LIFF']

        elif(channelScreet==None):
            channelScreet = self.endpoint.CHANNEL_ID['LIFF']

        apps = LINELiff()
        apps.login(channelId,channelScreet)
        print(str(apps))
        return apps

    def listLiffChannel(self, channelId=None, channelScreet=None):
        if(channelId == None):
            channelId = self.endpoint.CHANNEL_ID['LIFF']

        elif(channelScreet==None):
            channelScreet = self.endpoint.CHANNEL_SCREET['LIFF']

        apps = self.issueLiffChannelToken(channelId, channelScreet)
        apps.login(channelId,channelScreet)
        list_apps ="{}".format(apps.getLiffApp())
        numeric = list_apps.replace("LiffApp(liffId='","line://app/").replace("', view=View(type='full', url='"," url= ").replace("')),",",\n").replace("'))]"," ]")
        numeric_result = numeric.replace("[line","[ line")
        return numeric_result

    def deleteLiffApps(self, liffId, channelId=None, channelScreet=None):
        liff_apps = self.issueLiffChannelToken(channelId, channelScreet)
        try:
            liff_apps.deleteLiffApp(liffId)
        except Exception as e:
            print(str(e))

    def createLiffApps(self, view: str, url: str, channelId=None, channelScreet=None):
        assert view in ['compact','tall','full'], 'Invalid type "%s". Only compact, tall, or full'%view
        liff_apps = self.issueLiffChannelToken(channelId, channelScreet)
        try:
            liff_apps.createLiffApp(view, url)
        except Exception as e:
            print(str(e))

    def updateLiffApps(self, liffId, view, channelId=None, channelScreet=None):
        assert view in ['compact','tall','full'], 'Invalid type "%s". Only compact, tall, or full'%view
        liff_apps = self.issueLiffChannelToken(channelId, channelScreet)
        try:
            liff_apps.updateLiffApp(LiffApp(liffId=liffId, view=view))
        except Exception as e:
            print(str(e))

    def createLiffAppsChannel(self, type, clientid, channelsecret, url):
        authToken = self.issueLiffLogin(clientid, channelsecret)
        liff_id = self.createLiffChannelId(type, authToken, url)
        hsl = f"your appId: line://app/{liff_id}"
        return hsl

    def liff_add(self, url, size_type, channelId, channelScreet):
        authToken = self.issueLiffLogin(channelId, channelScreet)
        data = {
            "view": {
                "type": size_type,
                "url": url
            }
        }
        response = requests.post("https://api.line.me/liff/v1/apps", headers=self.setLiffHeaders(authToken), json=data)
        response_json_dic = json.loads(response.text)
        return response_json_dic

    def liff_delete(self, liff_id, channelId, channelScreet):
        authToken = self.issueLiffLogin(channelId, channelScreet)
        return requests.delete("https://api.line.me/liff/v1/apps" + "/" + liff_id, headers=self.setLiffHeaders(authToken))

    def liff_update(self, liff_id, view, channelId, channelScreet):
        authToken = self.issueLiffLogin(channelId, channelScreet)
        return requests.put("https://api.line.me/liff/v1/apps" + "/" + liff_id + "/view", headers=self.setLiffHeaders(authToken), json=view)

    def liff_list(self, channelId, channelScreet):
        authToken = self.issueLiffLogin(channelId, channelScreet)
        response = requests.get("https://api.line.me/liff/v1/apps", headers=self.setLiffHeaders(authToken))
        response_json_dic = json.loads(response.text)
        return response_json_dic

    def post_video(self, id: str, url: str, icon: Optional[str] = None):
        if id in self._liff_channel: token = self._liff_channel[id]
        else:token = self.refreshLiffChannelAccessToken(id)
        if icon== None: 'https://i.imgur.com/hT4U9vs.png'
        data = {
            "type": "video",
            "originalContentUrl": url,
            "previewImageUrl": icon
        }
        result = requests.post('https://api.line.me/message/v3/share', json={"messages":[data]}, headers=self.setLiffHeaders(token))
        if result.status_code != 200:
            raise Exception("[ Error ] Fail post video")
        return

    def post_audio(self, id: str, url: str):
        if id in self._liff_channel: token = self._liff_channel[id]
        else:token = self.refreshLiffChannelAccessToken(id)
        data = {
            "type": "audio",
            "originalContentUrl": url,
            "duration": 1000
        }
        result = requests.post('https://api.line.me/message/v3/share', json={"messages":[data]}, headers=self.setLiffHeaders(token))
        if result.status_code != 200:
            raise Exception("[ Error ] Fail post audio")
        return

    def sendTemplate(self, id: str, m: str):
        try:
            if id in self._liff_channel: token = self._liff_channel[id]
            else:token = self.refreshLiffChannelAccessToken(id)
            requests.post('https://api.line.me/message/v3/share', headers=self.setLiffHeaders(token), data=json.dumps({"messages":[m]}))
        except:
            self.sendMessage(id, "LiffId unverified\n Let's try again...!")
            self.getLiffVerifierPermission()

    def sendFlex(self, id: str, m: str, altText: Optional[str] = "Linepoll-Client"):
        try:
            if id in self._liff_channel: token = self._liff_channel[id]
            else:token = self.refreshLiffChannelAccessToken(id)
            data = {
               "messages":[
                {
                  'type': 'flex',
                  'altText': altText,
                  'contents': m
                }
              ]
            }
            requests.post('https://api.line.me/message/v3/share', headers=self.setLiffHeaders(token), data=json.dumps(data))
        except:
            self.sendMessage(id,"LiffId unverified\n Let's try again...!")
            self.getLiffVerifierPermission()

    def sendCarousel(self, id: str, d: Union[dict]):
        try:
            if id in self._liff_channel: token = self._liff_channel[id]
            else:token = self.refreshLiffChannelAccessToken(id)
            requests.post('https://api.line.me/message/v3/share', data=json.dumps(d), headers=self.setLiffHeaders(token))
        except:
            self.sendMessage(id, "LiffId unverified\n Let's try again...!")
            self.getLiffVerifierPermission()

    def eventTrue(self, settings, to: str, text: str):
        if(to in settings['template']):
            m = {
                "type":"flex","altText":"Line sendMessage","contents":{"type":"bubble","size":"kilo","body":{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"baseline","contents":[{"type":"icon","url":"https://i.imgur.com/hE7qxyC.png","size":"xxl","offsetStart":"1px","offsetBottom":"25px"}],"width":"30px","height":"25px","backgroundColor":"#00cc00ff","paddingAll":"0px","offsetBottom": "6px"},{"type":"box","layout":"horizontal","contents":[{"type":"separator"},{"type":"text","text":text,"size":"xs","color":"#ffffff","offsetStart":"1px"}],"backgroundColor":"#00cc00ff"}],"height":"18px","paddingAll":"0px","cornerRadius":"5px","backgroundColor":"#00cc00ff"}}
            }
            self.sendTemplate(to, m)
        else:
            self.sendMessage(to, text)

    def eventFalse(self, settings, to: str, text: str):
        if(to in settings['template']):
            m = {
                "type":"flex","altText":"Line sendMessage","contents":{"type":"bubble","size":"kilo","body":{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"baseline","contents":[{"type":"icon","url":"https://i.imgur.com/UnYhQRU.png","size":"xxl","offsetStart":"1px","offsetBottom":"25px"}],"width":"30px","height":"25px","backgroundColor":"#ff0000","paddingAll":"0px","offsetBottom": "6px"},{"type":"box","layout":"horizontal","contents":[{"type":"separator"},{"type":"text","text":text,"size":"xs","color":"#ffffff","offsetStart":"1px"}],"backgroundColor":"#ff0000"}],"height":"18px","paddingAll":"0px","cornerRadius":"5px","backgroundColor":"#ff0000"}}
            }
            self.sendTemplate(to, m)
        else:
            self.sendMessage(to, text)

    def cmds(self, to: str, text: str, load: bool = False, label: Optional[str] = None):
        if load == True: limg = 'https://i.imgur.com/DPQvsdx.gif'
        else: limg = 'https://i.imgur.com/hT4U9vs.png'
        if label == None: label = "Linepoll-Client 2021?"
        data = {
            "type": "text",
            "text": "{}".format(text),
            "sentBy": {
                "label": "%s"%label,
                "iconUrl": '%s'%limg,
                "linkUrl": "line://nv/profilePopup/mid=u0be3650c6619cc078452ce5ec11a86db"
            }
        }
        return self.sendTemplate(to, data)

    """Line Notify"""
    def logError(self, name, text, url_path = None):
        if(url_path is None):
            url_path = 'e587jHYMewAYbDYHk5nCiF08PDYZk771DlWJo7f2VA2'

        pesan_kirim = LineNotify(url_path)
        return pesan_kirim.send('\n=> {}\n->> {}'.format(name,text))

    def notification(self, text, url_path=None, name=None,image_path=None, sticker_id=None, package_id=None):
        """Support for free sticker_id or package_id only / image path only ,not support url image path given"""
        if(url_path == None):
            url_path = 'e587jHYMewAYbDYHk5nCiF08PDYZk771DlWJo7f2VA2'

        if(name==None):
            name= '> Line Notify\n'

        pesan_text = f"file > {name}\n\n{text}"
        pesan_kirim = LineNotify(url_path)
        return pesan_kirim.send(pesan_text, image_path=image_path,sticker_id=sticker_id, package_id=package_id)
