# -*- coding: UTF-8 -*-
"""
simple Linepoll
©ALFINONH
"""
import typing
import line
from line.utility.filter import Filters
from random import choice, randint
from pathlib import Path
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import os.path, time, json, concurrent.futures, requests, subprocess, threading, traceback, urllib.parse, random

_file_name_ = os.path.splitext(os.path.basename(__file__))[0]
starting_timer = time.time()


"""
ex:
client = line.LineClient(email='YOUR_EMAIL',password='YOUR_PASS',apps='IOSIPAD')

client = line.LineClient(authToken='YOUR_TOKEN', apps='SEE AT CONFIG')
"""
client = line.LineClient(authKey='LINE_AUTHKEY',apps="IOS")
client_mid = client.profile.mid
responsename = f'{_file_name_}-{client.profile.displayName}'
LinePoller = line.Poll(client, threaded=True)

if Path('%s-%s.json'%(_file_name_,client_mid)).exists():
    db = line.Database('%s-%s.json'%(_file_name_,client_mid), True, True, 4)
else:
    db = line.Database('%s-%s.json'%(_file_name_,client_mid), True, True, 4)
    db.update(line.LINE_ENPOINT.DATA)

msg_dict = {}
owner = db['owner']
admin = db['admin']
def parse_tl(msg):
    pUrl = msg.replace('https://line.me/R/home/post?','').split('&')
    actorId = pUrl[0].replace('userMid=','') if not 'userMid=' in pUrl[0] else pUrl[0].replace('homeId=','')
    print(str(actorId))
    return actorId

def line_notify(text: str, to: typing.Union[str]=None) -> line.LineNotify:
    if(to == None): to = client.server.LINE_NOTIFY_PATH
    pesan_text = f"file ›› {_file_name_}\n{text}"
    return line.LineNotify(to).send(pesan_text)

def speed_timing(gid: typing.Optional[str]) -> line.Message:
    j = 0
    for i in range(3):
        start = time.time()
        client.sendMessage(gid,"Send message")
        stop = time.time()
        client.sendMessage(gid,str(stop-start))
        j += stop-start
    else:
        client.sendMessage(gid,"Average time: " + str(j / 3))

def command(text: str):
    pesan = text.lower()
    if db["prefix"]["status"]:
        if pesan.startswith(db["prefix"]["key"]):
            cmd = pesan.replace(db["prefix"]["key"],"")
        else:
            cmd = ""
    else:
        cmd = pesan
    return cmd

def remove_command(text: str, key: str=None):
    if key == '':
        mykey = '' if not db['prefix']['status'] else db['prefix']['key']
    else:
        mykey = key
    text_ = text[len(mykey):]
    sep = text_.split(' ')
    return text_[len(sep[0] + ' '):]

def parser(res):
    result = ''
    textt = res.split('\n')
    for text in textt:
        if True not in [text.startswith(s) for s in ['╭', '├', '│', '╰']]:
            result += '\n│ ' + text
        else:
            if text == textt[0]:
                result += text
            else:
                result += '\n' + text
    return result

