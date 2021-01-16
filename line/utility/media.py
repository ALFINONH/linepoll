# -*- coding: UTF-8 -*-
"""
©alfino
"""
from bs4 import BeautifulSoup

import mechanize
import random
import requests
import json
import os
import urllib.parse

class Sms:
    def __init__(self, client=None):
        self.br = mechanize.Browser()
        if client != None:
            self._client = client
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders =[('Connection','keep-alive'),
            ('Pragma','no-cache'),
            ('Cache-Control','no-cache'),
            ('Origin','http://sms.payuterus.biz'),
            ('Upgrade-Insecure-Requests','1'),
            ('Content-Type','application/x-www-form-urlencoded'),
            ('User-Agent','Opera/9.80 (Android; Opera Mini/8.0.1807/36.1609; U; en) Presto/2.12.423 Version/12.16'),
            ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'),
            ('Referer','http://sms.payuterus.biz/alpha/'),
            ('Accept-Encoding','gzip, deflate'),
            ('Accept-Language','id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'),
            ('Cookie','_ga=GA1.2.131924726.1560439960; PHPSESSID=jjrqqaakmfcgfgbtjt8tve5595; _gid=GA1.2.1969561921.1561024035; _gat=1')
        ]
        self.u='http://sms.payuterus.biz/alpha/'

    def main(self, to, no, msg):
        o=[]
        bs = BeautifulSoup(self.br.open(self.u),features="html.parser")
        for x in bs.find_all("span"):
            o.append(x.text)
        capt=int(str(o)[2])+int(str(o)[6])
        self.br.select_form(nr=0)
        self.br.form['nohp']=no
        self.br.form['pesan']=msg
        self.br.form['captcha']=str(capt)
        sub=self.br.submit().read()
        if 'SMS Gratis Telah Dikirim' in str(sub):
            if self._client:
                self._client.sendMessage(to,"SMS Gratis Telah dikirim\nPesan: {}".format(str(msg)))
            else:
                print('[+] Sukses mengirim sms ke',no)
        elif 'Mohon Tunggu 8 Menit Lagi' in str(sub):
            if self._client:
                self._client.sendMessage(to,"Pesan berikut masih dalam proses, cobalah beberapa saat lagi".format(str(msg)))
            else:
                print('[!] Tunggu 8 menit untuk mengirim sms yang sama')
        else:
            if self._client:
                self._client.sendMessage(to,"Gagal mengirim sms\nSilahkan cek kembali nomor berikut atau pesan minimal tidak kurang dari 16 karakter".format(str(msg)))
            else:
                print('[-] Gagal mengirim sms ke',no)

