from datetime import datetime
from copy import deepcopy
import base64, urllib, tempfile, shutil, json, random, threading, traceback, os, re, rsa,time, pytz, requests, hashlib, ntpath

import urllib.request
import urllib.parse

class Timeline:

    isLoggin = False

    def __init__(self):
        self.isLoggin = True

    def _loginLineTimeline(self):
        channelToken = self.channel.issueChannelToken("1341209850")
        self.channel_access_token = channelToken.channelAccessToken
        self.refresh_token = channelToken.refreshToken
        self.obs_token = self.talk.acquireEncryptedAccessToken(2)
        self.timelineHeaders.update({
            'Content-Type': 'application/json',
            "User-Agent": self.endpoint.UA[self.APP_TYPE],
            "X-Line-Application":self.endpoint.LA[self.APP_TYPE],
            'X-Line-Carrier': '51089, 1-0',
            "X-Line-AcceptLanguage": 'en',
            'X-Line-Mid': self.profile.mid,
            "X-Line-ChannelToken": self.channel_access_token,
            "X-Requested-With": 'jp.naver.line.android.LineApplication'
            })

    def downloadObjectMsg(self, messageId, returnAs='path', saveAs=''):
        assert returnAs in ['path','bool','bin'], 'Invalid returnAs value %s'%(returnAs)
        if saveAs == '':
            saveAs = self.genTempFile('path')
        params = {'oid': messageId}
        url = 'https://obs-sg.line-apps.com/talk/m/download.nhn?'+urllib.parse.urlencode(params)
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

    def downloadFileURL(self, fileUrl, returnAs='path', saveAs='', headers=None, chunked=False):
        assert returnAs in ['path','bool','bin'], 'Invalid returnAs value %s'%(returnAs)
        if saveAs == '':
            saveAs = self.genTempFile()
        r = self.getContent(fileUrl)
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

    def uploadObjHome(self, path, type='image', objId=None):
        if type not in ['image','video','audio']:
            raise Exception('Invalid type value')
        if type == 'image':
            contentType = 'image/jpeg'
        elif type == 'video':
            contentType = 'video/mp4'
        elif type == 'audio':
            contentType = 'audio/mp3'
        if not objId:
            hstr = 'Linepoll-Client_%s' % int(time.time()*1000)
            objid = hashlib.md5(hstr.encode()).hexdigest()
        file = open(path, 'rb').read()
        params = {
            'name': '%s' % str(time.time()*1000),
            'userid': '%s' % self.profile.mid,
            'oid': '%s' % str(objId),
            'type': type,
            'ver': '1.0'
        }
        hr = {
            'Content-Type': contentType,
            'Content-Length': str(len(file)),
            'x-obs-params': self.genOBSParams(params,'b64') #base64 encode
        }
        hr.update(self.timelineHeaders)
        r = self.postContent('https://obs-tw.line-apps.com/myhome/c/upload.nhn', headers=hr, data=file)

        if r.status_code != 201:
            raise Exception(f"Upload object home failure. Receive statue code: {r.status_code}")
        return objId
        
    def uploadObjTalk(self, path=None, type='image', objId=None, to=None):
        if type not in ['image','gif','video','audio','file']:
            raise Exception('Invalid type value')
        headers=None
        files = {'file': open(path, 'rb')}
        #url = 'https://obs.line-apps.com/talk/m/upload.nhn' #if reqseq not working
        url = 'https://obs.line-apps.com/r/talk/m/reqseq'
        params = {
            "type": "image",
            "ver": "2.0",
            "name": files['file'].name,
            "oid": "reqseq",
            "reqseq": str(self.revision),
            "cat": "original"
        }
        if objId != None:
            params['oid'] = objId
        if to != None:
            params['tomid'] = to
        if type != 'gif':
            params['type'] = type
            data = {'params': self.genOBSParams(params)}
        elif type == 'gif':
            params = {
                'type': 'image',
                'ver': '2.0',
                'name': files['file'].name,
                'oid': 'reqseq',
                'reqseq': '%s' % str(self.revision),
                'tomid': '%s' % str(to),
                'cat': 'original'
            }
            files = None
            data = open(path, 'rb').read()
            headers = {
                'content-type': 'image/gif',
                'Content-Length': str(len(data)),
                'x-obs-params': self.genOBSParams(params,'b64'), #base64 encode
                'X-Line-Access': self.obs_token
            }
            headers.update(self.headers)
        r = self.postContent(url, data=data, headers=headers, files=files)
        if r.status_code != 201:
            console.log("uploadObjTalk: ", r.text)
            raise Exception('Upload %s failure.' % type)
        else:
            if objId is None:
                objId = r.headers['x-obs-oid']
            objHash = r.headers['x-obs-hash']
        return objId

    def getActorId(self, data):
        result = data["postEndUrl"]
        metadata = result.replace('https://line.me/R/home/post?','').split('&')
        if('userMid=' in metadata[0]):
            actorId = metadata[0].replace('userMid=','')
            return actorId

        elif('homeId=' in metadata[0]):
            actorId = metadata[0].replace('homeId=','')
            return actorId

    def getProfileDetails(self, mid=None):
        if mid is None:
            mid = self.profile.mid

        params = {
            'homeId': mid
        }
        hr = {
            'x-lhm': "GET",
        }
        hr.update(self.timelineHeaders)
        url = 'https://ga2.line.naver.jp/hm/api/v1/home/cover.json?'+urllib.parse.urlencode(params)
        r = self.postContent(url, headers=hr)
        return r.json()

    def getProfileDetail(self, mid=None):
        if mid is None:
            mid = self.profile.mid

        params = {
            'userMid': mid
        }
        hr = deepcopy(self.timelineHeaders)
        hr.update({
            'x-lhm': "GET",
        })
        url = 'https://gd2.line.naver.jp/mh/api/v1/userpopup/getDetail.json?'+urllib.parse.urlencode(params)
        r = self.getContent(url, headers=hr)
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
        url = 'https://obs-sg.line-apps.com/myhome/c/download.nhn?'+urllib.parse.urlencode(params)
        return url

    def updateProfileCover(self, path):
        hstr = 'Linepoll-Client_%s' % int(time.time()*1000)
        objid = hashlib.md5(hstr.encode()).hexdigest()
        objId = self.uploadObjHome(path, type='image', objId=objid)
        home = self.updateProfileCoverById(objId)
        return objId

    def changeProfileCover(self, path):
        hstr = 'Linepoll_%s' % int(time.time() * 1000)
        objid = hashlib.md5(hstr.encode()).hexdigest()
        if not objid:
            hstr = 'Linepoll_%s' % int(time.time()*1000)
            objid = hashlib.md5(hstr.encode()).hexdigest()
        url = f'https://obs.line-apps.com/r/myhome/c/{objid}'
        file = {'file': open(path, 'rb')}
        params = {
            'name': objid,
            'quality': '100',
            'type': 'image',
            'ver': '2.0'
        }
        data = {'params': json.dumps(params)}
        r = self.postContent(url, headers=self.timelineHeaders, data=data, files=file)
        if r.status_code != 201:
            raise Exception(f"Upload object home failure. Receive statue code: {r.status_code}")
        objId = r.headers['x-obs-oid']
        home = self.updateProfileCoverById(objId)
        return home
    
    def updateProfileCoverById(self, objid, vObjid=None):
        """
        params = {
            'coverImageId': objId
        }
        url = 'https://gd2.line.naver.jp/mh/api/v39/home/updateCover.json?' + urllib.parse.urlencode(params)
        r = requests.get(url, headers=deepcopy(self.timelineHeaders))
        """
        data = {
            "homeId": self.profile.mid,
            "coverObjectId": objid,
            "storyShare": False,
            "meta":{}
        }
        if vObjid:
            data['videoCoverObjectId'] = vObjid
        hr = {
            'x-lhm': "POST",
        }
        hr.update(self.timelineHeaders)
        r = self.postContent('https://ga2.line.naver.jp/hm/api/v1/home/cover.json', headers=hr, data=json.dumps(data))
        return r.json()

    def updateGroupPicture(self, groupId, path):
        files = {'file': open(path, 'rb')}
        ob_params = {
            'oid': groupId,
            'type': 'image',
            'name': 'alfino-nh.bin',
            'ver': '1.0'
        }
        data = {'params': json.dumps(ob_params)}
        url = 'https://obs-sg.line-apps.com/talk/g/upload.nhn'
        headers = deepcopy(self.headers)
        self.postContent(url, headers=headers, data=data, files=files)

        return True

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
        r = self.postContent('https://obs-sg.line-apps.com/talk/p/upload.nhn', headers=deepcopy(self.headers), data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update profile picture failure.')
        return True

    def updateProfileImage(self, path):
        url = f'https://obs.line-apps.com/r/talk/p/{self.profile.mid}'
        file = open(path, 'rb')
        hstr = 'Linepoll_%s' % int(time.time() * 1000)
        file_name = hashlib.md5(hstr.encode()).hexdigest()
        params = {
            'name': file_name,
            'quality': '100',
            "type": "image",
            "ver": "2.0"
        }
        r = self.postContent(url, headers=self.timelineHeaders, data={'params': json.dumps(params)}, files={'file':file})
        if r.status_code != 201:
            raise Exception(f"updateProfileImage failure. Receive statue code: {r.status_code}")
        return objId

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
            r_vp = self.postContent('https://obs-sg.line-apps.com/talk/vp/upload.nhn',headers = deepcopy(self.headers), data=datas, files=files)
            if r_vp.status_code != 201:
                raise Exception("Update vide profile Failed")
            self.updateProfilePicture(pict, 'vp')
        except Exception:
            print("< Update profile video failed>")

    def getPost(self, mid, postId):
        params = {
            'homeId': mid,
            'postId': postId,
        }
        hr = {
            'x-lhm': "GET",
            'Content-type': "application/json",
            'x-lpv': '1',
            'x-lsr':'ID'
        }
        hr.update(self.timelineHeaders)
        url = 'https://gwz.line.naver.jp/mh/api/v52/post/get.json?'+urllib.parse.urlencode(params)
        r = self.postContent(url, headers=hr)
        return r.json()

    def createPost(self, text, holdingTime=None):
        params = {
               'homeId': self.profile.mid,
               'sourceType': 'TIMELINE'
        }
        url = 'https://gd2.line.naver.jp/mh/api/v39/post/create.json?' + urllib.parse.urlencode(params)
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
        r = self.postContent(url, headers=self.timelineHeaders, data=data)
        return r.json()

    def sendPostToTalk(self, mid, postId):
        if mid is None:
            mid = self.profile.mid

        params = {
           'receiveMid': mid,
           'postId': postId
        }
        url = 'https://gd2.line.naver.jp/mh/api/v39/post/sendPostToTalk.json?' + urllib.parse.urlencode(params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    def searchNote(self, mid, text):
        data = {
           "query" : text,
           "queryType" : "TEXT",
           "homeId" : mid,
           "postLimit" : 20,
           "commandId" : 16,
           "channelId" : "1341209850",
           "commandType" : 188259
        }
        url = 'https://gwz.line.naver.jp/mh/api/v46/search/note.json?'+urllib.parse.urlencode({})
        r = self.postContent(url, headers=self.timelineHeaders, data=json.dumps(data))
        res = r.json()
        return res["result"]["feeds"]

    def listComment(self, mid, contentId):
        params = {
            'homeId': mid,
            #'actorId': actorId,
            'contentId': contentId,
            #'limit': 10
        }
        hr = {
            'x-lhm': "GET",
            'Content-type': "application/json",
            'x-lpv': '1',
            'x-lsr':'ID'
        }
        hr.update(self.timelineHeaders)
        url = 'https://gwz.line.naver.jp/mh/api/v52/comment/getList.json?' + urllib.parse.urlencode(params)
        r = self.postContent(url, headers=hr)
        return r.json()

    def createComment(self, mid, postId, text):
        params = {
            'homeId': mid,
            'sourceType': 'TIMELINE'
        }
        payload = {
            'commentText': text,
            'activityExternalId': postId,
            'actorId': mid
        }

        header = {
            'x-lhm': "POST",
            "Content-Type" : "application/json",
            "User-Agent": self.endpoint.UA[self.APP_TYPE],
            "X-Line-Application":self.endpoint.LA[self.APP_TYPE],
            "X-Line-Mid" : self.profile.mid,
            "x-lct" : self.channel_access_token,
            'x-lpv': '1'
        }
        url = 'https://gd2.line.naver.jp/mh/api/v39/comment/create.json?' + urllib.parse.urlencode(params)
        data = json.dumps(payload)
        r = self.postContent(url, headers=header, data=data)
        return r.json()

    def createComments(self, mid, contentId, text, id=1, pkgid=1,pkgver=1):
        params = {
            'homeId': mid
        }
        data = {
           "contentId" : contentId,
           "commentText" : text,
           "secret" : False,
           "contentsList" : [
              {
                 "categoryId" : "sticker",
                 "extData" : {
                    "id" : id,
                    "packageId" : pkgid,
                    "packageVersion" : pkgver
                 }
              }
           ],
           "commandId" : 16777257,
           "channelId" : "1341209850",
           "commandType" : 188208
        }
        hr = {
            'x-lhm': "POST",
            'Content-type': "application/json",
            'x-lpv': '1',
            'x-lsr':'ID'
        }
        hr.update(self.timelineHeaders)
        url = 'https://gwz.line.naver.jp/mh/api/v52/comment/create.json?' + urllib.parse.urlencode(params)
        r = self.postContent(url, headers=hr, json=data)
        return r.json()

    def deleteComment(self, mid, postId, commentId):
        header = {
            "Content-Type" : "application/json",
            "User-Agent": self.endpoint.UA[self.APP_TYPE],
            "X-Line-Application":self.endpoint.LA[self.APP_TYPE],
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
        url = 'https://gd2.line.naver.jp/mh/api/v39/comment/delete.json?' + urllib.parse.urlencode(params)
        data = json.dumps(payload)
        r = self.postContent(url, headers=header, data=data)
        return r.json()

    def deleteComments(self, mid, contentId, commentId):
        params = {
            'homeId': mid,
            'commentId': commentId
        }
        hr = {
            'x-lhm': "GET",
            'Content-type': "application/json",
            'x-lpv': '1',
            'x-lsr':'ID'
        }
        hr.update(self.timelineHeaders)
        url = 'https://gwz.line.naver.jp/mh/api/v52/comment/delete.json?' + urllib.parse.urlencode(params)
        r = self.postContent(url, headers=hr)
        return r.json()

    def likePost(self, mid, postId, likeType=None):
        if likeType == None:
            likeType = random.choice([1001,1002,1003,1004,1005,1006])

        params = {
            'homeId': mid #'sourceType': 'TIMELINE'
        }
        url = 'https://gd2.line.naver.jp/mh/api/v39/like/create.json?' + urllib.parse.urlencode(params)
        payload = {
            'likeType': likeType,
            'activityExternalId': postId,
            'actorId': mid,
            "sharable" : False
        }
        r = self.postContent(url, headers=self.timelineHeaders, data=json.dumps(payload))
        return r.json()

    def createLike(self, mid, contentId, likeType=None):
        if likeType == None:
            likeType = random.choice([1001,1002,1003,1004,1005,1006])

        params = {
            'homeId': mid
        }
        data = {
           "contentId" : contentId,
           "likeType" : str(likeType),
           "sharable" : False,
           "commandId" : 16777265,
           "channelId" : "1341209850",
           "commandType" : 188210
        }
        hr = {
            'x-lhm': "POST",
            'Content-type': "application/json",
            'x-lpv': '1',
            'x-lsr':'ID'
        }
        hr.update(self.timelineHeaders)
        url = 'https://gwz.line.naver.jp/mh/api/v41/like/create.json?' + urllib.parse.urlencode(params)
        r = self.postContent(url, headers=hr, json=data)
        return r.json()

    def cancelLike(self, contentId):
        params = {
            'contentId': contentId,
        }
        hr = {
            'x-lhm': "GET",
            'Content-type': "application/json",
            'x-lpv': '1',
            'x-lsr':'ID'
        }
        hr.update(self.timelineHeaders)
        url = 'https://gwz.line.naver.jp/mh/api/v41/like/cancel.json?'+urllib.parse.urlencode(params)
        r = self.postContent(url, headers=hr)
        return r.json()

    def listLike(self, mid, contentId):
        params = {
            'homeId': mid,
            'contentId': contentId,
        }
        hr = {
            'x-lhm': "GET",
            'Content-type': "application/json",
            'x-lpv': '1',
            'x-lsr':'ID'
        }
        hr.update(self.timelineHeaders)
        url = 'https://gwz.line.naver.jp/mh/api/v52/like/getList.json?' + urllib.parse.urlencode(params)
        r = self.postContent(url, headers=hr)
        return r.json()

    def unlikePost(self, mid, postId):
        if mid is None:
            mid = self.profile.mid
        params = {
            'homeId': mid,
            'sourceType': 'TIMELINE'
        }
        url = 'https://gd2.line.naver.jp/mh/api/v39/like/cancel.json?' + urllib.parse.urlencode(params)
        data = json.dumps({'activityExternalId': postId, 'actorId': mid})
        r = self.postContent(url, headers=self.timelineHeaders, data=data)
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
        r = self.postContent(url, headers=self.timelineHeaders, data=data)
        return r.json()

    def createPostGroupR(self, text,to):
        params = {
            'homeId': to,
            'sourceType': 'GROUPHOME'
        }
        url = 'https://gd2.line.naver.jp/mh/api/v39/relay/create.json?'+urllib.parse.urlencode(params)
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
        r = self.postContent(url, headers=self.timelineHeaders, data=data)
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
        r = self.postContent('https://gd2.line.naver.jp/mh/api/v39/post/create.json', headers=self.timelineHeaders, data=data)
        return r.json()

    def createGroupAlbum(self, mid, name):
        data = json.dumps({'title': name, 'type': 'image'})
        params = {
            'homeId': mid,
            'count': '1','auto': '0'
        }
        url = 'https://gd2.line.naver.jp/mh/album/v3/album.json?'+urllib.parse.urlencode(params)
        r = self.postContent(url, headers=self.timelineHeaders, data=data)
        if r.status_code != 201:
            raise Exception('Create a new album failure.')
        return True

    def deleteGroupAlbum(self, mid, albumId):
        params = {
            'homeId': mid
        }
        url = 'https://gd2.line.naver.jp/mh'+ '/album/v3/album/%s' % albumId + urllib.parse.urlencode(params)
        r =self.deleteContent(url, headers=self.timelineHeaders)
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
        url = 'https://gd2.line.naver.jp/mh/api/v39/post/list.json?'+urllib.parse.urlencode(params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    """Group Album"""

    def getGroupAlbum(self, mid):
        params = {
            'homeId': mid,
            'type': 'g',
            'sourceType': 'TALKROOM'
        }
        url = 'https://gd2.line.naver.jp/mh/album/v3/albums.json?'+urllib.parse.urlencode(params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    def changeGroupAlbumName(self, mid, albumId, name):
        data = json.dumps({'title': name})
        params = {
            'homeId': mid
        }
        #url + path + '?' + urllib.parse.urlencode(params)
        url = "https://gd2.line.naver.jp/mh/album/v3/album/"+ albumId+"?"+urllib.parse.urlencode(params)
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
        hr = {
            'Content-Type': 'image/jpeg',
            'X-Line-Mid': mid,
            'X-Line-Album': albumId,
            'x-obs-params': self.genOBSParams(params,'b64')
        }
        hr.update(self.timelineHeaders)
        r = self.postContent('https://obs-sg.line-apps.com/album/a/upload.nhn', headers=hr, data=file)
        if r.status_code != 201:
            raise Exception('Add image to album failure.')
        return r.json()

    def getImageGroupAlbum(self, mid, albumId, objId, returnAs='path', saveAs=''):
        assert returnAs in ['path','bool','bin'], 'Invalid returnAs value %s'%(returnAs)
        if saveAs == '':
            saveAs = self.genTempFile('path')
        hr = {
                'Content-Type': 'image/jpeg',
                'X-Line-Mid': mid,
                'X-Line-Album': albumId
            }
        hr.update(self.timelineHeaders)
        params = {
            'ver': '1.0',
            'oid': objId
        }
        url = 'https://obs-sg.line-apps.com/album/a/download.nhn?'+urllib.parse.urlencode(params)
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
