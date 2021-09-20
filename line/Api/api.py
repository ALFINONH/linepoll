from .session import Server
from random import choice
from copy import deepcopy
import axolotl_curve25519, base64, hmac, hashlib, json, os, rsa, re, requests, socket, sys, traceback, urllib.parse

class Api(Server):
    isCrt = ".cert/"
    isToken = ".tokens/"
    certificate = None

    def __init__(self,):
        Server.__init__(self)
        self.headers.update({
           "User-Agent": self.endpoint.UA[self.APP_TYPE],
           "X-Line-Application": self.endpoint.LA[self.APP_TYPE]
        })

    def login(self):
        self.talk = self._client1(self.console.TalkService, self.host, "/S4", self.headers)
        self.liff = self._client1(self.console.LiffService, self.host, "/LIFF1", self.headers)
        self.channel = self._client1(self.console.ChannelService, self.host, "/CH4", self.headers)
        self.poll = self._client3(self.host, "/P4", self.headers)

        self.revision = self.poll.getLastOpRevision()

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
            self.__write_val(password),
        )
        message = self.__gen_message(message_)
        crypto  = self.__rsa_crypt(message, RSA).hex()
        return crypto

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
        result = mid + ":" + iat + "." + digest
        self.headers.update({'X-Line-Access': result})
        self.authToken = result
        self.login()

    def sign_with_requests_session(self, type, data):
        lReq = self._func.LoginRequest()
        if type == '0':
            lReq.type = 0
            lReq.identityProvider = data['identityProvider']
            lReq.identifier = data['identifier']
            lReq.password = data['password']
            lReq.keepLoggedIn = data['keepLoggedIn']
            lReq.accessLocation = data['accessLocation']
            lReq.systemName = data['systemName']
            lReq.certificate = data['certificate']
            lReq.e2eeVersion = data['e2eeVersion']
        elif type == '1':
            lReq.type = 1
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

    def loginWithCredentialsForCrt(self, email, passwd, certificate= None, systemName = None, appName=None):
        if systemName is None:
            systemName=self.systemName

        if re.compile(r"[^@]+@[^@]+\.[^@]+").match(email):
            self.provider = 1
        else:
            self.provider = 2

        if appName is None:
            appName = self.APP_TYPE

        self.tauth = self._client1(self.console.TalkService, self.host, '/api/v4/TalkService.do', self.headers)
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

        self.auth = self._client1(self.console.AuthService, self.host, '/api/v4p/rs', self.headers)
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
        if result.type == 1:
            self.headers.update({
                'X-Line-Access': result.authToken
            })
            self.certificate = result.certificate
            self.authToken = result.authToken
            self.login()
            self.__defaultCallback("loginWithCredentialsForCertificate: success")
            with open(self.isToken + email +'.session','w') as f:
                f.write(result.authToken)

        elif result.type == 3:
            self.__defaultCallback("›››› Input your pin code on your LINE apps: %s ‹‹‹‹"%result.pinCode)
            self.headers['X-Line-Access'] = result.verifier
            content = requests.get(self.url+"/Q",headers=self.headers).text

            getAccessKey = json.loads(content)
            self.authh = self._client1(self.console.AuthService, self.host, '/api/v4p/rs', self.headers)
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

            if result2.type == 1:
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

    def secondaryQr(self,
          appType="DESKTOPWIN",
          systemName="Linepoll-Client",
          version="6.7.0",
          certificate=None
        ):
        self.clauth = self._client2(
            self.console.LoginService,
            "https://gxx.line.naver.jp/acct/lgn/sq/v1",
             http_header_factory={
                'User-Agent': f'Line/{version}',
                'X-Line-Application': f'{appType}\t{version}\t{systemName}\t10.0.0-NT-x64;SECONDARY',
                'x-lal': 'en_id',
                'server': choice(["pool-1","pool-2"])
           }
        )
        session = self.clauth.createSession(self._func.CreateQrSessionRequest())
        session_id = session.authSessionId
        sys.stdout = open('login.txt', 'w')
        qrcode = self.clauth.createQrCode(self._func.CreateQrCodeRequest(session_id))
        qrCode = qrcode.callbackUrl
        private_key = axolotl_curve25519.generatePrivateKey(os.urandom(32))
        public_key = axolotl_curve25519.generatePublicKey(private_key)
        secret = urllib.parse.quote(base64.b64encode(public_key).decode())
        data = f"{qrCode}?secret={secret}&e2eeVersion=1"
        print(data)
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        with open('login.txt', 'r') as f:
            output = f.read()
        print(str(output))
        os.remove('login.txt')
        self.client_verif = self._client2(
           self.console.LoginPermitNoticeService,
           "https://gxx.line.naver.jp/acct/lp/lgn/sq/v1",
            http_header_factory={
                'User-Agent': f'Line/{version}',
                'X-Line-Application': f'{appType}\t{version}\t{systemName}\t10.0.0-NT-x64;SECONDARY',
                'X-Line-Access': session_id,
                'x-lal': 'en_id',
                'server': choice(["pool-1","pool-2"])
            }
        )
        qrverified = self.client_verif.checkQrCodeVerified(
            self._func.CheckQrCodeVerifiedRequest(session_id)
        )
        if certificate:
            certificate = input(certificate)
        else:
            try:
                certverified = self.clauth.verifyCertificate(
                    self._func.VerifyCertificateRequest(session.authSessionId, certificate)
                )
            except Exception as error:
                print ('Error Verify Certificate :', error)
                sys.stdout = open('login.txt', 'w')
                pincode = self.clauth.createPinCode(
                    self._func.CreatePinCodeRequest(session.authSessionId)
                )
                print (pincode.pinCode)
                sys.stdout.close()
                sys.stdout = sys.__stdout__
                with open('login.txt', 'r') as f:
                    output = f.read()
                print (output)
                sys.stdout = open('login.txt', 'w')
                pincodeverified = self.client_verif.checkPinCodeVerified(
                    self._func.CheckPinCodeVerifiedRequest(session.authSessionId)
                )
                print (pincodeverified)
                sys.stdout.close()
                sys.stdout = sys.__stdout__
                with open('login.txt', 'r') as f:
                    output = f.read()                                    
                print(output)
                sys.stdout = open('login.txt', 'w')
            except Exception:
                traceback.print_exc()
            sys.stdout = open('login.txt', 'w')
            qrcodelogin = self.clauth.qrCodeLogin(
                self._func.QrCodeLoginRequest(session.authSessionId, systemName, True)
            )
            print (f'Qr Code Login : {qrcodelogin.accessToken}\nCRT : {qrcodelogin.certificate}')
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            with open('login.txt', 'r') as f:
                output = f.read()
            print(output)
            self.headers.update({'X-Line-Access': qrcodelogin.accessToken})
            self.authToken = qrcodelogin.accessToken
            self.certificate = qrcodelogin.certificate
            self.login()

    def __defaultCallback(self, txt, callback=None):
        if callback:
            return str(txt)
        print(txt)

    def logout(self):
        self.auth.logoutZ()