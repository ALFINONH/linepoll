# -*- coding: UTF-8 -*-
"""
    ~~~~~~~~~~~
    Simple linebot
    created by: 
    ©finbot alfino~nh
    ~~~~~~~~~~~
"""
from typing import Optional, Dict
from datetime import datetime
from random import randint, choice
from copy import deepcopy
import json, shutil, time, os, base64, tempfile, requests, urllib, urllib.parse, random, time

class LineTimeline(object):

    obs_token: Optional[str] = None
    channel_access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    def __init__(self):
        self.timelineHeaders = {}
        self.profileDetail = self.getProfileDetail()

    def _loginLineTimeline(self):
        channelToken = self.line['channel'].issueChannelToken(self.server.CHANNEL_ID["TIMELINE"])
        self.channel_access_token = channelToken.channelAccessToken
        self.refresh_token = channelToken.refreshToken
        self.obs_token = self.line['talk'].acquireEncryptedAccessToken(2)
        self.setTimelineHeadersWithDict({
            'Content-Type': 'application/json',
            'User-Agent': 'DESKTOPMAC\t5.1.2\tMAC\t10.9.4-MAVERICKS-x64', #self.UA,
            'X-Line-Application': 'DESKTOPMAC\t5.1.2\tMAC\t10.9.4-MAVERICKS-x64', #self.LA,
            'X-Line-Carrier': self.server.CARRIER,
            "X-Line-AcceptLanguage": 'en',
            'X-Line-Mid': self.profile.mid,
            "X-Line-ChannelToken": self.channel_access_token,
            "X-Requested-With": 'jp.naver.line.android.LineApplication'
            })

    def refreshTimelineChannelAccessToken(self):
        self.channel_access_token = self.line['channel'].issueChannelToken(self.server.CHANNEL_ID["TIMELINE"]).channelAccessToken
        self.setTimelineHeaders("X-Line-ChannelToken", self.channel_access_token)

    def setTimelineHeadersWithDict(self, headersDict):
        self.timelineHeaders.update(headersDict)

    def setTimelineHeaders(self, argument, value):
        self.timelineHeaders[argument] = value

    def additionalHeaders(self, source, newSource):
        headerList={}
        headerList.update(source)
        headerList.update(newSource)
        return headerList

    def updateGroupPicture(self, groupId, path):
        files = {
            'file': open(path, 'rb')
        }
        ob_params = {
            'oid': groupId,
            'type': 'image',
            'name': 'alfino-nh.bin',
            'ver': '1.0'
        }
        data = {
            'params': json.dumps(ob_params) #self.genOBSParams({'oid': groupId,'type': 'image'})
        }
        r = self.postContent(self.server.OBS_SG_HOST+'/talk/g/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update group picture failure.')
        return True

    def uploadGroupPicture(self, path, mid):
        file_dir = {
            'file': open(path, 'rb')
        }
        ob_params = {
            'oid': mid,
            'type': 'image',
            'name': 'alfino-nh.bin',
            'ver': '1.0'
        }
        data = {
            'params': json.dumps(ob_params)
        }
        r = self._session.post("https://obs-sg.line-apps.com/talk/g/upload.nhn", headers=deepcopy(self.headers), data= data, files=file_dir, verify=False)
        if r.status_code != 201:
            raise Exception('Update group picture failure.')
        return True

    def getFeed(self, postLimit=10, commentLimit=1, likeLimit=1, order='TIME'):
        params = {
            'postLimit': postLimit,
            'commentLimit': commentLimit,
            'likeLimit': likeLimit,
            'order': order
        }
        url = self.server.TIMELINE_API+ '/v39/feed/list.json?' + urllib.parse.urlencode(params)
        r = self._session.get(url, headers=deepcopy(self.timelineHeaders))
        return r.json()

    def getHomeProfile(self, mid=None, postLimit=10, commentLimit=1, likeLimit=1):
        if mid is None:
            mid = self.profile.mid

        params = {
            'homeId': mid,
            'postLimit': postLimit,
            'commentLimit': commentLimit,
            'likeLimit': likeLimit, 
            'sourceType': 'LINE_PROFILE_COVER'
        }
        url = self.server.TIMELINE_API+'/v39/post/list.json?'+urllib.parse.urlencode(params)
        r = self._session.get(url, headers=deepcopy(self.timelineHeaders))
        return r.json()

    def getProfileDetail(self, mid=None):
        if mid is None:
            mid = self.profile.mid

        params = {
            'userMid': mid
        }
        url = self.server.TIMELINE_API + '/v1/userpopup/getDetail.json?'+urllib.parse.urlencode(params)
        r = self._session.get(url, headers=deepcopy(self.timelineHeaders))
        return r.json()

    def getProfileCoverId(self, mid=None):
        if mid is None:
            mid = self.profile.mid

        home = self.getProfileDetail(mid)
        return home['result']['objectId']

    def getProfileCoverURL(self, mid=None):
        if mid is None:
            mid = self.profile.mid

        home = self.getProfileDetail(mid)
        params = {
            'userid': mid,
            'oid': home['result']['objectId']
        }
        url = self.server.OBS_SG_HOST + '/myhome/c/download.nhn?'+urllib.parse.urlencode(params)
        return url

    def updateProfileCoverById(self, objId):
        params = {
            'coverImageId': objId
        }
        url = self.server.TIMELINE_API + '/v39/home/updateCover.json?' + urllib.parse.urlencode(params)
        r = self._session.get(url, headers=deepcopy(self.timelineHeaders))
        return r.json()

    def updateCover(self, picture):
        objId = self.genObjectId()
        files = open(picture, 'rb').read()
        payload = {
               "name": picture,
               "oid": objId,
               "type": "image",
               "userid": self.profile.mid,
               "ver": "2.0"
        }
        params = {
            "X-Line-PostShare":  "false",
            "X-Line-StoryShare":"false",
            "x-line-signup-region": "ID",
            "content-type": "image/png",
            "x-obs-params": json.dumps(payload)
        }
        headers = self.additionalHeaders(deepcopy(self.timelineHeaders),params)
        result = self._session.post(self.server.OBS_SG_HOST + "/r/myhome/c/" + objId, headers=headers, data=files)
        if result.status_code != 201:
            raise Exception("[ Error ] Fail change cover")
        return

    def updateProfileCover(self, path, returnAs='objId'):
        assert returnAs in ['objId','bool'], 'Invalid returnAs value %s'%(returnAs)
        objId = self.uploadObjHome(path, type='image', returnAs='objId')
        self.updateProfileCoverById(objId)

    def updateProfileCoverVideo(self, path, returnAs='objId'):
        assert returnAs in ['objId','bool'], 'Invalid returnAs value %s'%(returnAs)
        objId = self.uploadObjHome(path, type='video', returnAs='objId')
        home = self.updateProfileCoverById(objId)
        if returnAs == 'objId':
            return objId
        elif returnAs == 'bool':
            return True

    def createPost(self, text, holdingTime=None):
        params = {
               'homeId': self.profile.mid,
               'sourceType': 'TIMELINE'
        }
        url = self.server.TIMELINE_API + '/v39/post/create.json?' + urllib.parse.urlencode(params)
        payload = {
             'postInfo': {
                 'readPermission': {
                     'type': 'ALL'
                 }
             },
             'sourceType': 'TIMELINE',
             'contents': {
                 'text': text
             }
        }
        if holdingTime != None:
            payload["postInfo"]["holdingTime"] = holdingTime

        data = json.dumps(payload)
        r = self._session.post(url, headers=self.timelineHeaders, data=data)
        print(str(r.json()))
        return r.json()

    def sendPostToTalk(self, mid, postId):
        if mid is None:
            mid = self.profile.mid

        params = {
           'receiveMid': mid,
           'postId': postId
        }
        url = self.server.TIMELINE_API + '/v39/post/sendPostToTalk.json?' + urllib.parse.urlencode(params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    def createComment(self, mid, postId, text):
        params = {
            'homeId': mid,
            'sourceType': 'TIMELINE'
        }
        url = self.server.TIMELINE_API + '/v39/comment/create.json?' + urllib.parse.urlencode(params)
        payload = {
            'commentText': text,
            'activityExternalId': postId,
            'actorId': mid
        }
        header = {
            "Content-Type" : "application/json",
            "X-Line-Application": "DESKTOPMAC\t5.1.2\tMAC\t10.9.4-MAVERICKS-x64",
            "User-Agent": "DESKTOP:MAC:10.9.4-MAVERICKS-x64(5.1.2)",
            "X-Line-Mid" : self.profile.mid,
            "x-lct" : self.channel_access_token
        }
        data = json.dumps(payload)
        r = requests.post(url, headers=header, data=data)
        return r.json()

    def deleteComment(self, mid, postId, commentId):
        header = {
            "Content-Type" : "application/json",
            "X-Line-Application": "DESKTOPMAC\t5.1.2\tMAC\t10.9.4-MAVERICKS-x64",
            "User-Agent": "DESKTOP:MAC:10.9.4-MAVERICKS-x64(5.1.2)",
            "X-Line-Mid" : self.profile.mid,
            "x-lct" : self.channel_access_token
        }
        params = {
            'homeId': mid,
            'sourceType': 'TIMELINE'
        }
        payload = {
            'commentId': commentId,
            'activityExternalId': postId,
            'actorId': mid
        }
        url = self.server.TIMELINE_API + '/v39/comment/delete.json?' + urllib.parse.urlencode(params)
        data = json.dumps(payload)
        r = self._session.postContent(url, headers=header, data=data)
        print(str(r.json()))
        print("komen")
        return r.json()

    def likePost(self, mid, postId, likeType=None):
        liking = [1001,1002,1003,1004,1005,1006]
        if likeType == None:
            likeType = random.choice(liking)

        params = {
            'homeId': mid,
            'sourceType': 'TIMELINE'
        }
        url = self.server.TIMELINE_API + '/v39/like/create.json?' + urllib.parse.urlencode(params)
        payload = {
            'likeType': likeType,
            'activityExternalId': postId,
            'actorId': mid
        }
        r = self._session.post(url, headers=self.timelineHeaders, data=json.dumps(payload))
        return r.json()

    def unlikePost(self, mid, postId):
        if mid is None:
            mid = self.profile.mid
        params = {
            'homeId': mid,
            'sourceType': 'TIMELINE'
        }
        url = self.server.TIMELINE_API + '/v39/like/cancel.json?' + urllib.parse.urlencode(params)
        data = json.dumps({'activityExternalId': postId, 'actorId': mid})
        r = self._session.post(url, headers=self.timelineHeaders, data=data)
        return r.json()

    def createPostGroup(self, text,to, holdingTime=None,textMeta=[]):
        params = {
            'homeId': to,
            'sourceType': 'GROUPHOME'
        }
        url = 'https://gd2.line.naver.jp/v39/post/create.json?' + urllib.parse.urlencode(params)
        payload = {
            'postInfo': {
                'readPermission': {
                    'type': 'ALL'
                }
            },
            'sourceType': 'GROUPHOME',
            'contents': {
                'text': text,
                'textMeta':textMeta
            }
        }
        if holdingTime != None:
            payload["postInfo"]["holdingTime"] = holdingTime
        data = json.dumps(payload)
        r = self._session.post(url, headers=self.timelineHeaders, data=data)
        return r.json()

    def createPostGroupR(self, text,to):
        params = {
            'homeId': to,
            'sourceType': 'GROUPHOME'
        }
        url = self.server.TIMELINE_API + '/v39/relay/create.json?'+urllib.parse.urlencode(params)
        payload = {
            'postInfo': {
                'readPermission': {
                    'type': 'ALL'
                }
            },
            'sourceType': 'GROUPHOME',
            'contents': {
                'text': text,
                'textMeta':textMeta
            }
        }
        if holdingTime != None:
            payload["postInfo"]["holdingTime"] = holdingTime
        data = json.dumps(payload)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        return r.json()
    
    def createGroupPost(self, mid, text):
        payload = {
            'postInfo': {
            'readPermission': {
                'homeId': mid
            }
        },
        'sourceType': 'TIMELINE',
        'contents': {
            'text': text
            }
        }
        data = json.dumps(payload)
        r = self.postContent(self.server.TIMELINE_API+'/v39/post/create.json', data=data, headers=self.timelineHeaders)
        return r.json()

    def createGroupAlbum(self, mid, name):
        data = json.dumps({'title': name, 'type': 'image'})
        params = {
            'homeId': mid,
            'count': '1','auto': '0'
        }
        url = self.server.TIMELINE_MH+'/album/v3/album.json?'+urllib.parse.urlencode(params)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Create a new album failure.')
        return True

    def deleteGroupAlbum(self, mid, albumId):
        params = {
            'homeId': mid
        }
        url = self.urlEncode(self.server.TIMELINE_MH, '/album/v3/album/%s' % albumId, params)
        r = self.deleteContent(url, headers=self.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Delete album failure.')
        return True
    
    def getGroupPost(self, mid, postLimit=50, commentLimit=1, likeLimit=1):
        params = {
            'homeId': mid,
            'postLimit':postLimit,
            'commentLimit': commentLimit,
            'likeLimit': likeLimit,
            'sourceType': 'TALKROOM'
        }
        url = self.server.TIMELINE_API + '/v39/post/list.json?'+urllib.parse.urlencode(params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    """Group Album"""

    def getGroupAlbum(self, mid):
        params = {
            'homeId': mid,
            'type': 'g',
            'sourceType': 'TALKROOM'
        }
        url = self.server.TIMELINE_MH + '/album/v3/albums.json?'+urllib.parse.urlencode(params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    def changeGroupAlbumName(self, mid, albumId, name):
        data = json.dumps({'title': name})
        params = {
            'homeId': mid
        }
        url = self.urlEncode(self.server.TIMELINE_MH, '/album/v3/album/%s' % albumId, params)
        r = self.putContent(url, data=data, headers=self.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Change album name failure.')
        return True

    def addImageToAlbum(self, mid, albumId, path):
        file = open(path, 'rb').read()
        params = {
            'oid': int(time.time()),
            'quality': '90',
            'range': len(file),
            'type': 'image'
        }
        hr = self.additionalHeaders(self.timelineHeaders, {
            'Content-Type': 'image/jpeg',
            'X-Line-Mid': mid,
            'X-Line-Album': albumId,
            'x-obs-params': self.genOBSParams(params,'b64')
        })
        r = self.getContent(self.server.OBS_SG_HOST+'/album/a/upload.nhn', data=file, headers=hr)
        if r.status_code != 201:
            raise Exception('Add image to album failure.')
        return r.json()

    def getImageGroupAlbum(self, mid, albumId, objId, returnAs='path', saveAs=''):
        assert returnAs in ['path','bool','bin'], 'Invalid returnAs value %s'%(returnAs)
        if saveAs == '':
            saveAs = self.genTempFile('path')
        hr = self.additionalHeaders(
            deepcopy(self.timelineHeaders),
            {
                'Content-Type': 'image/jpeg',
                'X-Line-Mid': mid,
                'X-Line-Album': albumId
            }
        )
        params = {
            'ver': '1.0',
            'oid': objId
        }
        url = self.server.OBS_SG_HOST + '/album/a/download.nhn?'+urllib.parse.urlencode(params)
        r = self.getContent(url, headers=hr)
        if r.status_code == 200:
            self.saveFile(saveAs, r.raw)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception('Download image album failure.')

    def uploadObjTalk(self, path, type='image', returnAs='bool', objId=None, to=None):
        assert returnAs in ['objId','bool'], 'Invalid returnAs value %s'%(returnAs)
        assert type in ['image','video','audio','gif','file'], 'Invalid type value %s'%(type)
        headers = None
        files = {
            'file': open(path, 'rb')
        }
        if(type == 'image' or type == 'video' or type == 'audio' or type == 'file'):
            e_p = 'https://obs.line-apps.com/talk/m/upload.nhn'
            data = {'params': self.genOBSParams({'oid': objId,'size': len(open(path, 'rb').read()),'type': type})}

        elif type == 'gif':
            e_p = 'https://obs.line-apps.com/r/talk/m/reqseq'
            files = None
            data = open(path, 'rb').read()
            params = {
                'ver': '1.0',
                'oid': 'reqseq',
                'reqseq': '%s' % str(self.revision),
                'tomid': '%s' % str(to),
                'name': '%s' % str(time.time()*1000),
                'cat': 'original',
                'type': 'image'
            }
            headers = self.additionalHeaders(deepcopy(self.headers), {
                'Content-Type': 'image/gif',
                'Content-Length': str(len(data)),
                'x-obs-params': self.genOBSParams(params,'b64')
            })
        r = self.postContent(e_p, data=data, headers=headers, files=files)
        if r.status_code != 201:
            raise Exception('Upload %s failure.' % type)

        if returnAs == 'objId':
            return objId

        elif returnAs == 'bool':
            return True

    def uploadObjHome(self, path, type='image', returnAs='bool', objId=None):
        assert returnAs in ['objId','bool'], 'Invalid returnAs value %s'%(returnAs)
        assert type in ['image','video','audio'], 'Invalid type value %s'%(type)
        if type == 'image': contentType = 'image/jpeg'
        elif type == 'video': contentType = 'video/mp4'
        elif type == 'audio': contentType = 'audio/mp3'
        if not objId:
            objId = int(time.time())

        file = open(path, 'rb').read()
        params = {
            'name': '%s' % str(time.time()*1000),
            'userid': '%s' % self.profile.mid,
            'oid': '%s' % str(objId),
            'type': type,
            'ver': '1.0'
        }
        hr = self.additionalHeaders(deepcopy(self.timelineHeaders), {
            'Content-Type': contentType,
            'Content-Length': str(len(file)),
            'x-obs-params': self.genOBSParams(params,'b64')
        })
        r = self._session.post(self.server.OBS_SG_HOST + '/myhome/c/upload.nhn', headers=hr, data=file)
        if r.status_code != 201:
            raise Exception('Upload object home failure.')
        if returnAs == 'objId':
            return objId
        elif returnAs == 'bool':
            return True

    def downloadObjectMsg(self, messageId, returnAs='path', saveAs=''):
        assert returnAs in ['path','bool','bin'], 'Invalid returnAs value %s'%(returnAs)

        if saveAs == '':
            saveAs = self.genTempFile('path')

        params = {'oid': messageId}
        url = self.server.OBS_SG_HOST + '/talk/m/download.nhn?'+urllib.parse.urlencode(params)
        r = self.getContent(url)
        if r.status_code == 200:
            self.saveFile(saveAs, r.raw)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception('Download object failure.')            

    def forwardObjectMsg(self, to, msgId, contentType='image'):
        assert contentType in ['image','video','audio'], 'Invalid type value %s'%(contentType)
        data = self.genOBSParams({'oid': 'reqseq','reqseq': self.revision,'type': contentType,'copyFrom': '/talk/m/%s' % msgId},'default')
        r = self.postContent(self.server.OBS_SG_HOST+'/talk/m/copy.nhn', data=data)
        if r.status_code != 200:
            raise Exception('Forward object failure.')

        return True

    def downloadFileURL(self, fileUrl, returnAs='path', saveAs='', headers=None, chunked=False):
        assert returnAs in ['path','bool','bin'], 'Invalid returnAs value %s'%(returnAs)
        if saveAs == '':
            saveAs = self.genTempFile()

        r = self.getContent(fileUrl, headers=headers)
        size = int(r.headers.get('Content-Length', 0))
        chunk_size = size if size > 0 else 16*1024*1024
        if r.ok:
            if chunked:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        self.saveFile(saveAs, chunk)
            else:
                self.saveFile(saveAs, r.raw)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception("Download url failed with code {}".format(r.status_code))

    """Generator"""

    def genTempFile(self, returnAs='path'):
        """
        'alfino-%s-%i.bin' % (int(time.time()), randint(0, 9))
        """
        assert returnAs in ['file','path'], 'Invalid returnAs value %s'%(returnAs)
        fName = 'alfino-nh.bin'
        fPath = tempfile.gettempdir()
        return fName if returnAs == "file" else os.path.join(fPath, fName)

    def genObsParams(self, params):
        return base64.b64encode(json.dumps(params).encode('utf-8'))

    def genObjectId(self):
        random.seed = (os.urandom(1024))
        return ''.join(random.choice("abcdef1234567890") for i in range(32))

    def genOBSParams(self, newList, returnAs='json'):
        assert returnAs in ['json','b64','default'], 'Invalid parameter returnAs %s'%(returnAs)
        oldList = {
            'name': self.genTempFile('file'),
            'ver': '1.0'
        }
        if 'name' in newList and not newList['name']: newList['name'] = oldList['name']
        oldList.update(newList)
        if 'range' in oldList:
            new_range='bytes 0-%s\/%s' % ( str(oldList['range']-1), str(oldList['range']))
            oldList.update({'range': new_range})
        if returnAs == 'json':
            oldList=json.dumps(oldList)
            return oldList
        elif returnAs == 'b64':
            oldList=json.dumps(oldList)
            return base64.b64encode(oldList.encode('utf-8'))
        elif returnAs == 'default':
            return oldList