class media(object):

    def __init__(self, client, assist=None):
        self.client = client
        self.wait = self.client.line['waits']
        self.settings = self.client.line['settings']
        self.host_photofunia = 'https://api.photofunia.com'
        self.path2 = {'sketch': '/2.0/effects/sketch','bride': '/2.0/effects/bride','neon': '/2.0/effects/neon','wanted': '/2.0/effects/wanted','summer-diary': '/2.0/effects/summer-diary','resident_evil_shooting': '/2.0/effects/resident_evil_shooting','snow-globe': '/2.0/effects/snow-globe','neon-writing': '/2.0/effects/neon-writing','passage': '/2.0/effects/passage','explorer-drawing': '/2.0/effects/explorer-drawing','light-writing': '/2.0/effects/light-writing','watercolour-text': '/2.0/effects/watercolour-text','number-plate': '/2.0/effects/number-plate','two-valentines': '/2.0/effects/two-valentines','calendar': '/2.0/effects/calendar','burning-fire': '/2.0/effects/burning-fire','retro-wave':  '/2.0/effects/retro-wave'}
        self.params2 = {'access_key': 'e3084acf282e8323181caa61fa305b2a','lang': 'en'}
        self.bool_dict = {True: ['yes', 'active'],False: ['no', 'deactive']}
        if(assist != None):
            self.assist=assist

    def urlEncode2(self,url, path, params=[]):
        return url + path + '?' + urllib.parse.urlencode(params)

    def optionsContent2(self,url, data=None, headers=None):
        return requests.Session().options(url, headers=headers, data=data)

    def postContent2(self,url, data=None, files=None, headers=None):
        return requests.Session().post(url, headers=headers, data=data, files=files)

    def getContent2(self,url, headers=None):
        return requests.Session().get(url, headers=headers, stream=True)

    def deleteContent2(self, url, data=None, headers=None):
        return requests.Session().delete(url, headers=headers, data=data)

    def putContent(self, url, data=None, headers=None):
        return requests.Session().put(url, headers=headers, data=data)

    """
    GEO MEDIA
    """
    def number_plate(self,mek, colour='orange'):
        url = self.urlEncode2(self.host_photofunia, self.path2['number-plate'], self.params2)
        data = {'text': mek, 'colour': colour}
        response = self.postContent2(url, data=data).json()
        anu = f"{response['response']['images']['large']['url']}"
        return anu

    def burning_fire(self,path):
        url = self.urlEncode2(self.host_photofunia, self.path2['burning-fire'], self.params2)
        data = {'name': 'image'}
        files = {'image': open(path, 'rb')}
        response = self.postContent2(url, data=data, files=files).json()
        anu = f"{response['response']['images']['regular']['url']}"
        return anu

    def calender(self, path, type='', year='2020'):
        url = self.urlEncode2(self.host_photofunia, self.path2['calendar'], self.params2)
        data = {'type': type, 'year': year}
        files = {'image': open(path, 'rb')}
        response = self.postContent2(url, data=data, files=files).json()
        mek = f"{response['response']['images']['large']['url']}"
        return mek

    def two_valentines(self,text, image, text2, image2):
        url = self.urlEncode2(self.host_photofunia, self.path2['two-valentines'], self.params2)
        data = {'text': text, 'text2': text2}
        files = {'image': open(image, 'rb'), 'image2': open(image2, 'rb')}
        response = self.postContent2(url, data=data, files=files).json()
        mek = f"{response['response']['images']['large']['url']}"
        return mek

    def summer_diary(self,image, text, image2):
        url = self.urlEncode2(self.host_photofunia, self.path2['summer-diary'], self.params2)
        data = {'text': text}
        files = {'image': open(image, 'rb'), 'image2': open(image2, 'rb')}
        response = self.postContent2(url, data=data, files=files).json()
        mek = f"{response['response']['images']['large']['url']}"
        return mek

    def bride(self,image):
        url = self.urlEncode2(self.host_photofunia, self.path2['bride'], self.params2)
        files = {'image': open(image, 'rb')}
        response = self.postContent2(url, files=files).json()
        mek = f"{response['response']['images']['large']['url']}"
        return mek

    def sketch(self,path, fade=True):
        url = self.urlEncode2(self.host_photofunia, self.path2['sketch'], self.params2)
        data = {'fade': self.bool_dict[fade][0], 'name': 'image'}
        files = {'image': open(path, 'rb')}
        response = self.postContent2(url, data=data, files=files).json()
        anu = f"{response['response']['images']['regular']['url']}"
        return anu
	
    def neon_writing(self,text, text2=None):
        url = self.urlEncode2(self.host_photofunia, self.path2['neon-writing'], self.params2)
        data = {'text': text, 'text2': text2}
        response = self.postContent2(url, data=data).json()
        anu = f"{response['response']['images']['large']['url']}"
        return anu
	
    def watercolour_text(self, text, text2=None, color=1, font='segoeprb', splashes=True):
        if color not in [1, 2, 3, 4, 5]:
            raise Exception('Invalid color value')
        if font not in ['segoeprb', 'lobster']:
            raise Exception('Invalid font value')
        url = self.urlEncode2(self.host_photofunia, self.path2['watercolour-text'], self.params2)
        data = {'text': text, 'text2': text2, 'color': color, 'font': font, 'splashes': self.bool_dict[splashes][0]}
        response = self.postContent2(url, data=data).json()
        anu = f"{response['response']['images']['large']['url']}"
        return anu
	
    def retro_wave(self,text1,text2,text3):
        url = self.urlEncode2(self.host_photofunia, self.path2['retro-wave'], self.params2)
        data = {'text1': text1, 'text2': text2, 'text3': text3}
        response = self.postContent2(url, data=data).json()
        anu = f"{response['response']['images']['large']['url']}"
        return anu
	
    def wanted(self,image,text1,text2,name,reward,signed,paper=True):
        url = self.urlEncode2(self.host_photofunia, self.path2['wanted'], self.params2)
        data = {'text1': text1, 'text2': text2, 'name': name, 'reward': reward, 'signed': signed, 'paper': self.bool_dict[paper][0]}
        files = {'image': open(image, 'rb')}
        response = self.postContent2(url, data=data, files=files).json()
        anu = f"{response['response']['images']['regular']['url']}"
        return anu
	
    def snow_globe(self,text,text2,image,animation="animated"):
        url = self.urlEncode2(self.host_photofunia, self.path2['snow-globe'], self.params2)
        data = {'text1': text, 'text2': text2, 'animation': animation}
        files = {'image': open(image, 'rb')}
        response = self.postContent2(url, data=data, files=files).json()

        anu = f"{response['response']['images']['regular']['url']}"
        return anu

    def resident_evil(self,path):
        url = self.urlEncode2(self.host_photofunia, self.path2['resident_evil_shooting'], self.params2)
        files = {'image': open(path, 'rb')}
        response = self.postContent2(url, files=files).json()
        anu = f"{response['response']['images']['regular']['url']}"
        return anu

    def info(self, name):
        name = name.replace(' ', '-')
        name = name.replace('_', '-')
        url = self.urlEncode2(self.host_photofunia, '/2.0/effects/' + name, self.params2)
        response = self.getContent2(url).json()
        print (json.dumps(response, indent=4, sort_keys=True))

