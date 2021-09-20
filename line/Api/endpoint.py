
class Line_Endpoint:
    #MAC/Windows 6.7.2
    #iPhone 11.4.1
    UA = {
       "ANDROID":"Line/10.18.0",
       "ANDROID_BETA":"LLA/2.11.1 Nexus 5X 10",
       "ANDROID_ALPHA":"androidapp.line/10.18.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
       "BOT":"androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
       "CHROMEOS":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
       "DESKTOPWIN":"Line/6.7.0",
       "DESKTOPMAC":"DESKTOP:MAC:6.5.9-MAVERICKS-x64(5.1.2)",
       "IOS":"Line/11.3.0 iPhone8,1 13.3",
       "IOSIPAD":"Line/11.3.0 iPad4,1 8.0",
       "IPHONE": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari Line/11.3.0",
       "VIRTUAL":"Virtual.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
       "WAP":"WAPapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
       "WEB":"Line/2017.0731.2132 CFNetwork/758.6 Darwin/15.0.0"
    }

    LA = {
        'ANDROID': "ANDROID  10.18.0  Android  OS  6.0",
        'ANDROID_BETA': "ANDROIDLITE  2.11.1  Android  OS  6.0",
        'ANDROID_ALPHA': "ANDROID  10.18.0  Android  OS  6.0",
        'BOT': 'BOT  1.7.2  Linux Kernel  3.14.7',
        'CHROMEOS': "CHROMEOS\t2.3.8\tChrome\tOS\t83.0.4103.97",
        'DESKTOPWIN': 'DESKTOPWIN\t6.7.0\tDESKTOP-ALFINONH\t10.0.0-NT-x64',
        'DESKTOPMAC': "DESKTOPMAC\t6.5.9-MAVERICKS-x64\tMAC\t5.1.2",
        'MAC': 'MAC\t3.4.1\tMacOS\t8',
        'IOS': "IOS\t11.3.0\tiOS\t13.3",
        'IOSIPAD': "IOSIPAD\t11.3.0\tiPad4\t8.0.1",
        "IPHONE": "IOS\t11.3.0\tiPhone_OS\t13.3",
        'VIRTUAL': 'VIRTUAL  10.3.0  LINE_VIRTUAL  7.5.0',
        'WAP': 'WAP  10.3.0  iPhone  OS  1',
        'WEB': 'WEB  10.3.0  iPhone  OS  1'
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
        'LIFF_SERVICE': '1654055086-BoD0ExEX',
        'DEFAULT': '1604066537-dl9GVZzo'
    }

    CHANNEL_SCREET = {
        'LIFF': 'CHANNEL_SCREET',
        'LIFF_V1': 'CHANNEL_SCREET',
        'LIFF_V2': 'CHANNEL_SCREET',
        'XSRF-TOKEN':"wkwk",
        'SESSION1': 'wokwok',
        'SESSION2': 'wikwik'
    }

    headers = {
       "User-Agent": "",
       "X-Line-Application": "",
       "x-lal" : "id-ID",
       "x-lhm": "POST"
    }
    
    data = {
        'image': {},
        'cover': {},
        'postId': {},
        'prefix': {
            'status': False,
            'key': ''
        },
        'autolike':{
            'status': False,
            "comment":'Like by:\nLinepoll-Client'
        },
        'autoadd':{
            'status': False,
            "reply":{
                'status': False,
                'msg': 'Thanks for add me...'
            }
        },
        'autojoin': {
            'status': True,
            'ticket': True,
            'reply':{
                'status': False,
                'msg': 'Thanks for invited me.. @! '
            }
        },
        'unsendmessage': {},
        'lurking': {},
        'rname': '',
        'template': {},
        "mute": {},
        "token": False
        }