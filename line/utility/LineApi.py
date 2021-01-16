# -*- coding: UTF-8 -*-
"""
    ~~~~~~~~~~~
    Simple linebot
    created by: 
    ©finbot alfino~nh
    ~~~~~~~~~~~
"""
from typing import Optional
from ..lib.PrimaryAccountInitService import PrimaryAccountInitService
from ..lib.PrimaryAccountInitService.ttypes import *
from ..lib.SecondaryQrCodeLogin import *
from ..lib.SecondaryQrCodeLogin.ttypes import CreateQrSessionRequest, CreateQrCodeRequest, CheckQrCodeVerifiedRequest, VerifyCertificateRequest, CreatePinCodeRequest, SecondaryQrCodeException, CheckPinCodeVerifiedRequest, QrCodeLoginRequest
from ..lib.curve.ttypes import LoginRequest, LoginType, IdentityProvider, LoginResultType

from . LineServer import LineServer, LineConnect
from random import choice, randint
import axolotl_curve25519
import hashlib
import hmac
import socket
import json, time, re, rsa, os, urllib.parse, shutil, base64, uuid

class LineApi(object):

    def __init__(self):
        self.headers = {}

    def login(self):
        self.line = {'talk':LineServer(self.headers).LT(), 'poll': LineServer(self.headers).LP(), 'call': LineServer(self.headers).LC(), 'shop': LineServer(self.headers).LS(), 'liff': LineServer(self.headers).LL(), 'message': LineServer(self.headers).LM(), 'channel': LineServer(self.headers).LCH()}
        self.isLogin = True

    def sign_with_requests_session(self, type, data):
        lReq = LoginRequest()
        if type == '0':
            lReq.type = LoginType.ID_CREDENTIAL
            lReq.identityProvider = data['identityProvider']
            lReq.identifier = data['identifier']
            lReq.password = data['password']
            lReq.keepLoggedIn = data['keepLoggedIn']
            lReq.accessLocation = data['accessLocation']
            lReq.systemName = data['systemName']
            lReq.certificate = data['certificate']
            lReq.e2eeVersion = data['e2eeVersion']
        elif type == '1':
            lReq.type = LoginType.QRCODE
            lReq.keepLoggedIn = data['keepLoggedIn']
            if 'identityProvider' in data:
                lReq.identityProvider = data['identityProvider']
            if 'accessLocation' in data:
                lReq.accessLocation = data['accessLocation']
            if 'systemName' in data:
                lReq.systemName = data['systemName']
            lReq.verifier = data['verifier']
            lReq.e2eeVersion = data['e2eeVersion']
        else:
            lReq=False
        return lReq

    def setHeadersWithDict(self, headersDict):
        self.headers.update(headersDict)

    def setHeaders(self, argument, value):
        self.headers[argument] = value

    def __write_val(self, data):
        return (chr(len(data)) + data)
		
    def __gen_message(self, tuple_msg):
        return (''.join(tuple_msg)).encode('utf-8')

    def __rsa_crypt(self, message, RSA):
        pub_key = rsa.PublicKey(int(RSA.nvalue, 16), int(RSA.evalue, 16))
        crypto  = rsa.encrypt(message, pub_key)
        return crypto

    def _encryptedEmailAndPassword(self, mail, passwd, RSA):
        message_ = (
            self.__write_val(RSA.sessionKey),
            self.__write_val(mail),
            self.__write_val(passwd),
        )
        message = self.__gen_message(message_)
        crypto  = self.__rsa_crypt(message, RSA).hex()
        return crypto

    def _encryptedPhoneAndPassword(self, phone, password, RSA):
        message_ = (
            self.__write_val(RSA.sessionKey),
            self.__write_val(phone),
            self.__write_val(passwd),
        )
        message = self.__gen_message(message_)
        crypto  = self.__rsa_crypt(message, RSA).hex()
        return crypto

    def generateUdidHash(self):
        UDID = uuid.uuid4().hex
        return UDID

    def createPrimaryOrSecondary(self, uri: str, headers=None, service = None):
        return LineServer(headers)._make_thttp_client(uri, service, False)

    def requestEmailConfirmation(self, email, password, ignoreDuplication=False, useEmailOnly=False):
        raise NotImplementedError("for some reasons line removed it.")

    def resendEmailConfirmation(self, verifier):
        raise NotImplementedError("for some reasons line removed it.")

    def confirmEmail(self, verifier, pincode):
        raise NotImplementedError("for some reasons line removed it.")

    def deviceInfo(self, appType=32):
        raise NotImplementedError("for some reasons line removed it.")

    def startVerification(self, phoneNumber, region, seed='', appType=32):
        raise NotImplementedError("for some reasons line removed it.")

    def changeVerificationMethod(self, sessionId, method):
        raise NotImplementedError("for some reasons line removed it.")

    def verifyPhoneNumber(self, sessionId, pincode, seed=''):
        raise NotImplementedError("for some reasons line removed it.")

    def registerWithPhoneNumber(self, tuple_verifyPhoneNumber):
        raise NotImplementedError("for some reasons line removed it.")

    def registerWithFacebook(self, fbtoken, seed='', appType=32, country="JP"):
        raise NotImplementedError("for some reasons line removed it.")

    def createAccountMigrationPincodeSession(self):
        raise NotImplementedError("for some reasons line removed it.")

    def findSnsIdUserStatus(self, snsIdType, snsAccessToken, udidHash, migrationPincodeSessionId, oldUdidHash):
        raise NotImplementedError("for some reasons line removed it.")

    def registerWithSnsId(self, snsIdType, snsAccessToken, region, udidHash, deviceInfo, mid, migrationPincodeSessionId):
        raise NotImplementedError("for some reasons line removed it.")

    def register_account(self, seed=''):
        """
        self.talk = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_API_QUERY_PATH_FIR).Talk()
        #res = requests.post('https://ga2s.line.naver.jp/plc/api/core/device/issueUdid', data=json.dumps(payload), #headers=header)
        #udidHash = res.json()['udidHash']
        #print(udidHash)
        udidHash = hashlib.md5( ('cool'+seed).encode() ).hexdigest()
        oldUdidHash = hashlib.md5( (udidHash).encode() ).hexdigest()
        return self.talk.registerDeviceWithoutPhoneNumber("JP", udidHash, self.deviceInfo())
        """
        raise NotImplementedError("for some reasons line removed it.")

    def get_issued_at(self) -> bytes:
        return base64.b64encode(
            f"iat: {int(time.time()) * 60}\n".encode("utf-8")) + b"."

    def get_digest(self, key: bytes, iat: bytes) -> bytes:
        return base64.b64encode(hmac.new(key, iat, hashlib.sha1).digest())

    def generateAccessToken(self, authKey):
        mid, key = authKey.partition(":")[::2]
        key = base64.b64decode(key.encode("utf-8"))
        iat = self.get_issued_at()
        digest = self.get_digest(key, iat).decode("utf-8")
        iat = iat.decode("utf-8")
        return mid + ":" + iat + "." + digest

    def loginWithQrCode(self, certificate=None):
        self.cl = self.createPrimaryOrSecondary(
            'https://gxx.line.naver.jp/acct/lgn/sq/v1',
            headers = {
                'User-Agent': 'Line/5.21.3',
                'X-Line-Application': 'DESKTOPWIN\t5.21.3\tALFINO-PCV3\t10.0;SECONDARY',
                'x-lal': 'en_id',
                'server': choice(["pool-1","pool-2"])
            },
            service = SecondaryQrCodeLoginService.Client
        )
        session = self.cl.createSession(CreateQrSessionRequest())
        session_id = session.authSessionId
        qrcode = self.cl.createQrCode(CreateQrCodeRequest(session_id))
        qrCode = qrcode.callbackUrl
        private_key = axolotl_curve25519.generatePrivateKey(os.urandom(32))
        public_key = axolotl_curve25519.generatePublicKey(private_key)
        secret = urllib.parse.quote(base64.b64encode(public_key).decode())
        data = f"{qrCode}?secret={secret}&e2eeVersion=1"
        self.__defaultCallback(data)
        self.client_verif = self.createPrimaryOrSecondary(
            'https://gxx.line.naver.jp/acct/lp/lgn/sq/v1',
            headers={
                'User-Agent': 'Line/5.21.3',
                'X-Line-Application': 'DESKTOPWIN\t5.21.3\tALFINO-PCV3\t10.0;SECONDARY',
                'X-Line-Access': session_id,
                'x-lal': 'en_id',
                'server': choice(["pool-1","pool-2"])
            },
            service=SecondaryQrCodeLoginPermitNoticeService.Client
        )
        qrverified = self.client_verif.checkQrCodeVerified(CheckQrCodeVerifiedRequest(session_id))
        if certificate != None:
            self.certificate = certificate
        else:
            try:
                self.cl.verifyCertificate(VerifyCertificateRequest(session.authSessionId, self.certificate))
                return True
            except SecondaryQrCodeException:
                return False
                os.system('clear')
                self.pincode = self.cl.createPinCode(CreatePinCodeRequest(session.authSessionId))
                self.__defaultCallback('Pin Code :', self.pincode.pinCode)
                self.pincodeverified = self.client_verif.checkPinCodeVerified(CheckPinCodeVerifiedRequest(session.authSessionId))
                self.__defaultCallback('Pin Code Verified :', self.pincodeverified)
            qrcodelogin = self.cl.qrCodeLogin(QrCodeLoginRequest(session.authSessionId, 'ALFINO-PCV3', True))
            self.__defaultCallback(f'Qr Code Login : {qrcodelogin.accessToken}\nCRT : {qrcodelogin.certificate}')
            self.headers.update({
                'User-Agent': 'Line/5.21.3',
                'X-Line-Application': 'DESKTOPWIN\t5.21.3\tALFINO-PCV3\t10.0;SECONDARY',
                'X-Line-Access': qrcodelogin.accessToken,
                'x-lal': 'en_id'
            })
            self.certificate = qrcodelogin.certificate
            self.authToken = qrcodelogin.accessToken

    def loginWithCredentialsForCrt(self, email, passwd, certificate= None, systemName = None, appName=None):
        if systemName is None:
            systemName=self.server.DEVICE_NAME

        if re.compile(r"[^@]+@[^@]+\.[^@]+").match(email):
            self.provider = IdentityProvider.LINE
        else:
            self.provider = IdentityProvider.LINE_KR

        if appName is None:
            appName=self.LA

        self.headers['X-Line-Application'] = appName
        self.tauth = LineServer(self.headers).LTSD()
        rsaKey      = self.tauth.getRSAKeyInfo(self.provider)
        crypto     = self._encryptedEmailAndPassword(email, passwd, rsaKey)
        try:
            with open(self.isCrt + email + '.crt', 'r') as f:
                self.certificate = f.read()
        except:
            if certificate is not None:
                self.certificate = certificate
                if os.path.exists(certificate):
                    with open(certificate, 'r') as f:
                        self.certificate = f.read()

        self.auth = LineServer(self.headers).LLR()
        accessLocation = socket.gethostbyname(socket.gethostname())
        lReq = self.sign_with_requests_session('0', {
            'identityProvider': self.provider,
            'identifier': rsaKey.keynm,
            'password': crypto,
            'keepLoggedIn': True,
            'accessLocation': accessLocation,
            'systemName': systemName,
            'certificate': self.certificate,
            'e2eeVersion': 0
        })
        result = self.auth.loginZ(lReq)
        if result.type == LoginResultType.SUCCESS:
            self.headers.update({
                'X-Line-Access': result.authToken
            })
            self.certificate = result.certificate
            self.authToken = result.authToken
            self.login()
            self.__defaultCallback("loginWithCredentialsForCertificate: success")
            with open(self.isToken + email +'.session','w') as f:
                f.write(result.authToken)

        elif result.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
            self.__defaultCallback("›››› Input your pin code on your LINE apps: %s ‹‹‹‹"%result.pinCode)
            self.setHeaders('X-Line-Access', result.verifier)
            getAccessKey = LineServer(self.headers).LCR()
            self.authh = LineServer(self.headers).LLR()
            try:
                _lreq = self.sign_with_requests_session('1', {
                    'identityProvider': self.provider,
                    'keepLoggedIn': True,
                    'accessLocation': accessLocation,
                    'systemName': systemName,
                    'verifier': getAccessKey['result']['verifier'],
                    'e2eeVersion': 0
                })
                result2 = self.authh.loginZ(_lreq)
            except:
                raise Exception('Login failed <%s>'%email)

            if result2.type == LoginResultType.SUCCESS:
                if result2.certificate is not None:
                    with open(self.isCrt + email + '.crt', 'w') as f:
                        f.write(result2.certificate)
                    self.certificate = result2.certificate

                if result2.authToken is not None:
                    self.headers.update({'X-Line-Access': result2.authToken})
                    self.authToken = result2.authToken 
                    self.login()
                    self.__defaultCallback("loginWithCredentialsForCertificate: success")
                    with open(self.isToken + email +'.session','w') as f:
                        f.write(result2.authToken)
                else:
                    return False

            else:
                self.__defaultCallback('Login "%s" failed...'%email)

    def __defaultCallback(self, txt, callback=None):
        if callback:
            return str(txt)
        print(txt)

    def logout(self):
        self.auth.logoutZ()