@LinePoller.handler(line.OpType.SEND_MESSAGE, Filters.text & Filters.group)
def send_message(op: line.Operation):
    msg = op.message
    cmd_prefix = command(msg.text)
    for cmd_prefix in cmd_prefix.split(' & '):
        if cmd_prefix == 'like on':
            if db['autoLike']['status'] == True:
                client.sendMessage(msg.to, 'Auto like already setted')
            else:
                client.sendMessage(msg.to, 'Auto like enabled')
                db['autoLike']['status'] = True
        if cmd_prefix == 'like off':
            if db['autoLike']['status'] == False:
                client.sendMessage(msg.to, 'Auto like already disabled')
            else:
                client.sendMessage(msg.to, 'Auto like disabled')
                db['autoLike']['status'] = False
        if msg.text.startswith('~/ex'):
            ewe = msg.text[5:]
            try:
                exec(ewe)
            except:
                line_notify(traceback.format_exc())

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.text & Filters.group)
def public_conversation(op: line.Operation):
    msg = op.message
    text = msg.text.lower()
    sender = msg._from
    receiver = msg.to
    to = receiver if msg.toType == line.MIDType.GROUP else msg._from
    if(msg.to in db["unsendMessage"] and sender not in owner):
        if msg.location != None:
            msg_dict[msg.id] = {
                "location": msg.location,
                "from": sender,
                "waktu": time.time()
            }
        else:
            msg_dict[msg.id] = {
                "text": msg.text,
                "from": sender,
                "waktu": time.time()
            }
    if not(receiver in db['mute']):
        if(text in ['hi','hello','hai']):
            client.sendReplyMessage(msg.id, to, choice(['Hi juga','Hi too','Hello','Hi how are you..!','Yes hi too.., Do i know you..?']))
        if(text in ['.me','!me','#me','|me','/me','me']):
            client.sendReplyMessage(msg.id, to, choice(['cin','mek','ayam..?','kir..?','teet...?']))
        if(text in ['.mid','!mid','#mid','|mid','/mid','mid']):
            client.sendReplyMessage(msg.id, to, msg._from)

    #if sender own
    if(text in ["respon",'test','coba'] and sender in owner):
        client.sendReplyMessage(msg.id, to, str(responsename))
    elif(text == "mute:on" and sender in owner):
        if(receiver in db['mute']):
            client.sendReplyMessage(msg.id, to, "Group conversation has been activated")
        else:
            client.sendReplyMessage(msg.id, to, "Group conversation enabled")
            db['mute'][receiver] = True
    elif(text == "mute:off" and sender in owner):
        if(receiver in db['mute']):
            client.sendReplyMessage(msg.id, to, "Group conversation disabled")
            del db['mute'][receiver]
        else:
            client.sendReplyMessage(msg.id, to, "No group conversations are enabled")

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.image & Filters.group)
def receive_image(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if(msg.to in db["unsendMessage"] and msg._from not in owner):
        if 'DOWNLOAD_URL' in msg.contentMetadata:
            path = msg.contentMetadata['DOWNLOAD_URL']
        else:
            path = client.downloadObjectMsg(msg.id)
        msg_dict[msg.id] = {
            "from": msg._from,
            "image": path,
            "waktu": time.time()
        }

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.video & Filters.group)
def receive_video(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if(msg.to in db["unsendMessage"] and msg._from not in owner):
        if 'DOWNLOAD_URL' in msg.contentMetadata:
            path = msg.contentMetadata['DOWNLOAD_URL']
        else:
            path = client.downloadObjectMsg(msg.id)
        msg_dict[msg.id] = {
            "from": msg._from,
            "video": path,
            "waktu": time.time()
        }

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.audio & Filters.group)
def receive_audio(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if(msg.to in db["unsendMessage"] and msg._from not in owner):
        if 'DOWNLOAD_URL' in msg.contentMetadata:
            path = msg.contentMetadata['DOWNLOAD_URL']
        else:
            path = client.downloadObjectMsg(msg.id)
        msg_dict[msg.id] = {
            "from": msg._from,
            "audio": path,
            "waktu": time.time()
        }

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE,Filters.html & Filters.group)
def receive_html(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if msg.contentType == line.ContentType.HTML:
        print(msg.contentMetadata)

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.pdf & Filters.group)
def receive_pdf(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if msg.contentType == line.ContentType.PDF:
        print('PDF',msg.contentMetadata)

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.call & Filters.group)
def receive_call(op: line.Operation):
    """
    {'GC_EVT_TYPE': 'S', 'GC_CHAT_MID': 'ca567277b6710d3334c6d5757b6f6a3db', 'CAUSE': '16', 'GC_MEDIA_TYPE': 'AUDIO', 'VERSION': 'X', 'GC_PROTO': 'C', 'TYPE': 'G', 'GC_IGNORE_ON_FAILBACK': 'false', 'RESULT': 'INFO', 'DURATION': '0', 'SKIP_BADGE_COUNT': 'false'}
    {'GC_EVT_TYPE': 'E', 'GC_CHAT_MID': 'ca567277b6710d3334c6d5757b6f6a3db', 'CAUSE': '16', 'GC_MEDIA_TYPE': 'AUDIO', 'VERSION': 'X', 'GC_PROTO': 'C', 'TYPE': 'G', 'GC_IGNORE_ON_FAILBACK': 'true', 'RESULT': 'INFO', 'DURATION': '88657', 'SKIP_BADGE_COUNT': 'true'}
    """
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if(msg.contentMetadata['GC_EVT_TYPE'] == 'S'):
        client.sendText(to,'Maaf sedang sibuk..!')
        if(msg.contentMetadata['GC_MEDIA_TYPE'] == 'AUDIO'):
            client.inviteGroupCall(to, 1, 1)
        else:
            client.inviteGroupCall(to, 1, 2)

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE,Filters.sticker & Filters.group)
def receive_sticker(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if(msg.to in db["unsendMessage"] and sender not in owner):
        msg_dict[msg.id] = {
            "from":msg._from,
            "sticker":"https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/android/sticker.png".format(msg.contentMetadata["STKID"]),
            "waktu":time.time()
        }

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE,Filters.gift & Filters.group)
def receive_gift(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if msg.contentType == line.ContentType.GIFT:
        print('GIFT',msg.contentMetadata)

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.contact & Filters.group)
def receive_contact(op: line.Operation):
    try:
        msg = op.message
        if(msg.to in db["unsendMessage"] and msg._from not in owner):
            msg_dict[msg.id] = {
                "from":msg._from,
                "mid":msg.contentMetadata["mid"],
                "waktu":time.time()
            }
    except:
        line_notify(str(traceback.format_exc()))

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.location & Filters.group)
def receive_location(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if msg.location != None:                           
        setview = msg.location.latitude
        setview2 = msg.location.longitude
        s1 = "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=0&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))
        s2 = "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=90&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))
        s3 = "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=180&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))
        s4 = "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=270&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))
        s5 = "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=370&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))                           
        color = choice(["#0000FF","#FF0000","#FFFFFF","#00FFFF","#00FF00"])
        data = {
            "type":"carousel",
            "contents":[
                {"type":"bubble","size":"micro","body":{"type":"box","layout":"vertical","contents":[{"type":"image","url":s1,"size":"full","aspectMode":"cover","aspectRatio":"3:5","gravity":"center"},{"type":"text","text":"Google Maps","position":"absolute","size":"xs","color":color,"offsetStart":"5px"}],"paddingAll":"0px"},"action":{"type":"uri","label":"action","uri":s1}},
                {"type":"bubble","size":"micro","body":{"type":"box","layout":"vertical","contents":[{"type":"image","url":s2,"size":"full","aspectMode":"cover","aspectRatio":"3:5","gravity":"center"},{"type":"text","text":"Google Maps","position":"absolute","size":"xs","color":color,"offsetStart":"5px"}],"paddingAll":"0px"},"action":{"type":"uri","label":"action","uri":s2}},
                {"type":"bubble","size":"micro","body":{"type":"box","layout":"vertical","contents":[{"type":"image","url":s3,"size":"full","aspectMode":"cover","aspectRatio":"3:5","gravity":"center"},{"type":"text","text":"Google Maps","position":"absolute","size":"xs","color":color,"offsetStart":"5px"}],"paddingAll":"0px"},"action":{"type":"uri","label":"action","uri":s3}},
                {"type":"bubble","size":"micro","body":{"type":"box","layout":"vertical","contents":[{"type":"image","url":s4,"size":"full","aspectMode":"cover","aspectRatio":"3:5","gravity":"center"},{"type":"text","text":"Google Maps","position":"absolute","size":"xs","color":color,"offsetStart":"5px"}],"paddingAll":"0px"},"action":{"type":"uri","label":"action","uri":s4}},
                {"type":"bubble","size":"micro","body":{"type":"box","layout":"vertical","contents":[{"type":"image","url":s5,"size":"full","aspectMode":"cover","aspectRatio":"3:5","gravity":"center"},{"type":"text","text":"Google Maps","position":"absolute","size":"xs","color":color,"offsetStart":"5px"}],"paddingAll":"0px"},"action":{"type":"uri","label":"action","uri":s5}}
            ]
        }
        datas = {
            "messages": [
            {
                "type": "flex",
                "altText": "Google Maps",
                "contents": data
                }
            ]
        }
        client.sendCarousel(to,datas)

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE,Filters.post & Filters.group)
def receive_post(op: line.Operation):
    try:
        msg = op.message
        to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
        actorId = parse_tl(msg.contentMetadata["postEndUrl"])
        if db['autoLike']['status'] == True:
            likeType = random.choice([1001,1002,1003,1004,1005,1006])
            postId = msg.contentMetadata["postEndUrl"].replace('https://line.me/R/home/post?','').split('&')[1].replace('postId=','')
            if postId not in db['postId']:
                headers = {
                    "Content-Type" : "application/json",
                    "X-Line-Application": "DESKTOPMAC\t5.1.2\tMAC\t10.9.4-MAVERICKS-x64",
                    "User-Agent": "DESKTOP:MAC:10.9.4-MAVERICKS-x64(5.1.2)",
                    "X-Line-Mid" : client_mid,
                    "x-lct" : client.channel_access_token
                }
                params = urllib.parse.urlencode({'homeId': actorId,'sourceType': 'TIMELINE'})
                to_like = {
                    'likeType': likeType,
                    'activityExternalId': postId,
                    'actorId': actorId
               }
                to_comment = {
                    'commentText': str(db['autoLike']['comment']),
                    'activityExternalId': postId,
                    'actorId': actorId
                }
                requests.Session().post('https://gd2.line.naver.jp/mh/api/v39/like/create.json?' + params, headers=headers, data=json.dumps(to_like))
                client.eventTrue(db, to,'›››› ᴘᴏsᴛ ʟɪᴋᴇᴅ')
                requests.Session().post('https://gd2.line.naver.jp/mh/api/v39/comment/create.json?'+ params, headers=headers, data=json.dumps(to_comment))
                db['postId'].append(postId)
            else:
                client.eventTrue(db, to,'›››› ᴘᴏsᴛ ᴄᴏᴍᴍᴇɴᴛᴇᴅ')
    except:
        line_notify(traceback.format_exc())

