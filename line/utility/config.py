# -*- coding: UTF-8 -*-

"""
©Alfinonh
"""
from ..lib.curve.ttypes import OpType
import re

LEGY_HOST = "https://legy-jp.line.naver.jp"
GXX_HOST = 'https://gxx.line.naver.jp'
GWX_HOST = 'https://gwx.line.naver.jp'
GA2S_HOST = "https://ga2s.line.naver.jp"
GD2_HOST = "https://gd2.line.naver.jp"
GF_HOST = 'https://gf.line.naver.jp'
GFS_HOST = 'https://gfs.line.naver.jp'

TIMELINE_API = 'https://gd2.line.naver.jp/mh/api'
TIMELINE_MH = 'https://gd2.line.naver.jp/mh'

OBS_HOST = "https://obs.line-apps.com"
OBS_SG_HOST = 'https://obs-sg.line-apps.com'

PROFILE_PATH = "https://profile.line-scdn.net"
PROFILE_DL_PATH = "http://dl.profile.line-cdn.net/"
POLL_PATH = "/P4"
TALK_PATH = "/S4"
MESSAGE_PATH = "/F4"
CALL_PATH = '/V4'
CHANNEL_PATH = '/CH4'
LIFF_PATH = '/LIFF1'
BUDDY_PATH = "/BUDDY4"
CERTIFICATE_PATH = '/Q'
SHOP_PATH = '/SHOP4'
TSHOP_PATH = "/TSHOP4"
NOTIFY_PATH = "/B"
STICON_PATH = "/SC4"
SQUARE_PATH = '/SQS1'
SPOT_PATH = "/SP4"
AGE_PATH = "/ACS4"

LOGIN_QUERY_PATH = '/api/v4p/rs'
AGE_REGISTRATION = "api/v4p/acs"
AUTH_QUERY_PATH  = '/api/v4/TalkService.do'
SECONDARY_REGISTER = "/acct/pais/v1"
SECONDARY_LOGIN_REQUEST = "/acct/lgn/sq/v1"
SECONDARY_LOGIN_CHECK = "/acct/lp/lgn/sq/v1"

LIFF_MESSAGE = 'https://api.line.me/message/v3/share'
LIFF_VERIFIER = 'https://access.line.me/dialog/api/permissions'
LINE_NOTIFY_PATH = 'NOTIFY_TOKEN'
LINE_SESSION_URL = "https://gd2.line.naver.jp/authct/v1/keys/line"
NAVER_SESSION_URL = "https://gd2.line.naver.jp/authct/v1/keys/naver"

BOT_ICON_PATH = 'https://i.imgur.com/hT4U9vs.png'
BOT_ID = 'u0be3650c6619cc078452ce5ec11a86db'
OWN_ID = 'u0eb030f2c26cec938f56c7fe75dcc6bd'
KEY_BITLY = 'BITLY_API_KEY'
KEY_OWMAP = "OPEN_WEATHER_APIKEY"
KEY_WMAP= "WEATHER_APIKEY" 
KEY_AMAP_FREE = 'APIKEY'
KEY_AMAP_PREM = 'b7KA5wfYVghgsytgekouh2833zR5v95GFMRWAtsCAxeIb'
KEY_PRAY_TIME = '8dcc83ae296d964cb73a8f8b00f61887'
KEY_RBG = 'SGMKWRkMkVf6FWHBDnRmjFNN017jgzyhveoi'
KEY_FLATICON = "64b1a45e07e6223a78541f58be7e2a73gTfh65da7a1d1d0"
KEY_YMAP = "AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD744GTHy"
KEY_YMP4 = "AIzaSyAgJGvMH90cZlTAVFRPyWbcg_xRUCNpnIgFgH70Lkmn"
KEY_THUMBNAIL = "ab5cf6d383e99cb13d766c566780b44b26beda1ba4fs46Hgv88"

