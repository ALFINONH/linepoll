# -*- coding: UTF-8 -*-
"""
©alfino
"""
from io import BytesIO as BufferIO
import Crypto.Cipher.PKCS1_OAEP as OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from collections import namedtuple
from pickle import dumps, PickleError

import axolotl_curve25519
import base64
import logging
import urllib.parse
import xxhash
import hashlib
import json, os, random, requests, sys, time, struct, traceback, copy

from copy import deepcopy

KeyPairCurve = namedtuple('KeyPair', ['private_key', 'public_key', 'nonce'])
AESKeyAndIV = namedtuple('AESKey', ['Key', 'IV'])
PICKLE_ERROR = ('Cannot pickle function. Refer to documentation: https://'
                'github.com/ross/requests-futures/#using-processpoolexecutor')

class E2EE:

    def __init__(self, private_key=None, public_key=None, nonce=None):
        self.Curve = self.generateKeypair(private_key, public_key, nonce)

    def _xor(self, buf):
        buf_length = int(len(buf) / 2)
        buf2 = bytearray(buf_length)
        for i in range(buf_length):
            buf2[i] = buf[i] ^ buf[buf_length + i]
        return bytes(buf2)

    def _getSHA256Sum(self, *args):
        instance = hashlib.sha256()
        for arg in args:
            if isinstance(arg, str):
                arg = arg.encode()
            instance.update(arg)
        return instance.digest()

    def _encryptAESECB(self, aes_key, plain_data):
        aes = AES.new(aes_key, AES.MODE_ECB)
        return aes.encrypt(plain_data)

    def _decryptAESECB(self, aes_key, encrypted_data):
        aes = AES.new(aes_key, AES.MODE_ECB)
        return aes.decrypt(encrypted_data)

    def _encryptAESCBC(self, aes_key, aes_iv, plain_data):
        aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        return aes.encrypt(plain_data)

    def _decrpytAESCBC(self, aes_key, aes_iv, encrypted_data):
        aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        return aes.decrypt(encrypted_data)

    def generateKeypair(self, private_key=None, public_key=None, nonce=None):
        private_key = private_key if private_key else axolotl_curve25519.generatePrivateKey(os.urandom(32))
        public_key = public_key if public_key else axolotl_curve25519.generatePublicKey(private_key)
        nonce = nonce if nonce else os.urandom(16)
        return KeyPairCurve(private_key, public_key, nonce)

    def generateParams(self):
        secret = base64.b64encode(self.Curve.public_key).decode()
        return 'secret={secret}&e2eeVersion=1'.format(secret=urllib.parse.quote(secret))

    def generateSharedSecret(self, public_key):
        private_key = self.Curve.private_key
        shared_secret = axolotl_curve25519.calculateAgreement(private_key, public_key)
        return shared_secret

    def calculateSignature(self, private_key, message):
        return axolotl_curve25519.calculateSignature(os.urandom(32), private_key, message)

    def calculateAgreement(self, private_key, public_key):
        return axolotl_curve25519.calculateAgreement(private_key, public_key)

    def generateAESKeyAndIV(self, shared_secret):
        aes_key = self._getSHA256Sum(shared_secret, 'Key')
        aes_iv = self._xor(self._getSHA256Sum(shared_secret, 'IV'))
        return AESKeyAndIV(aes_key, aes_iv)

    def generateSignature(self, aes_key, encrypted_data):
        data = self._xor(self._getSHA256Sum(encrypted_data))
        signature = self._encryptAESECB(aes_key, data)
        return signature

    def verifySignature(self, signature, aes_key, encrypted_data):
        data = self._xor(self._getSHA256Sum(encrypted_data))
        return self._decryptAESECB(aes_key, signature) == data

    def decryptKeychain(self, encrypted_keychain, public_key):
        public_key = base64.b64decode(public_key)
        encrypted_keychain = base64.b64decode(encrypted_keychain)
        shared_secret = self.generateSharedSecret(public_key)
        aes_key, aes_iv = self.generateAESKeyAndIV(shared_secret)
        keychain_data = self._decrpytAESCBC(aes_key, aes_iv, encrypted_keychain)
        return keychain_data

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