# -*- coding: UTF-8 -*-
"""
    ~~~~~~~~~~~
    Simple linebot
    created by: 
    ©finbot alfino~nh
    ~~~~~~~~~~~
"""
from typing import (
    Dict,
    Optional,
    Union,
    Any,
    List,
    Awaitable
)

from .lib.curve import ttypes as operationTypes
from .lib.curve.ttypes import *

from .utility.LineLiff import LINELiff, LiffApp
from .utility.media import LineNotify, Split, Zalgo
from .utility import config as LINE_ENDPOINT

from datetime import datetime
from bs4 import BeautifulSoup
from googletrans import Translator
from time import sleep
from random import choice
from copy import deepcopy
import pafy, requests, json, shutil, os, humanize, sys, pytz, ntpath, urllib.parse

max_rev: Optional[int] = 50
class LineTalk(object):

    def __init__(self):
        self.isLogin

    def google_trans(self, say, lang):
        translator = Translator()
        hasil = translator.translate(say, dest=lang)
        A = hasil.text
        return A

    def translators(self, to, text, settings):
        if(to in settings['translate']):
            translator = Translator()
            language = "{}".format(str(settings['translate'][to]))
            hasil = translator.translate(text, dest=language)
            A = hasil.text
            return str(A)

        else:
            return text

    def searchLinkYoutube(self,to,link):
        v = pafy.new(link)
        stream = v.streams
        for vi in stream:
            vide = vi.url
        return self.sendVideoWithURL(to,vide)

    def requestweb(self,url):
        r = requests.get(url)
        data = json.loads( r.text)
        return data

    def  bitly(self, longurl):
        r = requests.get("https://api-ssl.bitly.com/v3/shorten?access_token=c52a3ad85f0eeafbb55e680d0fb926a5c4cab823&longUrl="+longurl) #856d9935ce3a691d5d1671a29421824d8fffccb3
        if r.status_code != 200:
            raise 'error'
        result = json.loads(r.text)
        for data in result['data']:
            return data['url']

    def getProfile(self) -> Profile:
        return self.line['talk'].getProfile()

    def getSettings(self) -> Settings:
        return self.line['talk'].getSettings()

    def reissueUserTicket(self, expirationTime: int =100, maxUseCount: int =100) -> str:
        return self.line['talk'].reissueUserTicket(expirationTime, maxUseCount)

    def getUserTicket(self) -> Union[str, Ticket]:
        return self.line['talk'].getUserTicket()

    def generateUserTicket(self) -> str:
        try:
            ticket = self.getUserTicket().id
        except:
            self.reissueUserTicket()
            ticket = self.getUserTicket().id
        return ticket

    """Contact User"""

    def updateProfileAttribute(self, attrId: ProfileAttribute, value: str) -> bool:
        return bool(self.line['talk'].updateProfileAttribute(attrId, value))

    def updateProfile(self, profileObject=None, type='', name=None, path=None) -> bool:
        if type=='name' and name !=None:
            self.updateProfileDisplayName(str(name))
        elif type =='zname' and name != None:
            self.updateProfileZalgoName(str(name))
        elif type == 'picture' and path != None:
            self.updateProfilePicture(path, type='p')
        elif type == 'bio' and name != None:
            self.updateProfileStatusMessage(str(name))
        else:
            return bool(self.line['talk'].updateProfile(profileObject))

    def updateProfileZalgoName(self, value: str) -> ProfileAttribute:
        zn = Zalgo().Zalgofy(value)
        return self.line['talk'].updateProfileAttribute(ProfileAttribute.DISPLAY_NAME, zn)

    def updateProfileDisplayName(self,value: str) -> ProfileAttribute:
        return self.line['talk'].updateProfileAttribute(ProfileAttribute.DISPLAY_NAME, value)

    def updateProfileStatusMessage(self, value: str) -> ProfileAttribute:
        return self.line['talk'].updateProfileAttribute(ProfileAttribute.STATUS_MESSAGE, value)

    def updateProfilePicture(self, path, type='p'):
        assert type in ['p', 'vp'], "Invalid type value %s"%type
        files = {'file': open(path, 'rb')}
        params = {
            'oid': self.profile.mid,
            'type': 'image',
            'name': 'alfino-nh.bin',
            'ver': '1.0'
        }
        if type == 'vp':
            params.update({'ver': '2.0', 'cat': 'vp.mp4'})

        data = {'params': json.dumps(params)}
        r = self._session.post(self.server.OBS_SG_HOST+'/talk/p/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update profile picture failure.')
        return True

    def changeVideoPictureProfile(self, pict, vids):
        try:
            files = {
                'file': open("{}.mp4".format(vids), 'rb')
            }
            obs_params = {
                'name': 'media',
                'oid': self.profile.mid,
                'size': len(open("{}.mp4".format(vids),'rb').read()),
                'type': 'video',
                'cat': 'vp.mp4',
                'ver': '1.0'
            }
            datas = {
                'params': json.dumps(obs_params)
            }
            r_vp = self._session.post('https://obs-sg.line-apps.com/talk/vp/upload.nhn',headers = deepcopy(self.headers), data=datas, files=files)
            if r_vp.status_code != 201:
                raise Exception("Update vide profile Failed")
            self.updateProfilePicture(pict, 'vp')
        except Exception:
            print("< Update profile video failed>")

    def cloneContactProfile(self, to: str) -> Contact:
        try:
            contact = self.line['talk'].getContact(to)
            profile = self.profile
            profile_to_up = self.downloadFileURL(self.server.PROFILE_DL_PATH + contact.pictureStatus)
            profile.pictureStatus = profile_to_up
            profile.displayName = contact.displayName
            if self.getProfileCoverId(to) != None:
                objId = self.getProfileCoverId(to)
                self.updateProfileCoverById(objId)

            self.updateProfilePicture(profile.pictureStatus)
            return self.line['talk'].updateProfile(profile)
            if contact.videoProfile != None:
                path2 = self.server.PROFILE_DL_PATH + profile.pictureStatus
                self.updateProfilePicture(path2, 'vp')

            self.deleteFile(profile_to_up)
        except Exception:
            self.logError("Clone fail %s"%to)

    def updateSettings(self, settingObject):
        return self.line['talk'].updateSettings(settingObject)

    def updateContactSetting(self, mid: str, flag: int, value: str):
        return self.line['talk'].updateContactSetting(mid, flag, value)

    def renameContact(self, mid: str, name: str):
        return bool(self.line['talk'].updateContactSetting(mid, ContactSetting.CONTACT_SETTING_DISPLAY_NAME_OVERRIDE, name))

    def addToFavoriteContactMids(self,mid: str):
        return bool(self.line['talk'].updateContactSetting(mid, ContactSetting.CONTACT_SETTING_FAVORITE, 'True'))

    def addToHiddenContactMids(self, mid: str):
        return bool(self.line['talk'].updateContactSetting(mid, ContactSetting.CONTACT_SETTING_CONTACT_HIDE, 'True'))

    def disableNotifContact(self, mid: str):
        return bool(self.line['talk'].updateContactSetting(mid, ContactSetting.CONTACT_SETTING_NOTIFICATION_DISABLE, "True"))

    """Contact"""

    def blockContact(self, mids: Union[str, list, tuple]) -> bool:
        if isinstance(mids, str):
            return bool(self.line['talk'].blockContact(mids))

        elif isinstance(mids, (list, tuple)):
            for mid in mids:
                return bool(self.line['talk'].blockContact(mid))

    def unblockContact(self, mids: Union[str, list, tuple]) -> bool:
        if isinstance(mids, str):
            return bool(self.line['talk'].unblockContact(mids))

        elif isinstance(mids, (list, tuple)):
            for mid in mids:
                return bool(self.line['talk'].unblockContact(mid))

    def findAndAddContactsByMid(self,mid: str) -> bool:
        if mid not in self.friends:
            try:
                self.line['talk'].findAndAddContactsByMid(mid)
                self.friends.append(mid)
                return True
            except Exception: return False
        else:
            return

    def findContactsByUserid(self, userid: str) -> bool:
        return bool(self.line['talk'].findContactByUserid(userid))

    def findContactByTicket(self,ticketId: str) -> Contact:
        return self.line['talk'].findContactByUserTicket(ticketId)

    def getAllContactIds(self) -> list:
        return self.line['talk'].getAllContactIds()

    def getBlockedContactIds(self) -> list:
        return self.line['talk'].getBlockedContactIds()

    def getContact(self, mid):
        return self.line['talk'].getContact(mid)

    def getContacts(self, mids: Union[str, list, tuple]) -> Union[Contact, list]:
        mids = mids if isinstance(mids, (list, tuple)) else [mids]
        if len(mids) <= 1:
            return self.line['talk'].getContact(mids[0])
        else:
            return self.line['talk'].getContacts(mids)

    def getFavoriteMids(self) -> list:
        return self.line['talk'].getFavoriteMids()

    def getHiddenContactMids(self) -> list:
        return self.line['talk'].getHiddenContactMids()

    def deleteContact(self, contact) -> bool:
        return bool(self.line['talk'].updateContactSetting(contact, ContactSetting.CONTACT_SETTING_DELETE,'True'))

    def clearContacts(self):
        tt = self.line['talk'].getAllContactIds()
        t = self.getContacts(tt)
        for n in t:
            try:
                self.self.line['talk'].updateContactSetting(n.mid, ContactSetting.CONTACT_SETTING_DELETE,'True')
            except:
                pass
        pass

    def clearfriend(self, to: str):
        n = len(self.line['talk'].getAllContactIds())
        try:
            self.clearContacts()
        except: 
            pass
        t = len(self.line['talk'].getAllContactIds())
        for i in self.friends:
            self.friends.remove(i)
            self.friends = t
        return self.sendMessage(to,"Before: %s\nAfter:%s\nRemoved:%s"%(n,t,(n-t)))

    def refreshContacts(self):
        contact_ids = self.line['talk'].getAllContactIds()
        contacts    = self.getContacts(contact_ids)
        contacts = [contact.displayName+',./;'+contact.mid for contact in contacts]
        contacts.sort()
        contacts = [a.split(',./;')[1] for a in contacts]
        return contacts

    """ GROUP """
    def refreshGroups(self):
        group_ids = self.line['talk'].getGroupIdsJoined()
        groups    = self.getGroups(group_ids)

        groups = [gc.name+',./;'+gc.id for gc in groups]
        groups.sort()
        groups = [a.split(',./;')[1] for a in groups]
        return groups

    def refreshGroupInvited(self):
        group_ids = self.line['talk'].getGroupIdsInvited()
        groups    = self.getGroups(group_ids)

        groups = [gc.name+',./;'+gc.id for gc in groups]
        groups.sort()
        groups = [a.split(',./;')[1] for a in groups]
        return groups

    def getGroupWithoutMembers(self, groupId: str) -> Group:
        return self.line['talk'].getGroupWithoutMembers(groupId)

    def findGroupByTicket(self, ticketId):
        return self.line['talk'].findGroupByTicket(ticketId)

    def preventedTicket(self, groupId, bool = False):
        G = self.line['talk'].getGroupWithoutMembers(groupId)
        G.preventedJoinByTicket = bool
        self.line['talk'].updateGroup(G)
        if bool == False:
            return self.line['talk'].reissueGroupTicket(G.id)

    def receivePreventedTicket(self, g, t):
        if(g != self.groups):
            self.acceptGroupInvitationByTicket(g, t)
            return True
        else:
            return False

    def acceptGroupInvitation(self, groupId: str) -> bool:
        if groupId not in self.groups:
            self.groups.append(groupId)

        return self.line['talk'].acceptGroupInvitation(groupId)

    def acceptGroupInvitationByTicket(self,groupId: str, ticketId: str) -> bool:
        if groupId not in self.groups:
            self.groups.append(groupId)

        return self.line['talk'].acceptGroupInvitationByTicket(groupId, ticketId)

    def cancelGroupInvitation(self, group_id: str, mid_users: Union[str, list]) -> bool:
        mids = mid_users if isinstance(mid_users, list) else [mid_users]
        if(group_id in self.groups):
            if len(mids) > 1:
                for mid in mids:
                    try:
                        self.line['talk'].cancelGroupInvitation(group_id, [mid])
                        return True
                    except: return False
            else:
                try:
                    self.line['talk'].cancelGroupInvitation(group_id, mids)
                    return True
                except: return False
        else: return "<Not in group>"

    def createGroup(self, name: str, midlist: list) -> bool:
        return bool(self.line['talk'].createGroup(name, midlist))

    def getGroup(self, groupId: str):
        return self.line['talk'].getGroup(groupId)

    def getGroups(self, groupIds: Union[str, list]) -> Union[list, Group]:
        ids = groupIds if isinstance(groupIds, list) else [groupIds]
        if len(ids) <= 1:
            return self.getGroup(ids[0])

        else:
            return self.line['talk'].getGroups(ids)

    def getGroupsV2(self, groupIds: Union[list, str]) -> Group:
        return self.line['talk'].getGroupsV2(groupIds)

    def getCompactGroup(self, groupId: str) -> Group:
        return self.line['talk'].getCompactGroup(groupId)

    def getGroupIdsByName(self, groupName: str) -> str:
        gIds = []
        for gId in self.line['talk'].getGroupIdsJoined():
            g = self.line['talk'].getGroupWithoutMembers(gId)
            if groupName in g.name:
                gIds.append(gId)

        return gIds

    def getGroupIdsInvited(self) -> list:
        return self.line['talk'].getGroupIdsInvited()

    def getGroupIdsJoined(self) -> list:
        return self.line['talk'].getGroupIdsJoined()

    def updateGroupPreferenceAttribute(self, groupMid:str, updatedAttrs: dict) -> bool:
        return bool(self.line['talk'].updateGroupPreferenceAttribute(groupMid, updatedAttrs))

    def joinKickInviteGroup(self, group_id: str, mid_users, mids_users, ticket_id = None):
        if ticket_id:
            self.acceptGroupInvitationByTicket(group_id, ticket_id)

        elif group_id in self.ginvitee:
            self.acceptGroupInvitation(group_id)

        if self.limiter == False:
            try:
                self.kickoutFromGroup(group_id, [mid_users])
                self.inviteIntoGroup(group_id, [mids_users])
            except:
                self.limiter = True
            self.limiter = False

    def joinKickoutGroup(self, group_id: str, mid_users: Union[str, list], ticket_id = None):
        mids = mid_users if isinstance(mid_users, list) else mid_users
        if len(mids) > 1:
            for mid in mids:
                try:
                    if(group_id in self.groups):
                        self.kickoutFromGroup(group_id, [mid])
                    else:
                        if ticket_id:
                            self.acceptGroupInvitationByTicket(group_id, ticket_id)
                            sleep(0.08)
                            self.kickoutFromGroup(group_id, [mid])
                            self.leaveGroup(group_id)
                        elif group_id in self.ginvitee:
                            self.acceptGroupInvitation(group_id)
                            self.kickoutFromGroup(group_id, [mid])
                            self.leaveGroup(group_id)
                except:
                    self.limiter = True
                finally:
                    break
                self.limiter = False
        else:
            try:
                if(group_id in self.groups):
                    self.kickoutFromGroup(group_id, mids)
                else:
                    if ticket_id:
                        self.acceptGroupInvitationByTicket(group_id, ticket_id)
                        self.kickoutFromGroup(group_id, mids)
                        self.leaveGroup(group_id)
                    elif group_id in self.ginvitee:
                        self.acceptGroupInvitation(group_id)
                        self.kickoutFromGroup(group_id, mids)
                        self.leaveGroup(group_id)
            except:
                self.limiter = True
            self.limiter = False

    def inviteIntoGroup(self, group_id: str, mid_users: Union[str,list]) -> bool:
        mids = mid_users if isinstance(mid_users, list) else [mid_users]
        if(group_id in self.groups and self.limiter == False):
            if len(mids) > 1:
                for mid in mids:
                    try:
                        self.line['talk'].inviteIntoGroup(group_id, [mid])
                    except:
                        self.limiter = True
                    finally:
                        break
                    self.limiter = False
            else:
                try:
                    return self.line['talk'].inviteIntoGroup(group_id, mids)
                except:
                    self.limiter = True
                self.limiter = False
        else: return "<Execute invite users failed i'm not in group>"

    def kickoutFromGroup(self, group_id: str, mid_users: Union[str, list]) -> bool:
        mids = mid_users if isinstance(mid_users, list) else mid_users
        if(group_id in self.groups and self.limiter == False):
            if len(mids) > 1:
                for mid in mids:
                    try:
                        self.line['talk'].kickoutFromGroup(group_id, [mid])
                    except:
                        self.limiter = True
                    finally:
                        break
                    self.limiter = False
            else:
                try:
                    self.line['talk'].kickoutFromGroup(group_id, mids)
                except:
                    self.limiter = True
                self.limiter = False
        else: return "<Execute kick users failed i'm not in group>"

    def leaveGroup(self, groupId: str) -> bool:
        if(groupId in self.groups):
            leave = bool(self.line['talk'].leaveGroup(groupId))
            self.groups.remove(groupId)
            return leave
        else: return False

    def rejectGroupInvitation(self, groupId: str) -> bool:
        if(groupId in self.ginvitee):
            reject = bool(self.line['talk'].rejectGroupInvitation(groupId))
            self.ginvitee.remove(groupId)
            return reject
        else: return False

    def reissueGroupTicket(self, groupId: str) -> str:
        return self.line['talk'].reissueGroupTicket(groupId)

    def updateGroup(self, groupObject: Union[Group]) -> bool:
        return bool(self.line['talk'].updateGroup(groupObject))

    """Room"""

    def createRoom( self, midlist: Union[str,list]):
        return self.line['talk'].createRoom(midlist)

    def getRoom( self, roomId: str):
        return self.line['talk'].getRoom(roomId)

    def getCompactRoom(self, roomId: str):
        return self.line['talk'].getCompactRoom(roomId)

    def inviteIntoRoom(self, roomId: str, midlist: Union[str,list]):
        return self.line['talk'].inviteIntoRoom(roomId, midlist)

    def leaveRoom(self, roomId: str):
        return self.line['talk'].leaveRoom(roomId)

    def getChatRoomAnnouncementsBulk(self, chatRoomMids):
        return self.line['talk'].getChatRoomAnnouncementsBulk(chatRoomMids)

    def getChatRoomAnnouncements(self, chatRoomMid):
        return self.line['talk'].getChatRoomAnnouncements(chatRoomMid)

    def createChatRoomAnnouncement(self, chatRoomMid, type, contents):
        return self.line['talk'].createChatRoomAnnouncement(chatRoomMid, type, contents)

    def removeChatRoomAnnouncement(self, chatRoomMid, announcementSeq):
        return self.line['talk'].removeChatRoomAnnouncement(chatRoomMid, announcementSeq)

    def sendChatChecked(self, consumer, messageId):
        return self.line['talk'].sendChatChecked(consumer, messageId)

    def inviteIntoChat(self, gid: str, mid: Union[str,list]):
        mids = mid if isinstance(mid, list) else [mid]
        req = InviteIntoChatRequest()
        req.reqSeq=0
        req.chatMid=gid
        req.targetUserMids=mids
        try:
            return self.line['talk'].inviteIntoChat(req)
            sleep(0.08)
        except:
            return False
            self.limiter = True

    def acceptChatInvitation(self, gid):
        req = AcceptChatInvitationRequest()
        req.reqSeq=0
        req.chatMid=gid

        return self.line['talk'].acceptChatInvitation(req)

    def rejectChatInvitation(self, gid):
        req = RejectChatInvitationRequest()
        req.reqSeq=0
        req.chatMid=gid
        return self.line['talk'].rejectChatInvitation(req)

    def deleteOtherFromChat(self, gid: str, mid: Union[str,list]):
        mids = mid if isinstance(mid, list) else [mid]
        req = DeleteOtherFromChatRequest()
        req.reqSeq=0
        req.chatMid=gid
        req.targetUserMids=mids
        try:
            return self.line['talk'].deleteOtherFromChat(req)
            sleep(0.08)
        except:
            return False
            self.limiter = True

    def kick(self, gid, uid):
        mids = uid if isinstance(uid, list) else uid
        if(gid in self.groups and self.limiter == False):
            if len(mids) > 1:
                for mid in mids:
                    try:
                        self.line['talk'].kickoutFromGroup(gid,[uid])
                    except Exception as e:
                        if "code=10" in str(e):
                            print(self.profile.mid,'kick failed ',gid)
                        elif "code=35" in str(e):
                            self.limiter = True
                        return
                    self.limiter = False
            else:
                try:
                    self.line['talk'].kickoutFromGroup(gid, mids)
                except Exception as e:
                    if "code=10" in str(e):
                        print(self.profile.mid,'kick failed ',gid)
                    elif "code=35" in str(e):
                        self.limiter = True
                    return
                self.limiter = False

    def invite(self, gid, uid):
        try:
            self.inviteIntoGroup(gid, [uid])
        except Exception as e:
            if "code=10" in str(e):
                print(self.profile.mid,'invite failed ',gid)
            elif "code=35" in str(e):
                self.limiter = True
            G = self.getGroupWithoutMembers(gid)
            if G.preventedJoinByTicket == True:
                G.preventedJoinByTicket = False
            self.updateGroup(G)
            icket = self.reissueGroupTicket(gid)
            self.sendText(uid,".join {} {}".format(gid,icket))
            return
        self.limiter = False

    def delete_other_from_chat(self, to, ktarget = [], ctarget = []):
        if(to in self.groups and self.limiter == False):
            cmd = 'node expansion.js token={} gid={}'.format(self.token, to)
            for uid in ktarget:
                cmd += ' uid={}'.format(uid)
            for cud in ctarget:
                cmd += ' cud={}'.format(cud)
            os.system(cmd)

    def cancelChatInvitation(self, gid: str, mid: Union[str,list]):
        mids = mid if isinstance(mid, list) else [mid]
        req = CancelChatInvitationRequest()
        req.reqSeq=0
        req.chatMid=gid
        req.targetUserMids=mids
        return self.line['talk'].cancelChatInvitation(req)

    def sendEchoPush(self,text):
        return self.line['talk'].sendEchoPush(text)

    def removeAnnouncement(self, to: str):
        a = self.getChatRoomAnnouncements(to)
        c = a[0].announcementSeq
        return self.line['talk'].removeChatRoomAnnouncement(to, c)

    def createAnnouncement(self, to: str, text: str, msgid: str):
        c = ChatRoomAnnouncementContents()
        c.displayFields = 5
        c.text = text
        c.link = "line://nv/chatMsg?chatId={}&messageId={}".format(to,msgid)
        return self.line['talk'].createChatRoomAnnouncement(to, 0, c)

    """Message"""
    def sendMessageRelations(self, to: str, text: str, contentMetadata: Union[dict] = None, contentType: int = 0, msgid = None) -> Union[str, Message]:
        msg = self._message()
        if('MENTION' in contentMetadata.keys() != None):
            try:
                msg.relatedMessageId = str(self.line['talk'].getRecentMessagesV2(to, 10)[0].id)
                msg.relatedMessageServiceCode = 1
                msg.messageRelationType = 3
            except:
                pass
        if msgid != None:
            msg.relatedMessageId = str(msgid)
            msg.relatedMessageServiceCode = 1
            msg.messageRelationType = 3
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        return self.line['message'].sendMessage(msg)

    def sendMessages(self, msgObj):
        return self.line['message'].sendMessage(msgObj)

    def sendMessage(self, to: str, text: str, contentMetadata: Union[dict] = None, contentType: int = 0) -> Union[str, Message]:
        msg = Message(
            to=to,
            text = text,
            contentType =  contentType,
            contentMetadata = {'LINE_RECV':'1'}
            if contentMetadata is None \
            else contentMetadata
        )
        return self.line['message'].sendMessage(msg)

    def sendText(self, to: str, text: str):
        msg = Message(to=to, text = text)
        return self.line['message'].sendMessage(msg)

    def sendBroadcast(self, to: str, text: str, bc=2):
        if(bc==2):
            target = self.line['talk'].getGroupIdsJoined()
        else:
            target = self.line['talk'].getAllContactIds()
        num= 0
        for fr in target:
            try:
                self.line['message'].sendMessage(self._message(to=fr, text="{}".format(str(text))))
                num+=1
                sleep(0.3)
            except:
                pass
        return self.line['message'].sendMessage(self._message(to=to,text="Success broadcast {} friends".format(num)))

    def giftmessage(self,to):
        a = ["5","7","6","8"]
        b = choice(a)
        return self.line['message'].sendMessage(self._message(to=to,text=None, contentType=9,contentMetadata={'PRDTYPE': 'STICKER','STKVER': '1','MSGTPL': b,'STKPKGID': '1380280'}))

    def templatefoot(self,link,AI,AN):
        a={'AGENT_LINK': link,
        'AGENT_ICON': AI,
        'AGENT_NAME': AN}
        return a

    def archi(self, wait, sd, dd, ss, split, msg, tex, nama=[]):
        selection = Split(split,range(1,len(nama)+1))
        k = len(nama)//100
        for a in range(k+1):
            if a == 0:
                eto='╭「 '+sd+' 」─'+tex
            else:
                eto='├「 '+sd+' 」─'+tex
            text = ''
            mids = []
            no = a
            for i in selection.parse()[a*100 : (a+1)*100]:
                mids.append(nama[i-1])
                if dd == 'kick':
                    self.kickoutFromGroup(ss,[nama[i-1]])
                    hh = ''
                if dd == 'delfriend':
                    try:
                        self.deleteContact(nama[i-1])
                        hh = 'Del Friend'
                    except:
                        hh = 'Not Friend User'
                if dd == 'delbl':
                    try:
                        wait['blacklist'].remove(nama[i-1])
                        hh = 'Del BL'
                    except:
                        hh = 'Not BL User'
                if dd == 'delwl':
                    try:
                        wait['bots'].remove(nama[i-1])
                        hh = 'Del WL'
                    except:
                        hh = 'Not WL User'
                if dd == 'delml':
                    try:
                        wait['target'].remove(nama[i-1])
                        hh = 'Del ML'
                    except:
                        hh = 'Not ML User'
                if dd == 'delblock':
                    try:
                        self.line['talk'].unblockContact(nama[i-1])
                        hh = 'Del Block'
                    except:
                        hh = 'Not Block User'
                if dd == '':
                    hh = ''
                if dd == 'tag':
                    hh = ''
                no+= 1
                if no == len(selection.parse()):
                    text+= "\n╰{}. @! {}".format(i,hh)
                else:
                    text+= "\n│{}. @! {}".format(i,hh)
            if dd == 'tag':
                self.sendMention(ss,eto+text,sd,mids)
            else:
                self.sendMention(msg.to,eto+text,sd,mids)
        if dd == 'tag':
            self.sendMessage(msg.to,'╭「 Mention 」{}\n╰Status: Success tag {} mem'.format(tex,len(nama)-(len(nama)-len(selection.parse()))))

    def superdata(self, to, wait, text='', text1='', data=[]):
        to = to
        key = wait['prefix']["key"].title()
        if data == []:
            return self.sendMessage(to, "╭───「 {} 」─\n│{}: None\n│    | Command |  \n│Add {}\n│  Key:{} add{} [@|on]\n│Del {}\n│  Key:{} del{} [@|on|>|<|num 1]\n╰──────".format(text,text,text,key,text1,text,key,text1,key,text1))
        self.datamention(to,'{}'.format(text),data)

    def deletefriendnum(self, to, wait, cmd):
        asd = self.refreshContacts()
        selection = Split(self.splittext(cmd,'s'),range(1,len(asd)+1))
        k = len(asd)//20
        d = []
        for c in selection.parse():
            d.append(asd[int(c)-1])
        self.line['message'].sendMessage(self._message(to=to,text='「 Friendlist 」\nWaiting.....'))
        for a in range(k+1):
            if a == 0:self.mentionmention(to=to,wait=wait,text='',dataMid=d[:20],pl=-0,ps='â­ã Friendlist ãâ\nâ Type: Delete Friendlist',pg='DELFL',pt=d)
            else:self.mentionmention(to=to,wait=wait,text='',dataMid=d[a*20 : (a+1)*20],pl=a*20,ps='âã Friendlist ãâ\nâ Type: Delete Friendlist',pg='DELFL',pt=d)

    def getinformation(self, to, mid, data):
        try:
            if mid in data["bots"]:
                a = "Whitelist: ʏᴇs"
            else:
                a = "Whitelist: ɴᴏ"
            if mid in data["blacklist"]:
                b = "Blacklist: ʏᴇs"
            else:
                b = "Blacklist: ɴᴏ"
            h = self.line['talk'].getContact(mid).statusMessage
            if h == '':
                hh = '\n'
            else:
                hh = "Status:\n" + h + "\n\n"
            zxc = "Name: @!\n" + hh + "userid: \n" + mid + "\n"+a+" "+b
            self.sendMention(to, zxc, '',[mid])
            self.line['talk'].sendContact(to,mid)
        except:
            ginfo = self.line['talk'].getCompactGroup(mid)
            try:
                gCreators = ginfo.creator.mid
                gtime = ginfo.createdTime
            except:
                gCreators = ginfo.members[0].mid
                gtime = ginfo.createdTime
            if ginfo.invitee is None:
                sinvitee = "0"
            else:
                sinvitee = str(len(ginfo.invitee))
            if ginfo.preventedJoinByTicket == True:
                u = "No Prevented"
            else:
                u = "line://ti/g/" + self.line['talk'].reissueGroupTicket(mid)
            zxc =   "╭─•"
            zxc += "\n│ ⌬ Gname: {}".format(ginfo.name)
            zxc += "\n├─•"
            zxc += "\n│ ⌬ Gid: {}".format(mid)
            zxc += "\n│ ⌬ Gmem: {}".format(len(ginfo.members))
            zxc += "\n│ ⌬ Ginvite: {}".format(sinvitee)
            zxc += "\n│ ⌬ Gticket: {}".format(u)
            zxc += "\n│ ⌬ Gcreated: {}".format(humanize.naturaltime(datetime.fromtimestamp(gtime/1000)))
            zxc += "\n│ ⌬ Gcreator: @!"
            zxc += "╰───•"
            self.sendMention(to,zxc,'',[gCreators])
            self.sendContact(to,gCreators)

    def sendContact(self, to: str, mid: str):
        msg = self._message(to=to, text='', contentType= ContentType.CONTACT, contentMetadata = {'mid': mid})
        return self.line['message'].sendMessage(msg)

    def sendSticker(self, to, packageId, stickerId):
        msg = self._message(to=to,text='',contentType = ContentType.STICKER, contentMetadata = {'STKVER': '100', 'STKPKGID': packageId,'STKID': stickerId})
        return self.line['message'].sendMessage(msg)

    def sendImage(self, to, path):
        message = Message(to=to, text=None)
        message.contentType = ContentType.IMAGE
        message.contentPreview = None
        message.contentMetadata = None
        message_id = self.line['message'].sendMessage(message).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': message_id,
            'size': len(open(path, 'rb').read()),
            'type': 'image',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self._session.post('https://obs-sg.line-apps.com/talk/m/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload image failure.')
        return True

    def sendImageWithURL(self, to, url):
        path = 'pythonLine.data' 
        r = requests.get(url, stream=True)
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
        message = Message(to=to, text=None)
        message.contentType = ContentType.VIDEO
        message.contentPreview = None
        message.contentMetadata = {'VIDLEN': '60000','DURATION': '60000'}
        message_id = self.line['message'].sendMessage(message).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': message_id,
            'size': len(open(path, 'rb').read()),
            'type': 'video',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self._session.post('https://obs-sg.line-apps.com/talk/m/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    def sendVideoWithURL(self, to, url):
        path = 'pythonLine.data' 
        r = requests.get(url, stream=True)
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
        message = Message(to=to, text=None)
        message.contentType = ContentType.AUDIO
        message.contentPreview = None
        message.contentMetadata = None
        message_id = self.line['message'].sendMessage(message).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': message_id,
            'size': len(open(path, 'rb').read()),
            'type': 'audio',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self._session.post('https://obs-sg.line-apps.com/talk/m/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    def sendAudioWithURL(self, to, url):
        path = 'pythonLine.data' 
        r = requests.get(url, stream=True)
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
        message = Message(to=to, text=None)
        message.contentType = ContentType.FILE
        message.contentPreview = None
        message.contentMetadata = {'FILE_NAME': str(file_name),'FILE_SIZE': str(len(open(path, 'rb').read()))}
        message_id = self.line['message'].sendMessage(message).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': message_id,
            'size': len(open(path, 'rb').read()),
            'type': 'file',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self._session.post('https://obs-sg.line-apps.com/talk/m/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    def sendFileWithURL(self, to, url, fileName=''):
        if fileName == '':
            fileName = 'finbot_data.bin'
        r = requests.get(url, headers=headers, stream=True)
        if r.status_code != 404:
            with open(fileName, 'wb') as f:
                path = shutil.copyfileobj(r.raw, f)
        self.sendFile(to, path, fileName)
        if os.path.exists(fileName):
            os.remove(fileName)

    def sendLocation(self, to, address, latitude, longitude, phone=None, contentMetadata={}):
        locations = Location()
        locations.address = address
        locations.phone = phone
        locations.latitude = float(latitude)
        locations.longitude = float(longitude)
        locations.title = "Location"
        msg = self._message(to=to, text = "Location by Google Map", location = locations, contentMetadata = contentMetadata, contentType = ContentType.LOCATION)
        return self.line['message'].sendMessage(msg)

    def sendMessageCustom(self, to: str, text: str, name: str , icon: str):
        contentMetadata = {'MSG_SENDER_ICON': icon,
            'MSG_SENDER_NAME':  name,
            'text': text
        }
        msg = self._message(to=to, text=text, contentMetadata=contentMetadata)
        return self.line['message'].sendMessage(msg)

    def sendGift(self, to, productId, productType):
        assert productType in ['theme','sticker'], 'Invalid productType value %s'%productType
        cMetadata = {
            'MSGTPL': str(randint(0, 12)),
            'PRDTYPE': productType.upper(),
            'STKPKGID' if productType == 'sticker' else 'PRDID': productId
        }
        msg = self._message(to=to,text='',contentType=ContentType.GIFT,contentMetadata=cMetadata)
        return self.line['message'].sendMessage(msg)

    def generateReplyMessage(self, relatedMessageId):
        msg = self._message()
        msg.relatedMessageServiceCode = 1
        msg.messageRelationType = 3
        msg.relatedMessageId = str(relatedMessageId)
        return msg

    def sendReplyMessage(self, relatedMessageId: str, to: str, text: str, contentMetadata: Optional[Dict[str, str]] = None, contentType: int = ContentType.NONE) -> Union[str, Message]:
        msg = self._message(to = to, text = text, contentType = contentType, contentMetadata = {'LINE_RECV':'1'}, relatedMessageId = relatedMessageId, messageRelationType = 3, relatedMessageServiceCode = 1)
        return self.line['message'].sendMessage(msg)

    def sendMessageMention(self, to, text="",ps='', mids=[]):
        arrData = ""
        arr = []
        mention = "@KhieMention "
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
        results = self._message(to=to, text=textx, contentType=ContentType.NONE, contentMetadata={'AGENT_LINK': 'line://ti/p/~alfinonh0404','AGENT_ICON': "https://i.imgur.com/hT4U9vs.png",'AGENT_NAME': ps,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')})
        return self.line['message'].sendMessage(results)

    def sendMentionFooter(self, to, mid, firstmessage, lastmessage):
        try:
            arrData = ""
            text = "%s " %(str(firstmessage))
            arr = []
            mention = "@LopeAgri"
            slen = str(len(text))
            elen = str(len(text) + len(mention))
            arrData = {'S':slen, 'E':elen, 'M':mid}
            arr.append(arrData)
            text += mention + str(lastmessage)
            msg = Message()
            msg.to = to
            msg.text = text
            msg.contentMetadata = {
                'AGENT_LINK': "https://line.me/ti/p/~alfinonh0404",
                'AGENT_ICON': 'https://i.imgur.com/hT4U9vs.png',
                'AGENT_NAME': "Finbot",
                'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')
            }
            msg.contentType = ContentType.NONE
            self.line['message'].sendMessage(msg)
        except TalkException as x:
            print(str(x))

    def sendMention(self,to, text="",ps='', mids=[]):
        arrData = ""
        arr = []
        mention = "@KhieMention "
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
        self.line['message'].sendMessage(Message(to=to, text=textx,contentMetadata={'AGENT_LINK': 'line://ti/p/~kangnur04','AGENT_ICON': "https://i.imgur.com/hT4U9vs.png",'AGENT_NAME': ps,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}))

    def sendMentionV2(self, to: str, text: str, mids: Union[List[str]], isUnicode: bool = False):
        arrData = ""
        arr = []
        mention = "@zeroxyuuki "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ""
            unicode = ""
            if isUnicode:
                for mid in mids:
                    unicode += str(texts[mids.index(mid)].encode('unicode-escape'))
                    textx += str(texts[mids.index(mid)])
                    slen = len(textx) if unicode == textx else len(textx) + unicode.count('U0')
                    elen = len(textx) + 15
                    arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                    arr.append(arrData)
                    textx += mention
            else:
                for mid in mids:
                    textx += str(texts[mids.index(mid)])
                    slen = len(textx)
                    elen = len(textx) + 15
                    arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                    arr.append(arrData)
                    textx += mention
            textx += str(texts[len(mids)])
        else:
            raise Exception("Invalid mention position")
        self.line['message'].sendMessage(
            self._message(to=to, text=textx, contentMetadata={'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')})
        )

    def mentions(self,to, text="", mids=[]):
        arrData = ""
        arr = []
        mention = "@KhieGans  "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ""
            for mid in mids:
                textx += str(texts[mids.index(mid)])
                slen = len(textx)
                elen = len(textx) + 15
                arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                arr.append(arrData)
                textx += mention
            textx += str(texts[len(mids)])
        else:
            textx = ""
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
            arr.append(arrData)
            textx += mention + str(text)
        self.line['message'].sendMessage(Message(to=to, text=textx, contentMetadata={'AGENT_NAME':'LINE OFFICIAL', 'AGENT_LINK': 'line://ti/p/~alfinonh0404', 'AGENT_ICON': "https://i.imgur.com/hT4U9vs.png", 'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}))

    def templatefoot(self,link,AI,AN):
        a={'AGENT_LINK': link,
        'AGENT_ICON': AI,
        'AGENT_NAME': AN}
        return a

    def remoteMention(self, to: str, text: str, mids: Union[List[str]], version: bool = None):
        if version == None:
            version = LINE_ENDPOINT.VERSION

        if self.profile.mid in mids:mids.remove(self.profile.mid)
        parsed_len = len(mids)//20+1
        result = '╭•「 %s 」\n'%text
        mention = '@zeroxyuuki\n'
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
                self.sendMessage(to, result, {'MENTION': json.dumps({'MENTIONEES': mentionees})}, 0)
            result = ''

    def datamention(self, to, text, data, ps=''):
        if(data == [] or data == {}):return self.sendMessage(to," Sorry empty list")
        k = len(data)//100
        for aa in range(k+1):
            if aa == 0:dd = '╭「 {} 」─{}'.format(text,ps);no=aa
            else:dd = '├「 {} 」─{}'.format(text,ps);no=aa*100
            msgas = dd
            for i in data[aa*100 : (aa+1)*100]:
                no+=1
                if no == len(data):msgas+='\n╰{}. @!'.format(no)
                else:msgas+='\n│{}. @!'.format(no)
            self.sendMention(to, msgas,' 「 {} 」'.format(text), data[aa*100 : (aa+1)*100])

    def mentiondata(self, to, text, data, date, wait, ps=''):
        if(data == [] or data == {}):return self.sendMessage(to," Sorry empty list")
        k = len(data)//100
        for aa in range(k+1):
            if aa == 0:dd = '╭「 {} 」─{}'.format(text,ps);no=aa
            else:dd = '├「 {} 」─{}'.format(text,ps);no=aa*100
            msgas = dd
            for i in data[aa*100 : (aa+1)*100]:
                no+=1
                if date == 'ADDWL':
                    if i in wait["bots"]:a = 'WL User'
                    else:
                        if i not in wait["blacklist"]:a = 'Add WL';wait["bots"].append(i)
                        else:a = 'BL User'
                if date == 'DELWL':
                    try:wait["bots"].remove(i);a = 'Del WL'
                    except:a = 'Not WL User'
                if date == 'ADDBL':
                    if i in wait["bots"]:a = 'WL User'
                    else:
                        if i not in wait["blacklist"]:a = 'Add BL';wait["blacklist"].append(i)
                        else:a = 'BL User'
                if date == 'DELBL':
                    try:wait["blacklist"].remove(i);a = 'Del BL'
                    except:a = 'Not BL User'
                if date == 'DELFL':
                    try:self.deleteContact(i);a = 'Del Friend'
                    except:a = 'Not Friend User'
                if date == 'ADDML':
                    if i in wait["target"]:a = 'ML User'
                    else:a = 'Add ML';wait["target"].append(i)
                if date == 'DELML':
                    try:wait["target"].remove(i);a = 'Del ML'
                    except:a = 'Not ML User'
                if no == len(data):msgas+='\n╰{}. @!{}'.format(no,a)
                else:msgas+='\n│{}. @!{}'.format(no,a)
            self.sendMention(to, msgas,' 「 {} 」'.format(text), data[aa*100 : (aa+1)*100])

    def waktunjir(self):
        sd = ''
        if datetime.now().hour > 1 and datetime.now().hour <10:sd+= 'Good Morning'
        if datetime.now().hour > 10 and datetime.now().hour <15:sd+= 'Good Afternoon'
        if datetime.now().hour > 15 and datetime.now().hour <18:sd+= 'Good Evening'
        if datetime.now().hour >= 18:sd+= 'Good Night'
        return sd

    def waktu(self,secs):
        mins, secs = divmod(secs,60)
        hours, mins = divmod(mins,60)
        days, hours = divmod(hours, 24)
        return '%02d Hari %02d Jam %02d Menit %02d Detik' % (days, hours, mins, secs)

    def unsend2(self, to, wait):
        try:
            if msg.to not in wait['Unsend']:
                wait['Unsend'][msg.to] = {'B':[]}
            if msg._from not in [self.profile.mid]:
                return
            wait['Unsend'][msg.to]['B'].append(msg.id)
        except:pass

    def mycmd(self, text, settings):
        pesan = text.lower()
        if settings["prefix"]["status"]:
            if pesan.startswith(settings["prefix"]["key"]):
                cmd = pesan.replace(settings["prefix"]["key"],"")
            else:
                cmd = ""
        else:
            cmd = pesan
        return cmd

    def mentionmention(self, to, wait, text, dataMid=[], pl='', ps='', pg='', pt=[]):
        arr = []
        list_text=ps
        i=0
        no=pl
        if pg == 'MENTIONALLUNSED':
            for l in dataMid:
                no+=1
                if no == len(pt):list_text+='\n╰°'+str(no)+'. @[RhyN-'+str(i)+'] '
                else:list_text+='\n│'+str(no)+'. @[RhyN-'+str(i)+'] '
                i=i+1
            text=list_text+text
        if pg == 'SIDERMES':
            for l in dataMid:
                chiya = []
            for rom in wait["lurkt"][to][dataMid[0]].items():
                chiya.append(rom[1])
            for b in chiya:
                a = '{}'.format(humanize.naturaltime(datetime.fromtimestamp(b/1000)))
                no+=1
                if no == len(pt):list_text+='\n│'+str(no)+'. @[RhyN-'+str(i)+']\n╰    「 '+a+" 」"
                else:list_text+='\n│'+str(no)+'. @[RhyN-'+str(i)+']\n│    「 '+a+" 」"
                i=i+1
            text=list_text+text
        if pg == 'DELFL':
            for l in dataMid:
                try:
                    self.deleteContact(l)
                    a = 'Del Friend'
                except:
                    a = 'Not Friend User'
                no+=1
                if no == len(pt):list_text+='\nâ°'+str(no)+'. @[RhyN-'+str(i)+'] '+a
                else:list_text+='\nâ'+str(no)+'. @[RhyN-'+str(i)+'] '+a
                i=i+1
            text=text+list_text
        if pg == 'DELML':
            for l in dataMid:
                if l not in wait["mimic"]["target"]:
                    a = 'Not ML User'
                else:
                    a = 'DEL ML'
                    wait["mimic"]["target"].remove(l)
                no+=1
                if no == len(pt):list_text+='\nâ°'+str(no)+'. @[RhyN-'+str(i)+'] '+a
                else:list_text+='\nâ'+str(no)+'. @[RhyN-'+str(i)+'] '+a
                i=i+1
            text=list_text
        i=0
        for l in dataMid:
            mid=l
            name='@[RhyN-'+str(i)+']'
            ln_text=text.replace('\n',' ')
            if ln_text.find(name):
                line_s=int( ln_text.index(name) )
                line_e=(int(line_s)+int( len(name) ))
            arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
            arr.append(arrData)
            i=i+1
        contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
        if pg == 'MENTIONALLUNSED': self.line['message'].unsendMessage(self.sendMessage(to, text, contentMetadata).id)
        else: self.sendMessage(to, text, contentMetadata)

    def mainsplit(self,text,lp=''):
        separate = text.split(" ")
        if lp == '':
            adalah = text.replace(separate[0]+" ","")
        elif lp == 's':
            adalah = text.replace(separate[0]+" "+separate[1]+" ","")
        else:
            adalah = text.replace(separate[0]+" "+separate[1]+" "+separate[2]+" ","")
        return adalah

    def splittext(self,text,lp=''):
        separate = text.split(" ")
        if lp == '':adalah = text.replace(separate[0]+" ","")
        elif lp == 's':adalah = text.replace(separate[0]+" "+separate[1]+" ","")
        else:adalah = text.replace(separate[0]+" "+separate[1]+" "+separate[2]+" ","")
        return adalah

    def get_strings(self, string, start, end, index = 1):
        try:
            str = string.split(start)
            str = str[index].split(end)
            return str[0]
        except:pass

    """Liff"""
    def setLiffHeaders(self, token):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token),
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; X9009 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36 Line/10.20.1 LIFF",
            "X-Requested-With": "jp.naver.line.android"
        }
        return headers

    def refreshLiffChannelAccessToken(self, id):
        liff_struct = LiffViewRequest(self.server.CHANNEL_ID['LIFF_SERVICE'],LiffContext(chat = LiffChatContext(id)))
        self._liff_channel[id] = self.line['liff'].issueLiffView(liff_struct).accessToken
        return self._liff_channel[id]

    def issueLiffLogin(self, channelId, channelScreet):
        data = {
            "grant_type": "client_credentials",
            "client_id": channelId,
            "client_secret": channelSecret
        }
        req = self._session.post("https://api.line.me/v2/oauth/accessToken", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        result = json.loads(req.text)
        authToken = result["access_token"]
        return authToken

    def createLiffChannelId(self, type, authToken, url):
        data = {
            "view": {
                "type": type,
                "url": url
            }
        }
        req = self._session.post("https://api.line.me/liff/v1/apps", json=data, headers=self.setLiffHeaders(authToken))
        result = json.loads(req.text)
        liffid = result["liffId"]
        return liffid

    def issueLiffChannelToken(self, channelId=None, channelScreet=None):
        if(channelId == None):
            channelId = self.server.CHANNEL_ID['LIFF']

        elif(channelScreet==None):
            channelScreet = self.server.CHANNEL_SCREET['LIFF']

        apps = LINELiff()
        apps.login(channelId,channelScreet)
        print(str(apps))
        return apps

    def listLiffChannel(self, channelId=None, channelScreet=None):
        if(channelId == None):
            channelId = self.server.CHANNEL_ID['LIFF']

        elif(channelScreet==None):
            channelScreet = self.server.CHANNEL_SCREET['LIFF']

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
        response = self._session.post("https://api.line.me/liff/v1/apps", headers=self.setLiffHeaders(authToken), json=data)
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

    def getLiffVerifierPermission(self, channelId: Optional[str] = None):
        if channelId is None:
            channelId = self.server.CHANNEL_ID['LIFF']

        headers = deepcopy(self.headers)
        headers["User-Agent"] ="Mozilla/5.0 (Linux; Android 5.1; X9009 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36"
        headers["Content-Type"] = "application/json"
        headers["X-Requested-With"] = "jp.naver.line.android"
        headers["X-Line-ChannelId"] = channelId
        r = self._session.post('https://access.line.me/dialog/api/permissions', json={'on': ['P','CM'],'off': []}, headers=headers)
        return r

    def post_video(self, id: str, url: str, icon: Optional[str] = None):
        if id in self._liff_channel: token = self._liff_channel[id]
        else:token = self.refreshLiffChannelAccessToken(id)
        if icon== None: icon = self.server.BOT_ICON_PATH
        data = {
            "type": "video",
            "originalContentUrl": url,
            "previewImageUrl": icon
        }
        result = self._session.post('https://api.line.me/message/v3/share', json={"messages":[data]}, headers=self.setLiffHeaders(token))
        if result.status_code != 200:
            raise LiffException("[ Error ] Fail post video")
        return

    def post_audio(self, id: str, url: str):
        if id in self._liff_channel: token = self._liff_channel[id]
        else:token = self.refreshLiffChannelAccessToken(id)
        data = {
            "type": "audio",
            "originalContentUrl": url,
            "duration": 1000
        }
        result = self._session.post('https://api.line.me/message/v3/share', json={"messages":[data]}, headers=self.setLiffHeaders(token))
        if result.status_code != 200:
            raise LiffException("[ Error ] Fail post audio")
        return

    def sendTemplate(self, id: str, m: str):
        try:
            if id in self._liff_channel: token = self._liff_channel[id]
            else:token = self.refreshLiffChannelAccessToken(id)
            self._session.post('https://api.line.me/message/v3/share', headers=self.setLiffHeaders(token), data=json.dumps({"messages":[m]}))
        except LiffException:
            self.line['message'].sendMessage(self._message(to=id, text="LiffId unverified\n Let's try again...!"))
            self.getLiffVerifierPermission()

    def sendFlex(self, id: str, m: str, altText: Optional[str] = "Alfino~NH"):
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
            self._session.post('https://api.line.me/message/v3/share', headers=self.setLiffHeaders(token), data=json.dumps(data))
        except LiffException:
            self.line['message'].sendMessage(self._message(to=id, text="LiffId unverified\n Let's try again...!"))
            self.getLiffVerifierPermission()

    def sendCarousel(self, id: str, d: Union[dict]):
        try:
            if id in self._liff_channel: token = self._liff_channel[id]
            else:token = self.refreshLiffChannelAccessToken(id)
            self._session.post('https://api.line.me/message/v3/share', data=json.dumps(d), headers=self.setLiffHeaders(token))
        except LiffException:
            self.line['message'].sendMessage(self._message(to=id, text="LiffId unverified\n Let's try again...!"))
            self.getLiffVerifierPermission()

    def eventTrue(self, settings, to: str, text: str):
        if(to in settings['template']):
            m = {
                "type":"flex","altText":"Line sendMessage","contents":{"type":"bubble","size":"kilo","body":{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"baseline","contents":[{"type":"icon","url":"https://i.imgur.com/hE7qxyC.png","size":"xxl","offsetStart":"1px","offsetBottom":"25px"}],"width":"30px","height":"25px","backgroundColor":"#00cc00ff","paddingAll":"0px","offsetBottom": "6px"},{"type":"box","layout":"horizontal","contents":[{"type":"separator"},{"type":"text","text":text,"size":"xs","color":"#ffffff","offsetStart":"1px"}],"backgroundColor":"#00cc00ff"}],"height":"18px","paddingAll":"0px","cornerRadius":"5px","backgroundColor":"#00cc00ff"}}
            }
            self.sendTemplate(to, m)
        else:
            self.line['message'].sendMessage(self._message(to=to, text=text))

    def eventFalse(self, settings, to: str, text: str):
        if(to in settings['template']):
            m = {
                "type":"flex","altText":"Line sendMessage","contents":{"type":"bubble","size":"kilo","body":{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"baseline","contents":[{"type":"icon","url":"https://i.imgur.com/UnYhQRU.png","size":"xxl","offsetStart":"1px","offsetBottom":"25px"}],"width":"30px","height":"25px","backgroundColor":"#ff0000","paddingAll":"0px","offsetBottom": "6px"},{"type":"box","layout":"horizontal","contents":[{"type":"separator"},{"type":"text","text":text,"size":"xs","color":"#ffffff","offsetStart":"1px"}],"backgroundColor":"#ff0000"}],"height":"18px","paddingAll":"0px","cornerRadius":"5px","backgroundColor":"#ff0000"}}
            }
            self.sendTemplate(to, m)
        else:
            self.line['message'].sendMessage(self._message(to=to, text=text))

    def cmds(self, to: str, text: str, load: bool = False, label: Optional[str] = None):
        if load == True: limg = 'https://i.imgur.com/DPQvsdx.gif'
        else: limg = self.server.BOT_ICON_PATH
        if label == None: label = "©Alfino~Nh 2016˚"
        data = {
            "type": "text",
            "text": "{}".format(text),
            "sentBy": {
                "label": "%s"%label,
                "iconUrl": '%s'%limg,
                "linkUrl": "line://nv/profilePopup/mid=%s"%self.server.BOT_ID
            }
        }
        return self.sendTemplate(to, data)

    """Line Notify"""
    def logError(self, name, text, url_path = None):
        if(url_path is None):
            url_path = self.server.LINE_NOTIFY_PATH

        pesan_kirim = LineNotify(url_path)
        return pesan_kirim.send('\n=> {}\n->> {}'.format(name,text))

    def notification(self, text, url_path=None, name=None,image_path=None, sticker_id=None, package_id=None):
        """Support for free sticker_id or package_id only / image path only ,not support url image path given"""
        if(url_path == None):
            url_path = self.server.LINE_NOTIFY_PATH

        if(name==None):
            name= '> Line Notify\n'

        pesan_text = f"file > {name}\n\n{text}"
        pesan_kirim = LineNotify(url_path)
        return pesan_kirim.send(pesan_text, image_path=image_path,sticker_id=sticker_id, package_id=package_id)

    """Shop"""
    def getProduct(self, packageID, language, country):
        return self.line['shop'].getProduct(packageID, language, country)

    def getStickerInfo(self, sid):
        data = GetProductRequestStruct()
        data.productType = 1
        data.productId = sid
        data.carrierCode = '51089, 1-0' #"510012"
        data.saveBrowsingHistory = False
        return self.line['shop'].getProductV2(data)

    def sendFreeSticker(self, mid: str, sticker_id: str):
        info = self.getStickerInfo(sticker_id)
        locale = LocaleStruct()
        locale.language = "EN"
        locale.country = "ID"
        price = info.productDetail.price
        data = PurchaseOrderStruct()
        data.shopId = "stickershop"
        data.productId = sticker_id
        data.recipientMid = mid
        data.price = price
        data.enableLinePointAutoExchange= True
        data.locale = locale
        data.presentAttributes = {}
        return self.line['shop'].placePurchaseOrderForFreeProduct(data)

    def sendPaidSticker(self, mid: str, sticker_id: str):
        info = self.getStickerInfo(sticker_id)
        locale = LocaleStruct()
        locale.language = "EN"
        locale.country = "ID"
        price = info.productDetail.price
        data = PurchaseOrderStruct()
        data.shopId = "stickershop"
        data.productId = sticker_id
        data.recipientMid = mid
        data.price = price
        data.enableLinePointAutoExchange= True
        data.locale = locale
        data.presentAttributes = {}
        return self.line['shop'].placePurchaseOrderWithLineCoin(data)

    """ CALL """

    def inviteGroupCall(self, gmid: str, count =3, tipe =1):
        group = self.line['talk'].getGroup(gmid)
        members = [mem.mid for mem in group.members]
        isCall = self.line['call'].getGroupCall(gmid)
        if isCall.online == True:
            for num in range(count):
                self.line['call'].acquireGroupCallRoute(gmid, tipe)
                self.line['call'].inviteIntoGroupCall(gmid, members, tipe)
        else:
            return self.line['message'].sendMessage(self._message(to=gmid,text='Sorry no call group required'))

    def lurking(self, to, wait):
        moneys = {}
        for a in wait["setTime"][to].items():
            moneys[a[1]] = [a[0]] if a[1] is not None else idnya
        sort = sorted(moneys)
        sort = sort[0:]
        k = len(sort)//100
        for a in range(k+1):
            if a == 0:no= a;msgas = '╭「 Lurkers 」'
            else:no = a*100;msgas = '├「 Lurkers 」'
            h = []
            for i in sort[a*100 : (a+1)*100]:
                h.append(moneys[i][0])
                no+=1
                a = '{}'.format(humanize.naturaltime(datetime.fromtimestamp(i/1000)))
                if no == len(sort):msgas+='\n│{}. @!\n╰    「 {} 」'.format(no,a)
                else:msgas+='\n│{}. @!\n│    「 {} 」'.format(no,a)
            self.mentions(to, msgas, h)

    def download_smule(self, to, url_lagu, settings):
        link = f"https://pavillon-presse.de/archiv/smule/?url={url_lagu}"
        urls = requests.get(link).text
        result = self.get_strings(urls,'<a class="ipsButton ipsButton_medium ipsButton_important" href="','" download="')
        hasild = f'{result}' #.replace("%2F","/").replace("%3A",":")
        print('{result} \n')
        hasil = urllib.parse.unquote(hasild.replace("amp;",""))
        print(hasil)
        if('Download Audio' in str(result)):
            if(to in settings['template']):self.post_audio(to,str(hasil))
            else:self.sendAudioWithURL(to,str(hasil))
        else:
            if(to in settings['template']):self.post_video(to,str(hasil))
            else:self.sendVideoWithURL(to,str(hasil))

    def blekedok(self, t: int=None,tt: str=None):
        r = requests.get('https://www.webtoons.com/id/genre')
        soup = BeautifulSoup(r.text,'html5lib')
        data = soup.find_all(class_='card_lst')
        datea = data[t].find_all(class_='info')
        if tt == 'data':
            return datea
        else:
            return data[t].find_all('a')

    def helper_help(self, to: str, settings):
        if settings['prefix']['status'] == True:
            key = settings['prefix']['key']
        else:
            key = ''
        tz = pytz.timezone("Asia/Jakarta")
        timeNow = datetime.now(tz=tz)
        vv    = "╭─「 ʜᴇʟᴘ sᴇʟғʙᴏᴛ 」\n"
        vv += "├──────────\n"
        vv += "│➟ User selfbot\n"
        vv += "├─────────\n"
        vv += "│° Login selfbot\n"
        vv += "│° Logout selfbot\n"
        vv += "├─────────\n"
        vv += "│➟ Owner\n"
        vv += "├─────────\n"
        vv += "│° "+key+"proqr (on/off)\n"
        vv += "│° "+key+"proname (on/off)\n"
        vv += "│° "+key+"proimg (on/off)\n"
        vv += "│° "+key+"mute (on/off)\n"
        vv += "│° "+key+"template (on/off)\n"
        vv += "│° "+key+"token (on/off)\n"
        vv += "│° "+key+"login owner\n"
        vv += "│° "+key+"cname (name)\n"
        vv += "│° "+key+"zname (zalgo name)\n"
        vv += "│° "+key+"random name\n"
        vv += "│° "+key+"cprofile video (link)\n"
        vv += "│° "+key+"cpp\n"
        vv += "│° "+key+"comment post (text)\n"
        vv += "│° setkey (lock keys)\n"
        vv += "│° keyword:(on/off) no space\n"
        vv += "│° resetkey\n"
        vv += "│° "+key+"tag @|value\n"
        vv += "│° "+key+"user\n"
        vv += "│° "+key+"add-user @\n"
        vv += "│° "+key+"del-user (@/list numb user\n"
        vv += "│° "+key+"due-date @\n"
        vv += "│° "+key+"status-msg (text)\n"
        vv += "│° "+key+"respon-lang (language code)\n"
        vv += "│° "+key+"member-picture\n"
        vv += "│° "+key+"renew\n"
        vv += "│° "+key+"@reset\n"
        vv += "│° "+key+"@bye\n"
        vv += "├─────────\n"
        vv += "│➟ Publik\n"
        vv += "├─────────\n"
        vv += "│° Mid\n"
        vv += "│° Ginfo\n"
        vv += "│° Ginfo: gid\n"
        vv += "│° Info\n"
        vv += "│° Primary [AuthKey]\n"
        vv += "│° Token iosipad\n"
        vv += "│° Token chrome\n"
        vv += "│° Token mac\n"
        vv += "│° Token win10\n"
        vv += "│° Token desktopwin\n"
        vv += "│° Token list\n"
        vv += "│° Menu token\n"
        vv += "│° get-smule [smule_id]\n"
        vv += "│° get-mp3 [judul]\n"
        vv += "│° yt [judul]\n"
        vv += "│° .youtube [link]\n"
        vv += "│° youtube mp3 [link]\n"
        vv += "│° youtube mp4 [link]\n"
        vv += "│° Download video timeline\n"
        vv += "├─────────\n"
        vv += "│ ⌬ ᴄʀᴇᴀᴛᴏʀ: @! \n"
        vv += "│ ⌬ ᴅᴀʏ: {}\n".format(datetime.strftime(timeNow,'%Y-%m-%d'))
        vv += "│ ⌬ ᴛɪᴍᴇ: {} ᴡɪʙ\n".format(datetime.strftime(timeNow,'%H:%M:%S'))
        vv += "╰─────────" 
        return self.sendMention(to,str(vv),'',[self.server.BOT_ID])

    def helpmessage(self, to, settings):
        if settings['prefix']['status'] == True:
            key = settings['prefix']['key']
        else:
            key = ''
        tz = pytz.timezone("Asia/Jakarta")
        timeNow = datetime.now(tz=tz)
        helpMessage =   "╭──⟮ ʜᴇʟᴘ ᴍᴇssᴀɢᴇ ⟯" + "\n" + \
                    "│ ⌬ " + key + "ᴍʏsᴇʟғ" + "\n" + \
                    "│ ⌬ " + key + "ɢʀᴏᴜᴘ" + "\n" + \
                    "│ ⌬ " + key + "sᴛᴇᴀʟ" + "\n" + \
                    "│ ⌬ " + key + "ᴍᴇᴅɪᴀ" + "\n" + \
                    "│ ⌬ " + key + "sᴇᴛᴛɪɴɢs" + "\n" + \
                    "│ ⌬ " + key + "sᴘᴇᴄɪᴀʟ" + "\n" + \
                    "│ ⌬ " + key + "ᴛᴏᴋᴇɴ" + "\n" + \
                    "├──⟮ ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅ ⟯" + "\n" + \
                    "│ ⌬ " + key + "ɪɴғᴏ" + "\n" + \
                    "│ ⌬ " + key + "ᴄʀᴇᴀᴛᴏʀ" + "\n" + \
                    "│ ⌬ " + key + "ʀᴜɴᴛɪᴍᴇ" + "\n" + \
                    "│ ⌬ " + key + "sᴘᴇᴇᴅ" + "\n" + \
                    "│ ⌬ " + key + "ʀᴇsᴛᴀʀᴛ" + "\n" + \
                    "│ ⌬ " + key + "ʟᴏɢᴏᴜᴛ" + "\n" + \
                    "├─────────" + "\n" + \
                    "│ ⌬ ᴄʀᴇᴀᴛᴏʀ: @! " + "\n" + \
                    "│ ⌬ ᴅᴀʏ: " + datetime.strftime(timeNow,'%Y-%m-%d') + "\n" + \
                    "│ ⌬ ᴛɪᴍᴇ: " + datetime.strftime(timeNow,'%H:%M:%S') + " WIB" + "\n" + \
                    "╰─────────" 
        return self.sendMention(to,str(helpMessage),'',[self.server.BOT_ID])

    def helpmyself(self, to, settings):
        if settings['prefix']['status'] == True:
            key = settings['prefix']['key']
        else:
            key = ''
        tz = pytz.timezone("Asia/Jakarta")
        timeNow = datetime.now(tz=tz)
        helpMyself =   "╭──⟮ sᴇʟғ ⟯" + "\n" + \
                    "│ ⌬ " + key + "ᴍe" + "\n" + \
                    "│ ⌬ " + key + "ᴍʏᴍɪᴅ" + "\n" + \
                    "│ ⌬ " + key + "ᴍʏɴᴀᴍᴇ" + "\n" + \
                    "│ ⌬ " + key + "ᴍʏʙɪᴏ" + "\n" + \
                    "│ ⌬ " + key + "ᴍɪʏᴘɪᴄᴛᴜʀᴇ" + "\n" + \
                    "│ ⌬ " + key + "ᴍʏᴄᴏᴠᴇʀ" + "\n" + \
                    "│ ⌬ " + key + "ᴍʏᴠɪᴅᴇᴏᴘʀᴏғɪʟᴇ" + "\n" + \
                    "│ ⌬ " + key + "ᴍᴇɴᴛɪᴏɴᴀʟʟ" + "\n" + \
                    "│ ⌬ " + key + "ᴜɴsᴅ {ᴠᴀʟᴜᴇ}" + "\n" + \
                    "│ ⌬ " + key + "ʀᴇsᴛᴀʀᴛ" + "\n" + \
                    "│ ⌬ " + key + "ᴄᴘ-ɴᴀᴍᴇ" + "\n" + \
                    "│ ⌬ " + key + "ᴄᴘ-ʙɪᴏ" + "\n" + \
                    "│ ⌬ " + key + "ᴄᴘ-ᴘʀᴏғɪʟᴇ" + "\n" + \
                    "│ ⌬ " + key + "ᴄᴘ-ᴠɪᴅᴇᴏ {ʟɪɴᴋ ʏᴛᴜʙᴇ}" + "\n" + \
                    "│ ⌬ " + key + "ᴄᴘ-ᴛɪᴋᴛᴏᴋ {ʟɪɴᴋ ᴛɪᴋᴛᴏᴋ}" + "\n" + \
                    "├─────────" + "\n" + \
                    "│ ⌬ ᴄʀᴇᴀᴛᴏʀ: @! " + "\n" + \
                    "│ ⌬ ᴅᴀʏ: " + datetime.strftime(timeNow,'%Y-%m-%d') + "\n" + \
                    "│ ⌬ ᴛɪᴍᴇ: " + datetime.strftime(timeNow,'%H:%M:%S') + " WIB" + "\n" + \
                    "╰─────────" 
        return self.sendMention(to,str(helpMyself),'',[self.server.BOT_ID])

    def helpgroup(self, to, settings):
        if settings['prefix']['status'] == True:
            key = settings['prefix']['key']
        else:
            key = ''
        tz = pytz.timezone("Asia/Jakarta")
        timeNow = datetime.now(tz=tz)
        helpGroup =   "╭─⟮ ʜᴇʟᴘ ʜʀᴏᴜᴘ ⟯" + "\n" + \
                    "│ ⌬ " + key + "ɢɪᴅ" + "\n" + \
                    "│ ⌬ " + key + "ɢʟɪsᴛ" + "\n" + \
                    "│ ⌬ " + key + "ɢɪɴғᴏ" + "\n" + \
                    "│ ⌬ " + key + "ɢɴᴀᴍᴇ" + "\n" + \
                    "│ ⌬ " + key + "ɢᴘɪᴄᴛᴜʀᴇ" + "\n" + \
                    "│ ⌬ " + key + "ɢᴄʀᴇᴀᴛᴏʀ" + "\n" + \
                    "│ ⌬ " + key + "ɢᴛɪᴄᴋᴇᴛ「On/Off」" + "\n" + \
                    "│ ⌬ " + key + "ɢᴍᴇᴍʙᴇʀ ʟɪsᴛ" + "\n" + \
                    "├─────────" + "\n" + \
                    "│ ⌬ ᴄʀᴇᴀᴛᴏʀ: @! " + "\n" + \
                    "│ ⌬ ᴅᴀʏ: " + datetime.strftime(timeNow,'%Y-%m-%d') + "\n" + \
                    "│ ⌬ ᴛɪᴍᴇ: " + datetime.strftime(timeNow,'%H:%M:%S') + " WIB" + "\n" + \
                    "╰─────────" 
        return self.sendMention(to,str(helpGroup),'',[self.server.BOT_ID])