class Zalgo():

    def __init__(self):
        self.numAccentsUp = (1, 3)
        self.numAccentsDown = (1,3)
        self.numAccentsMiddle = (1,2)
        self.maxAccentsPerLetter = 3
        self.dd = ['̖',' ̗',' ̘',' ̙',' ̜',' ̝',' ̞',' ̟',' ̠',' ̤',' ̥',' ̦',' ̩',' ̪',' ̫',' ̬',' ̭',' ̮',' ̯',' ̰',' ̱',' ̲',' ̳',' ̹',' ̺',' ̻',' ̼',' ͅ',' ͇',' ͈',' ͉',' ͍',' ͎',' ͓',' ͔',' ͕',' ͖',' ͙',' ͚',' ',]
        self.du = [' ̍',' ̎',' ̄',' ̅',' ̿',' ̑',' ̆',' ̐',' ͒',' ͗',' ͑',' ̇',' ̈',' ̊',' ͂',' ̓',' ̈́',' ͊',' ͋',' ͌',' ̃',' ̂',' ̌',' ͐',' ́',' ̋',' ̏',' ̽',' ̉',' ͣ',' ͤ',' ͥ',' ͦ',' ͧ',' ͨ',' ͩ',' ͪ',' ͫ',' ͬ',' ͭ',' ͮ',' ͯ',' ̾',' ͛',' ͆',' ̚',]
        self.dm = [' ̕',' ̛',' ̀',' ́',' ͘',' ̡',' ̢',' ̧',' ̨',' ̴',' ̵',' ̶',' ͜',' ͝',' ͞',' ͟',' ͠',' ͢',' ̸',' ̷',' ͡',]

    def Zalgofy(self, text):
        letters = list(text)
        newWord = ''
        newLetters = []
        for letter in letters:
            a = letter
            if not a.isalpha():
                newLetters.append(a)
                continue
            numAccents = 0
            numU = random.randint(self.numAccentsUp[0],self.numAccentsUp[1])
            numD = random.randint(self.numAccentsDown[0],self.numAccentsDown[1])
            numM = random.randint(self.numAccentsMiddle[0],self.numAccentsMiddle[1])
            while numAccents < self.maxAccentsPerLetter and numU + numM + numD != 0:
                randint = random.randint(0,2)
                if randint == 0:
                    if numU > 0:
                        a = self.combineWithDiacritic(a, self.du)
                        numAccents += 1
                        numU -= 1
                elif randint == 1:
                    if numD > 0:
                        a = self.combineWithDiacritic(a, self.dd)
                        numD -= 1
                        numAccents += 1
                else:
                    if numM > 0:
                        a = self.combineWithDiacritic(a, self.dm)
                        numM -= 1
                        numAccents += 1
            newLetters.append(a)
        newWord = ''.join(newLetters)
        return newWord

    def combineWithDiacritic(self, letter, diacriticList):
        return letter.strip() + diacriticList[random.randrange(0, len(diacriticList))].strip()

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

class Split(object):
    data_array = []
    datalist = []

    def __init__(self, logic, datalist):
        self.datalist = datalist
        self.logic = logic

    def parse(self):
        logics = self.parse_coma(self.logic)
        theresult = []
        for logic in logics:
            if ">" in logic:
                res01 = self.do_logic(logic)
                self.util_append(res01, theresult)
            elif "<" in logic:
                res02 = self.do_logic(logic)
                self.util_append(res02, theresult)
            elif "-" in logic:
                res03 = self.do_range(logic)
                self.util_append(res03, theresult)
            else:
                res04 = self.do_append(logic)
                self.util_append(res04, theresult)
        last_step = self.util_filter_doubled(theresult)
        last_step.sort()
        return last_step

    def util_filter_doubled(self, nestlists):
        dmp = []
        for reslist in nestlists:
            for item in reslist:
                if item not in dmp:
                    dmp.append(item)
                else:
                    pass
        return dmp

    def util_append(self, data, thelist):
        if data != None:
            thelist.append(data)

    def do_append(self, logic):
        try:
            number = int(logic)
            if number in self.datalist:
                return [number]
            else: return None
        except:
            return None

    def do_logic(self, logic):
        dmp = []
        for d in self.datalist:
            state = eval("{0}{1}".format(d,logic))
            if state:
                dmp.append(d)
        return dmp

    def do_range(self, logic):
        rangedata = self.parse_minus(logic)
        if len(rangedata) == 1:
            return None
        elif len(rangedata) == 2:
            the_min = min( (int(rangedata[0])) , (int(rangedata[1])) )
            the_max = max( (int(rangedata[0])) , (int(rangedata[1])) )
            listrange = range(the_min, the_max+1)
            dmp = []
            for iter in self.datalist:
                if iter in set(listrange):
                    dmp.append(iter)
            return dmp
        elif len(rangedata) >= 3:
            return None

    def parse_minus(self,logic):
        logic = logic.split('-')
        return logic

    def parse_coma(self, logic):
        dat = logic.split(',')
        dmp = []
        for item in dat:
            if item != '':
                dmp.append(item)
        return dmp

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