UA = {
   "ANDROID":"Line/10.18.0",
   "ANDROIDLITE":"LLA/2.11.1 Nexus 5X 10",
   "ANDROID_ALPHA":"androidapp.line/10.18.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
   "BIZBOT":"",
   "BOT":"androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
   "CHROMEOS":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
   "DESKTOPWIN":"Line/5.21.3",
   "IOS":"Line/10.3.0 iPhone8,1 13.3",
   "IOSIPAD":"Line/10.3.0 iPhone8,1 13.3",
   "MAC":"DESKTOP:MAC:10.9.4-MAVERICKS-x64(5.1.2)",
   "VIRTUAL":"Virtual.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
   "WAP":"WAPapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
   "WEB":"Line/2017.0731.2132 CFNetwork/758.6 Darwin/15.0.0"
}
LA = {
    'ANDROID': "ANDROID\t10.18.0\tAndroid\tOS\t6.0",
    'ANDROIDLITE': "ANDROIDLITE\t2.11.1\tAndroid\tOS\t6.0",
    'ANDROID_ALPHA': "ANDROID\t10.18.0\tAndroid\tOS\t6.0",
    'BOT': 'BOT\t1.7.2\tLinux Kernel\t3.14.7',
    'BIZBOT': '',
    'CHROMEOS': "CHROMEOS\t2.3.8\tChrome\tOS\t83.0.4103.97",
    'DESKTOPWIN': 'DESKTOPWIN\t5.21.3\WINDOWS\t10.0',
    'IOS': "IOS\t10.3.0\tiOS\t13.3",
    'IOSIPAD': "IOSIPAD\t10.3.0\tiPhone\tOS\t13.3",
    'MAC': "DESKTOPMAC\t10.9.4-MAVERICKS-x64\tMAC\t5.1.2",
    'VIRTUAL': 'VIRTUAL\t10.3.0\tLINE_VIRTUAL\t7.5.0',
    'WAP': 'WAP\t10.3.0\tiPhone\tOS\t1',
    'WEB': 'WEB\t10.3.0\tiPhone\tOS\t1'
}

CHANNEL_ID = {
    'TIMELINE': '1341209850',
    'WEBTOON': '1401600689',
    'TODAY': '1518712866',
    'STORE': '1376922440',
    'MUSIC': '1381425814',
    'SERVICES': '1459630796',
    'LIFF': '1654055086',
    'LIFF_V1': '1654260419',
    'LIFF_V2': '1654578478',
    'LIFF_SERVICE': '1654055086-BoD0ExEX' #'1604066537-dl9GVZzo'
}

CHANNEL_SCREET = {
    'LIFF': 'LINE_CHANNEL_SCREET',
    'LIFF_V1': 'LINE_CHANNEL_SCREET',
    'LIFF_V2': 'LINE_CHANNEL_SCREET',
    'XSRF-TOKEN':"0cf2eed5-20e1-93e2dbc3a51d",
    'SESSION1': 'YzVmMzMy00NzI1LTk2OTYtODZiNjBiZDAwNmI3',
    'SESSION2': 'MjI3C00NTY1LTlhYWMtMjhiMzg0YmRlMDcy'
}

LINK_COMPILER = re.compile(r'^(?:http|ftp)s?://' r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' r'localhost|' r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' r'(?::\d+)?' r'(?:/?|[/?]\S+)$', re.IGNORECASE)
MID_COMPILER = re.compile(r'u\w{32}')
GID_COMPILER = re.compile(r'c\w{32}')
ROOM_COMPILER = re.compile(r'r\w{32}')
MGR_COMPILER = re.compile(r'(?:u\w{32}|c\w{32}|r\w{32})')
ROOM = {
    "ROM": {},
    "absen": {},
    "id": {},
    "lurking": {}
}
STICKER1 = {}
STICKER2 = {}
STICKER3 = {}
VIDEOS = {}
AUDIOS = {}
IMAGES = {}
USERS = {
    "info": {},
    "name": {}
}
GROUP  = {
    OpType.NOTIFIED_UPDATE_GROUP: {
        "type": {
            'groupname': {
                'name': '',
                'status': False
            },
            'grouppicture': {
                'path': '',
                'status': False
            },
            'grouplink': {
                'status': False
            }
        }
    },
    OpType.NOTIFIED_INVITE_INTO_GROUP: False,
    OpType.NOTIFIED_CANCEL_INVITATION_GROUP: False,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: False,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: False
}