@LinePoller.handler(line.OpType.RECEIVE_MESSAGE, Filters.flex & Filters.group)
def receive_flex(op: line.Operation):
    msg = op.message
    to = msg.to if msg.toType == line.MIDType.GROUP else msg._from
    if msg.contentType == line.ContentType.FLEX:
        print('FLEX',msg.contentMetadata)

@LinePoller.handler(line.OpType.NOTIFIED_INVITE_INTO_GROUP)
def notified_invite_into_group(op: line.Operation):
    if op.param3 == client_mid:
        if db['autoJoin']['status']:
            client.acceptGroupInvitation(op.param1)
        if db['autoJoin']['reply']:
            client.sendMention(op.param1, str(db['autoJoin']['message']), '', [op.param2]) if '@!' not in db['autoJoin']['message'] else client.sendMessage(op.param1,str(db['autoJoin']['message']))
    if op.param3 in db['blacklist'] and op.param2 not in(owner or admin):
        inv   = op.param3.replace('\x1e',',')
        invs = inv.split(',')
        for _mid in invs:
            client.cancelGroupInvitation(op.param1,[_mid])
        client.kickoutFromGroup(op.param1,[op.param2])
        db['blacklist'][op.param2] = True
    if op.param1 in db['protectinvite'] and op.param2 not in(owner or admin):
        inv   = op.param3.replace('\x1e',',')
        invs = inv.split(',')
        for _mid in invs:
            client.cancelGroupInvitation(op.param1,[_mid])
        client.kickoutFromGroup(op.param1,[op.param2])
        db['blacklist'][op.param2] = True

