# -*- coding: UTF-8 -*-
"""
©
"""

from .tools import Zalgo, Split

from datetime import datetime
from typing import Union, List, Dict, Any, Optional
from copy import deepcopy

import base64, urllib, urllib.parse, tempfile, shutil, json, humanize, threading, traceback, os, re, rsa, time, pytz, requests, hashlib, ntpath

class Talk(object):

    _messageReq = {}
    _unsendMessageReq = {}
    _msgSeq = 0

    def __init__(self):
        self.isLoggin = True

    def kickoutFromGroup(self, groupId, midlist):
        return self.talk.kickoutFromGroup(0, groupId, midlist)

    def leaveGroup(self, groupId):
        return self.talk.leaveGroup(0, groupId)

    def rejectGroupInvitation(self, groupId):
        return self.talk.rejectGroupInvitation(0, groupId)

    def reissueGroupTicket(self, groupId):
        return self.talk.reissueGroupTicket(groupId)

    def updateGroup(self, groupObject):
        return self.talk.updateGroup(0, groupObject)

    def createRoom(self, midlist):
        return self.talk.createRoom(0, midlist)

    def getRoom(self, roomId):
        return self.talk.getRoom(roomId)

    def inviteIntoRoom(self, roomId, midlist):
        return self.talk.inviteIntoRoom(0, roomId, midlist)

    def leaveRoom(self, roomId):
        return self.talk.leaveRoom(0, roomId)

    def acquireCallTalkRoute(self, to):
        return self.talk.acquireCallRoute(to)

    def reportSpam(self, chatMid, memberMids=[], spammerReasons=[], senderMids=[], spamMessageIds=[], spamMessages=[]):
        return self.talk.reportSpam(chatMid, memberMids, spammerReasons, senderMids, spamMessageIds, spamMessages)

    def reportSpammer(self, spammerMid, spammerReasons=[], spamMessageIds=[]):
        return self.talk.reportSpammer(spammerMid, spammerReasons, spamMessageIds)

    def acquireEncryptedAccessToken(self, featureType=2):
        return self.talk.acquireEncryptedAccessToken(featureType)

    def getProfile(self):
        return self.talk.getProfile()

    def getSettings(self):
        return self.talk.getSettings()

    def getUserTicket(self):
        return self.talk.getUserTicket()

    def generateUserTicket(self):
        try:
            ticket = self.getUserTicket().id
        except:
            self.reissueUserTicket()
            ticket = self.getUserTicket().id
        return ticket

    def updateProfile(self, profileObject=None, type='', name=None, path=None):
        if type=='name' and name !=None:
            return self.talk.updateProfileAttribute(0, 2, str(name))
        elif type =='zname' and name != None:
            zn = Zalgo().Zalgofy(name)
            return self.talk.updateProfileAttribute(0, 2, str(zn))
        elif type == 'picture' and path != None:
            return self.updateProfilePicture(path, type='p')
        elif type == 'bio' and name != None:
            return self.updateProfileStatusMessage(str(name))
        else:
            return self.talk.updateProfile(0, profileObject)

    def updateProfileZalgoName(self, value: str):
        zn = Zalgo().Zalgofy(value)
        return self.updateProfileAttribute(self._func.ProfileAttribute.DISPLAY_NAME, zn)

    def updateProfileDisplayName(self,value: str):
        return self.updateProfileAttribute(self._func.ProfileAttribute.DISPLAY_NAME, value)

    def updateProfileStatusMessage(self, value: str):
        return self.updateProfileAttribute(self._func.ProfileAttribute.STATUS_MESSAGE, value)

    def updateSettings(self, settingObject):
        return self.talk.updateSettings(0, settingObject)

    def updateProfileAttribute(self, attrId, value):
        return self.talk.updateProfileAttribute(0, attrId, value)

    def updateContactSetting(self, mid, flag, value):
        return self.talk.updateContactSetting(0, mid, flag, value)

    def deleteContact(self, mid):
        return self.updateContactSetting(mid, 16, 'True')

    def renameContact(self, mid, name):
        return self.updateContactSetting(mid, 2, name)

    def addToFavoriteContactMids(self, mid):
        return self.updateContactSetting(mid, 8, 'True')

    def addToHiddenContactMids(self, mid):
        return self.updateContactSetting(mid, 4, 'True')

    def generateReplyMessage(self, relatedMessageId):
        msg = self._func.Message()
        msg.relatedMessageServiceCode = 1
        msg.messageRelationType = 3
        msg.relatedMessageId = str(relatedMessageId)
        return msg

    def sendReplyMessage(self, relatedMessageId, to, text, contentMetadata={}, contentType=0):
        msg = self._func.Message(
           to = to,
           text = text,
           contentType = contentType,
           contentMetadata = {'LINE_RECV':'1'},
           relatedMessageId = relatedMessageId,
           messageRelationType = 3,
           relatedMessageServiceCode = 1
        )
        return self.talk.sendMessage(msg)

    def sMessage(self, to, text, contentMetadata={}, contentType=0, relatedMessageId=None):
        msg = self._func.Message(
           to = to,
           text = text,
           contentType = contentType,
           contentMetadata = {'LINE_RECV':'1'},
           relatedMessageId = relatedMessageId,
           messageRelationType = 3,
           relatedMessageServiceCode = 1
        )
        return self.talk.sendMessage(msg)

    def sendMessage(self, to, text, contentMetadata={}, contentType=0):
        msg = self._func.Message()

        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType , msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    def sendMessageAwaitCommit(self, to, text, contentMetadata={}, contentType=0):
        msg = self._func.Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessageAwaitCommit(self._messageReq[to], msg)

    def sendText(self, ToMid, text):
        msg = self._func.Message()
        msg.to= ToMid
        msg.text = str(text)
        msg.contentType = 0
        msg.contentMetadata = {}
        return self.talk.sendMessage(0, msg)

    def sendMessageObject(self, msg):
        to = msg.to
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    def sendMentions(self, to, mid, firstmessage='', lastmessage=''):
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@Alfinonh044 "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        self.sendMessage(to, text, contentMetadata={'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, contentType=0)

    def sendMention(self, to, text="",ps='', mids=[], contentType=0):
        arrData = ""
        arr = []
        mention ="@Alfinonh044 "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ''
            h = ''
            for mid in range(len(mids)):
                h+= str(texts[mid].encode('unicode-escape'))
                textx += str(texts[mid])
                if h != textx:slen = len(textx)+h.count('U0');elen = len(textx)+h.count('U0') + 13
                else:slen = len(textx);elen = len(textx) + 13
                arrData = {'S':str(slen), 'E':str(elen), 'M':mids[mid]}
                arr.append(arrData)
                textx += mention
            textx += str(texts[len(mids)])
        else:
            textx = ''
            slen = len(textx)
            elen = len(textx) + 18
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
            arr.append(arrData)
            textx += mention + str(text)
        return self.sendMessage(to, textx, contentMetadata={'AGENT_LINK': 'line://ti/p/~alfinonh0404','AGENT_ICON': "https://i.imgur.com/hT4U9vs.png",'AGENT_NAME': ps,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, contentType=contentType)

    def sendContact(self, to, mid):
        return self.sendMessage(to, None, contentMetadata={"mid": mid}, contentType=13)

    def sendImage(self, to, path):
        message_id = self.sendMessage(to,'',contentMetadata={}, contentType=1)
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': str(message_id.id),
            'size': len(open(path, 'rb').read()),
            'type': 'image',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.postContent('https://obs-sg.line-apps.com/talk/m/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload image failure.')
        return True

    def sendImageWithURL(self, to, url):
        path = 'pythonLine.data' 
        r = self.getContent(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            raise Exception('Download image failure.')

        try:
            self.sendImage(to, path)
            if os.path.exists(path):
                os.remove(path)
                return True
            else:
                return False
        except Exception as e:
            raise e

    def sendVideo(self, to, path):
        message_id = self.sendMessage(to,"",contentMetadata = {'VIDLEN': '60000','DURATION': '60000'}, contentType=2)
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': message_id.id,
            'size': len(open(path, 'rb').read()),
            'type': 'video',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.postContent('https://obs-sg.line-apps.com/talk/m/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    def sendVideoWithURL(self, to, url):
        path = 'pythonLine.data' 
        r = self.getContent(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            raise Exception('Download video failure.')

        try:
            self.sendVideo(to, path)
            if os.path.exists(path):
                os.remove(path)
                return True
            else:
                return False
        except Exception as e:
            raise e

    def sendAudio(self, to, path):
        message_id = self.sendMessage(to,'',contentMetadata={}, contentType = 3)
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': str(message_id.id),
            'size': len(open(path, 'rb').read()),
            'type': 'audio',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.postContent('https://obs-sg.line-apps.com/talk/m/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    def sendAudioWithURL(self, to, url):
        path = 'pythonLine.data' 
        r = self.getContent(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            raise Exception('Download audio failure.')
        try:
            self.sendAudio(to, path)
            if os.path.exists(path):
                os.remove(path)
                return True
            else:
                return False
        except Exception as e:
            raise e

    def sendFile(self, to: str, path, file_name=''):
        if file_name == '':
            file_name = ntpath.basename(path)

        mdata = {'FILE_NAME': str(file_name),'FILE_SIZE': str(len(open(path, 'rb').read()))}
        message_id = self.sendMessage(to,'', contentMetadata=mdata, contentType = 14)
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': str(message_id.id),
            'size': len(open(path, 'rb').read()),
            'type': 'file',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.postContent('https://obs-sg.line-apps.com/talk/m/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    def sendFileWithURL(self, to, url, fileName=''):
        if fileName == '':
            fileName = 'finbot_data.bin'
        r = self.getContent(url, headers=self.headers, stream=True)
        if r.status_code != 404:
            with open(fileName, 'wb') as f:
                path = shutil.copyfileobj(r.raw, f)
        self.sendFile(to, path, fileName)
        if os.path.exists(fileName):
            os.remove(fileName)

    def remoteMention(self, to: str, text: str, mids: Union[List[str]], version: bool = None):
        if version == None:
            version = "©Linepoll-Client 2021"

        if self.profile.mid in mids:mids.remove(self.profile.mid)
        parsed_len = len(mids)//20+1
        result = '╭•「 %s 」\n'%text
        mention = '@Alfinonh044\n'
        no = 0
        for point in range(parsed_len):
            mentionees = []
            for mid in mids[point*20:(point+1)*20]:
                no += 1
                result += '│ %i. %s' % (no, mention)
                slen = len(result) - 12
                elen = len(result) + 3
                mentionees.append({'S': str(slen), 'E': str(elen - 4), 'M': mid})
                if mid == mids[-1]:
                    result += '╰•「 %s 」\n'%version
            if result:
                if result.endswith('\n'): result = result[:-1]
                self.talk.sendMessage(self._func.Message(to=to, text=result, contentMetadata={'MENTION': json.dumps({'MENTIONEES': mentionees})}, contentType=0))
            result = ''

    def unsendMessage(self, messageId):
        return self.talk.unsendMessage(0, messageId)
        
    def getRecentMessagesV2(self, messageBoxId, messagesCount=1001):
        return self.talk.getRecentMessagesV2(messageBoxId, messagesCount)

    def requestResendMessage(self, senderMid, messageId):
        return self.talk.requestResendMessage(0, senderMid, messageId)

    def respondResendMessage(self, receiverMid, originalMessageId, resendMessage, errorCode):
        return self.talk.respondResendMessage(0, receiverMid, originalMessageId, resendMessage, errorCode)

    def removeMessage(self, messageId):
        return self.talk.removeMessage(messageId)
    
    def removeAllMessages(self, lastMessageId):
        return self.talk.removeAllMessages(0, lastMessageId)

    def removeMessageFromMyHome(self, messageId):
        return self.talk.removeMessageFromMyHome(messageId)

    def destroyMessage(self, chatId, messageId):
        return self.talk.destroyMessage(0, chatId, messageId, sessionId)
    
    def sendChatChecked(self, consumer, messageId):
        return self.talk.sendChatChecked(0, consumer, messageId)

    def sendEvent(self, messageObject):
        return self.talk.sendEvent(0, messageObject)

    def getLastReadMessageIds(self, chatId):
        return self.talk.getLastReadMessageIds(0, chatId)

    def getPreviousMessagesV2WithReadCount(self, messageBoxId, endMessageId, messagesCount=50):
        return self.talk.getPreviousMessagesV2WithReadCount(messageBoxId, endMessageId, messagesCount)

    def blockContact(self, mid):
        return self.talk.blockContact(0, mid)

    def unblockContact(self, mid):
        return self.talk.unblockContact(0, mid)

    def findAndAddContactByMetaTag(self, userid, reference):
        return self.talk.findAndAddContactByMetaTag(0, userid, reference)

    def findAndAddContactsByMid(self, mid):
        if mid in self.friends or mid == self.profile.mid:
            return
        else:
            try:
                self.talk.findAndAddContactsByMid(0, mid, 0, '')
                time.sleep(2)
            except:
                pass

    def findAndAddContactsByEmail(self, emails=[]):
        return self.talk.findAndAddContactsByEmail(0, emails)

    def findAndAddContactsByUserid(self, userid):
        return self.talk.findAndAddContactsByUserid(0, userid)

    def findContactsByUserid(self, userid):
        return self.talk.findContactByUserid(userid)

    def findContactByTicket(self, ticketId):
        return self.talk.findContactByUserTicket(ticketId)

    def getAllContactIds(self):
        return self.talk.getAllContactIds()

    def getBlockedContactIds(self):
        return self.talk.getBlockedContactIds()

    def getContact(self, mid):
        return self.talk.getContact(mid)

    def getContacts(self, midlist):
        return self.talk.getContacts(midlist)

    def getFavoriteMids(self):
        return self.talk.getFavoriteMids()

    def getHiddenContactMids(self):
        return self.talk.getHiddenContactMids()

    def tryFriendRequest(self, midOrEMid, friendRequestParams, method=1):
        return self.talk.tryFriendRequest(midOrEMid, method, friendRequestParams)

    def makeUserAddMyselfAsContact(self, contactOwnerMid):
        return self.talk.makeUserAddMyselfAsContact(contactOwnerMid)

    def getContactWithFriendRequestStatus(self, id):
        return self.talk.getContactWithFriendRequestStatus(id)

    def reissueUserTicket(self, expirationTime=100, maxUseCount=100):
        return self.talk.reissueUserTicket(expirationTime, maxUseCount)

    def getChatRoomAnnouncementsBulk(self, chatRoomMids):
        return self.talk.getChatRoomAnnouncementsBulk(chatRoomMids)

    def getChatRoomAnnouncements(self, chatRoomMid):
        return self.talk.getChatRoomAnnouncements(chatRoomMid)

    def createChatRoomAnnouncement(self, chatRoomMid, type, contents):
        return self.talk.createChatRoomAnnouncement(0, chatRoomMid, type, contents)

    def removeChatRoomAnnouncement(self, chatRoomMid, announcementSeq):
        return self.talk.removeChatRoomAnnouncement(0, chatRoomMid, announcementSeq)

    def getGroupWithoutMembers(self, groupId):
        return self.talk.getGroupWithoutMembers(groupId)
    
    def findGroupByTicket(self, ticketId):
        return self.talk.findGroupByTicket(ticketId)

    def acceptGroupInvitation(self, groupId):
        return self.talk.acceptGroupInvitation(0, groupId)

    def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self.talk.acceptGroupInvitationByTicket(0, groupId, ticketId)

    def joinByTicket(self, groupId, bool = False):
        G = self.getGroupWithoutMembers(groupId)
        G.preventedJoinByTicket = bool
        self.updateGroup(G)
        if bool == False:
            return self.reissueGroupTicket(G.id)

    def cancelGroupInvitation(self, groupId, contactIds):
        return self.talk.cancelGroupInvitation(0, groupId, contactIds)

    def cancel(self, gid, uid):
        return self.talk.cancelGroupInvitation(0, gid, [uid])

    def createGroup(self, name, midlist):
        return self.talk.createGroup(0, name, midlist)

    def getGroup(self, groupId):
        return self.talk.getGroup(groupId)

    def getGroups(self, groupIds):
        return self.talk.getGroups(groupIds)

    def getGroupsV2(self, groupIds):
        return self.talk.getGroupsV2(groupIds)

    def getCompactGroup(self, groupId):
        return self.talk.getCompactGroup(groupId)

    def getCompactRoom(self, roomId):
        return self.talk.getCompactRoom(roomId)

    def getGroupIdsByName(self, groupName):
        gIds = []
        for gId in self.getGroupIdsJoined():
            g = self.getCompactGroup(gId)
            if groupName in g.name:
                gIds.append(gId)
        return gIds

    def getGroupIdsInvited(self):
        return self.talk.getGroupIdsInvited()

    def getGroupIdsJoined(self):
        return self.talk.getGroupIdsJoined()

    def updateGroupPreferenceAttribute(self, groupMid, updatedAttrs):
        return self.talk.updateGroupPreferenceAttribute(0, groupMid, updatedAttrs)

    def inviteIntoGroup(self, groupId, midlist):
        return self.talk.inviteIntoGroup(0, groupId, midlist)