DATA = {
   "Addaudio":{
      "name":"",
      "status":False
   },
   "Addimage":{
      "name":"",
      "status":False
   },
   "Addvideo":{
      "name":"",
      "status":False
   },
   "DPC":False,
   "DPCV":False,
   "DPG":{},
   "DPP":False,
   "RreadMember":{},
   "RreadPoint":{},
   "addContact":False,
   "admin":[
     OWN_ID
   ],
   "anti":{},
   "assist":{},
   "autoAdd":{
      "pesan":"ʰⁱ @! ᵗʰᵃⁿᵏ'ˢ ᶠᵒʳ ᵃᵈᵈ ᵐᵉ",
      "reply":True,
      "status":False
   },
   "autoJoin":{
      "message":"ᵗʰᵃⁿᵏ'ˢ ᶠᵒʳ ⁱⁿᵛⁱᵗᵉᵈ ᵐᵉ @!",
      "reply":True,
      "status":True,
      "ticket":True
   },
   "autoJoinTicket":False,
   "autoLike":{
      "comment":"ᴍᴀɴᴜᴀʟ ʟɪᴋᴇ ʙʏ \\U00100503\\U0010010eline\\U0010ffff\n\n›››› https://tinyurl.com/a-nhofficial",
      "status":False
   },
   "autoRead":False,
   "autoRespond":{
      "message":"ʰᵉˡˡᵒ @!,\nⁿᵒ ʳᵉᵖˡʸ, ᵗʰⁱˢ ⁱˢ ᵃᵘᵗᵒ ʳᵉˢᵖᵒⁿ",
      "status":False
   },
   "autoRespondMention":{
      "message":"ʰᵉˡˡᵒ @!, ᵗʰᵃⁿᵏ'ˢ ᶠᵒʳ ᵐᵉⁿᵗⁱᵒⁿᵉᵈ ᵐᵉ",
      "status":False
   },
   "autoTranslate":{},
   "auto_download_link":{},
   "blacklist":{},
   "bots":{},
   "defaultReplyReader":"ʰⁱ @!, ʲᵒⁱⁿ ᵘˢ ᵗᵒ ᶜʰᵃᵗ.",
   "download":False,
   "file_name":{
      "name":"",
      "status":""
   },
   "gname":{},
   "imgbb":False,
   "invite":True,
   "kflood":{
      
   },
   "logos":{
      "icon":"https://i.imgur.com/urRc6WD.png",
      "imgurl":[
         "https://i.imgur.com/edOpohH.jpg",
         "https://i.imgur.com/HmH0gO9.jpg"
      ],
      "logo":[
         "https://i.imgur.com/TwGwKYv.jpg",
         "https://i.imgur.com/90972oQ.png",
         "https://i.imgur.com/uFybpPi.png"
      ]
   },
   "mp3":[
      
   ],
   "mute":{
      
   },
   "notifCall":False,
   "notify":{
      "login-monitoring":"LINE_NOTIFY_TOKEN",
      "room-monitoring":"LINE_NOTIFY_TOKEN"
   },
   "nyusup":False,
   "owner":[
       OWN_ID,
       BOT_ID,
      "u8e6d34247f5f0adc92bf10a399f94fbc",
      "u34db2135ede0ad557417c6d7f123bb7e"
   ],
   "param":{
      "join":{
         "message":"Hello @!, welcome to group {name}",
         "status":False
      },
      "leave":{
         "message":"Good bye @!, See u next time...",
         "status":False
      }
   },
   "postId":[],
   "prefix":{
      "key":"",
      "status":False
   },
   "protectcancel":[],
   "protectinvite":[],
   "protectjoin":[],
   "protectkick":[],
   "protectname":[],
   "protectpicture":[],
   "protectqr":[],
   "rContact":False,
   "rSticker":False,
   "receivecount":1,
   "removebg":False,
   "restartPoint":"cff1a49280851a827092e30f72676180a",
   "rname":True,
   "savecall":{},
   "send":{
      "audio":"line://app/1604066537-dl9GVZzo?type=audio&link=",
      "my-room":"ca567277b6710d3334c6d5757b6f6a3db",
      "text":"line://app/1604066537-dl9GVZzo?type=text&text="
   },
   "sendcount":1,
   "squad":"c1a4c47f36191e682e2cc5a4d82b0538c",
   "staff":[],
   "sticker1":{
      "name":"",
      "status":False
   },
   "sticker2":{
      "name":"",
      "status":False
   },
   "sticker3":{
      "name":"",
      "status":False
   },
   "stickerflood":{},
   "template":{},
   "timeline":False,
   "token":True,
   "translate":{},
   "unsendMessage":{},
   "userAgent":[
      "Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
      "Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
      "Mozilla/5.0 (X11; Linux) Gecko Firefox/5.0",
      "Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 FirePHP/0.5",
      "Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Firefox/5.0",
      "Mozilla/5.0 (X11; Linux x86_64) Gecko Firefox/5.0",
      "Mozilla/5.0 (X11; Linux ppc; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (X11; Linux AMD64) Gecko Firefox/5.0",
      "Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:5.0) Gecko/20110619 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 6.1.1; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 5.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 5.1; U; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 5.0; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
      "Mozilla/5.0 (Windows NT 5.0; rv:5.0) Gecko/20100101 Firefox/5.0"
   ],
   "war":{},
   "whitelist":{}
}

LIFF_AUTH = f"line://app/{CHANNEL_ID['LIFF_SERVICE']}"
CARRIER     = '51089, 1-0'
DEVICE_NAME = 'iPhone OS'
IP_ADDR     = '8.8.8.8'
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
VERSION = '©Finpoll 3.0.1'