@LinePoller.handler(line.OpType.NOTIFIED_ACCEPT_GROUP_INVITATION)
def notified_accept_group_invitation(op: line.Operation):
    if op.param2 in db["blacklist"] and op.param2 not in(owner or admin):
        if(client.limiter == False):
            client.kickoutFromGroup(op.param1,[op.param2])

    if op.param1 in db["protectjoin"]:
        if op.param2 not in(owner or admin):
            client.kickoutFromGroup(op.param1,[op.param2])
            db["blacklist"][op.param2] = True
    if db['param']['join']['status']:
        if '@!' not in db['param']['join']['message']:client.sendText(op.param1, db['param']['join']['message'].format(name=client.getGroupWithoutMembers(op.param1).name))
        else:client.sendMessageMention(op.param1, db['param']['join']['message'].format(name=client.getGroupWithoutMembers(op.param1).name), "",[op.param2])

@LinePoller.handler(line.OpType.NOTIFIED_KICKOUT_FROM_GROUP)
def notified_kickout_from_group(op: line.Operation):
    if op.param1 in db["protectkick"]:
        if op.param2 not in(owner or admin):
            if(client.limiter== False):
                client.kickoutFromGroup(op.param1,[op.param2])
                db["blacklist"][op.param2] = True

        if op.param3 in(owner or admin):
            if(op.param3 in client.friends and client.limiter != True):
                client.inviteIntoGroup(op.param1,[op.param3])
                client.kickoutFromGroup(op.param1,[op.param2])
            else:
                client.findAndAddContactsByMid(op.param3)
                client.inviteIntoGroup(op.param1,[op.param3])
                client.kickoutFromGroup(op.param1,[op.param2])

@LinePoller.handler(line.OpType.NOTIFIED_ADD_CONTACT)
def notified_add_contact(op: line.Operation):
    if db['autoAdd']['status']:
        if not(op.param1 in client.friends):
            client.findAndAddContactsByMid(op.param1)
        else:
            pass
    if db['autoAdd']['reply']:
        if op.param1 in(owner or admin):
            client.line['message'].sendMessage(
                line.Message(to=op.param1,text='Thanks for add me boss..!')
            )
        else:
            with open('add.txt','r') as f:
                client.line['message'].sendMessage(
                    line.Message(to=op.param1,text=str(f.read()))
                )

LinePoller.start()
