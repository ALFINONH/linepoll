import sys

class Client(object):
    def __init__(self, iprot, oprot=None):        
        self._iprot = self._oprot = iprot

        if oprot is not None:
            self._oprot = oprot

        self._seqid = 0
        self.sequence = 0

    def getLastOpRevision(self):
        self._oprot.writeMessageBegin('getLastOpRevision', 1, self._seqid)
        args = getLastOpRevision_args()
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()
        return self.recv_getLastOpRevision()

    def recv_getLastOpRevision(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == 3:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getLastOpRevision_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TApplicationException(5, "getLastOpRevision failed: unknown result")

    def fetchOperations(self, localRev, count):
        self._oprot.writeMessageBegin('fetchOperations', 1, self._seqid)
        args = fetchOperations_args(localRev = localRev,count = count)
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()
        return self.recv_fetchOperations()

    def recv_fetchOperations(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == 3:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = fetchOperations_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TApplicationException(5, "fetchOperations failed: unknown result")

    def fetchOps(self, localRev, count, globalRev, individualRev):
        self._oprot.writeMessageBegin('fetchOps', 1, self._seqid)
        args = fetchOps_args(localRev = localRev, count = count, globalRev = globalRev, individualRev = individualRev)
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()
        return self.recv_fetchOps()

    def recv_fetchOps(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == 3:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = fetchOps_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TApplicationException(5, "fetchOps failed: unknown result")


class TApplicationException(Exception):
    """Application level thrift exceptions."""

    UNKNOWN = 0
    if (2, 6, 0) <= sys.version_info < (3, 0):
        def _get_message(self):
            return self._message

        def _set_message(self, message):
            self._message = message
        message = property(_get_message, _set_message)

    def __init__(self, type=UNKNOWN, message=None):
        Exception.__init__(self, message)
        self.message = message
        self.type = type

    def __str__(self):
        if self.message:
            return self.message
        elif self.type == 1:
            return 'Unknown method'
        elif self.type == 2:
            return 'Invalid message type'
        elif self.type == 3:
            return 'Wrong method name'
        elif self.type == 4:
            return 'Bad sequence ID'
        elif self.type == 5:
            return 'Missing result'
        elif self.type == 6:
            return 'Internal error'
        elif self.type == 7:
            return 'Protocol error'
        elif self.type == 8:
            return 'Invalid transform'
        elif self.type == 9:
            return 'Invalid protocol'
        elif self.type == 10:
            return 'Unsupported client type'
        else:
            return 'Default (unknown) TApplicationException'

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 11:
                    self.message = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 8:
                    self.type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('TApplicationException')
        if self.message is not None:
            oprot.writeFieldBegin('message', 11, 1)
            oprot.writeString(self.message)
            oprot.writeFieldEnd()
        if self.type is not None:
            oprot.writeFieldBegin('type', 8, 2)
            oprot.writeI32(self.type)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class Location(object):

    thrift_spec = (
    None,  # 0
    (1, 11, 'title', 'UTF8', None, ),  # 1
    (2, 11, 'address', 'UTF8', None, ),  # 2
    (3, 4, 'latitude', None, None, ),  # 3
    (4, 4, 'longitude', None, None, ),  # 4
    (5, 11, 'phone', 'UTF8', None, ),  # 5
    )

    def __init__(self, title=None, address=None, latitude=None, longitude=None, phone=None,):
        self.title = title
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.phone = phone

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 11:
                    self.title = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 11:
                    self.address = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 4:
                    self.latitude = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == 4:
                    self.longitude = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == 11:
                    self.phone = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Location')
        if self.title is not None:
            oprot.writeFieldBegin('title', 11, 1)
            oprot.writeString(self.title.encode('utf-8') if sys.version_info[0] == 2 else self.title)
            oprot.writeFieldEnd()
        if self.address is not None:
            oprot.writeFieldBegin('address', 11, 2)
            oprot.writeString(self.address.encode('utf-8') if sys.version_info[0] == 2 else self.address)
            oprot.writeFieldEnd()
        if self.latitude is not None:
            oprot.writeFieldBegin('latitude', 4, 3)
            oprot.writeDouble(self.latitude)
            oprot.writeFieldEnd()
        if self.longitude is not None:
            oprot.writeFieldBegin('longitude', 4, 4)
            oprot.writeDouble(self.longitude)
            oprot.writeFieldEnd()
        if self.phone is not None:
            oprot.writeFieldBegin('phone', 11, 5)
            oprot.writeString(self.phone.encode('utf-8') if sys.version_info[0] == 2 else self.phone)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class Message(object):

    thrift_spec = (
    None,  # 0
    (1, 11, '_from', 'UTF8', None, ),  # 1
    (2, 11, 'to', 'UTF8', None, ),  # 2
    (3, 8, 'toType', None, None, ),  # 3
    (4, 11, 'id', 'UTF8', None, ),  # 4
    (5, 10, 'createdTime', None, None, ),  # 5
    (6, 10, 'deliveredTime', None, None, ),  # 6
    None,  # 7
    None,  # 8
    None,  # 9
    (10, 11, 'text', 'UTF8', None, ),  # 10
    (11, 12, 'location', [Location, None], None, ),  # 11
    None,  # 12
    None,  # 13
    (14, 2, 'hasContent', None, None, ),  # 14
    (15, 8, 'contentType', None, None, ),  # 15
    None,  # 16
    (17, 11, 'contentPreview', 'BINARY', None, ),  # 17
    (18, 13, 'contentMetadata', (11, 'UTF8', 11, 'UTF8', False), None, ),  # 18
    (19, 3, 'sessionId', None, None, ),  # 19
    (20, 15, 'chunks', (11, 'BINARY', False), None, ),  # 20
    (21, 11, 'relatedMessageId', 'UTF8', None, ),  # 21
    (22, 8, 'messageRelationType', None, None, ),  # 22
    (23, 10, 'readCount', None, None, ),  # 23
    (24, 8, 'relatedMessageServiceCode', None, None, ),  # 24
    )

    def __init__(self, _from=None, to=None, toType=None, id=None, createdTime=None, deliveredTime=None, text=None, location=None, hasContent=None, contentType=None, contentPreview=None, contentMetadata=None, sessionId=None, chunks=None, relatedMessageId=None, messageRelationType=None, readCount=None, relatedMessageServiceCode=None,):
        self._from = _from
        self.to = to
        self.toType = toType
        self.id = id
        self.createdTime = createdTime
        self.deliveredTime = deliveredTime
        self.text = text
        self.location = location
        self.hasContent = hasContent
        self.contentType = contentType
        self.contentPreview = contentPreview
        self.contentMetadata = contentMetadata
        self.sessionId = sessionId
        self.chunks = chunks
        self.relatedMessageId = relatedMessageId
        self.messageRelationType = messageRelationType
        self.readCount = readCount
        self.relatedMessageServiceCode = relatedMessageServiceCode

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 11:
                    self._from = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 11:
                    self.to = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 8:
                    self.toType = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == 11:
                    self.id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == 10:
                    self.createdTime = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == 10:
                    self.deliveredTime = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 10:
                if ftype == 11:
                    self.text = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 11:
                if ftype == 12:
                    self.location = Location()
                    self.location.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 14:
                if ftype == 2:
                    self.hasContent = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 15:
                if ftype == 8:
                    self.contentType = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 17:
                if ftype == 11:
                    self.contentPreview = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 18:
                if ftype == 13:
                    self.contentMetadata = {}
                    (_ktype277, _vtype278, _size276) = iprot.readMapBegin()
                    for _i280 in range(_size276):
                        _key281 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val282 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.contentMetadata[_key281] = _val282
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 19:
                if ftype == 3:
                    self.sessionId = iprot.readByte()
                else:
                    iprot.skip(ftype)
            elif fid == 20:
                if ftype == 15:
                    self.chunks = []
                    (_etype286, _size283) = iprot.readListBegin()
                    for _i287 in range(_size283):
                        _elem288 = iprot.readBinary()
                        self.chunks.append(_elem288)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 21:
                if ftype == 11:
                    self.relatedMessageId = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 22:
                if ftype == 8:
                    self.messageRelationType = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 23:
                if ftype == 10:
                    self.readCount = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 24:
                if ftype == 8:
                    self.relatedMessageServiceCode = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Message')
        if self._from is not None:
            oprot.writeFieldBegin('_from', 11, 1)
            oprot.writeString(self._from.encode('utf-8') if sys.version_info[0] == 2 else self._from)
            oprot.writeFieldEnd()
        if self.to is not None:
            oprot.writeFieldBegin('to', 11, 2)
            oprot.writeString(self.to.encode('utf-8') if sys.version_info[0] == 2 else self.to)
            oprot.writeFieldEnd()
        if self.toType is not None:
            oprot.writeFieldBegin('toType', 8, 3)
            oprot.writeI32(self.toType)
            oprot.writeFieldEnd()
        if self.id is not None:
            oprot.writeFieldBegin('id', 11, 4)
            oprot.writeString(self.id.encode('utf-8') if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        if self.createdTime is not None:
            oprot.writeFieldBegin('createdTime', 10, 5)
            oprot.writeI64(self.createdTime)
            oprot.writeFieldEnd()
        if self.deliveredTime is not None:
            oprot.writeFieldBegin('deliveredTime', 10, 6)
            oprot.writeI64(self.deliveredTime)
            oprot.writeFieldEnd()
        if self.text is not None:
            oprot.writeFieldBegin('text', 11, 10)
            oprot.writeString(self.text.encode('utf-8') if sys.version_info[0] == 2 else self.text)
            oprot.writeFieldEnd()
        if self.location is not None:
            oprot.writeFieldBegin('location', 12, 11)
            self.location.write(oprot)
            oprot.writeFieldEnd()
        if self.hasContent is not None:
            oprot.writeFieldBegin('hasContent', 2, 14)
            oprot.writeBool(self.hasContent)
            oprot.writeFieldEnd()
        if self.contentType is not None:
            oprot.writeFieldBegin('contentType', 8, 15)
            oprot.writeI32(self.contentType)
            oprot.writeFieldEnd()
        if self.contentPreview is not None:
            oprot.writeFieldBegin('contentPreview', 11, 17)
            oprot.writeBinary(self.contentPreview)
            oprot.writeFieldEnd()
        if self.contentMetadata is not None:
            oprot.writeFieldBegin('contentMetadata', 13, 18)
            oprot.writeMapBegin(11, 11, len(self.contentMetadata))
            for kiter289, viter290 in self.contentMetadata.items():
                oprot.writeString(kiter289.encode('utf-8') if sys.version_info[0] == 2 else kiter289)
                oprot.writeString(viter290.encode('utf-8') if sys.version_info[0] == 2 else viter290)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.sessionId is not None:
            oprot.writeFieldBegin('sessionId', 3, 19)
            oprot.writeByte(self.sessionId)
            oprot.writeFieldEnd()
        if self.chunks is not None:
            oprot.writeFieldBegin('chunks', 15, 20)
            oprot.writeListBegin(11, len(self.chunks))
            for iter291 in self.chunks:
                oprot.writeBinary(iter291)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.relatedMessageId is not None:
            oprot.writeFieldBegin('relatedMessageId', 11, 21)
            oprot.writeString(self.relatedMessageId.encode('utf-8') if sys.version_info[0] == 2 else self.relatedMessageId)
            oprot.writeFieldEnd()
        if self.messageRelationType is not None:
            oprot.writeFieldBegin('messageRelationType', 8, 22)
            oprot.writeI32(self.messageRelationType)
            oprot.writeFieldEnd()
        if self.readCount is not None:
            oprot.writeFieldBegin('readCount', 10, 23)
            oprot.writeI64(self.readCount)
            oprot.writeFieldEnd()
        if self.relatedMessageServiceCode is not None:
            oprot.writeFieldBegin('relatedMessageServiceCode', 8, 24)
            oprot.writeI32(self.relatedMessageServiceCode)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class Operation(object):

    thrift_spec = (
        None,  # 0
        (1, 10, 'revision', None, None, ),  # 1
        (2, 10, 'createdTime', None, None, ),  # 2
        (3, 8, 'type', None, None, ),  # 3
        (4, 8, 'reqSeq', None, None, ),  # 4
        (5, 11, 'checksum', 'UTF8', None, ),  # 5
        None,  # 6
        (7, 8, 'status', None, None, ),  # 7
        None,  # 8
        None,  # 9
        (10, 11, 'param1', 'UTF8', None, ),  # 10
        (11, 11, 'param2', 'UTF8', None, ),  # 11
        (12, 11, 'param3', 'UTF8', None, ),  # 12
        None,  # 13
        None,  # 14
        None,  # 15
        None,  # 16
        None,  # 17
        None,  # 18
        None,  # 19
        (20, 12, 'message', [Message, None], None, ),  # 20
    )

    def __init__(self, revision=None, createdTime=None, type=None, reqSeq=None, checksum=None, status=None, param1=None, param2=None, param3=None, message=None,):
        self.revision = revision
        self.createdTime = createdTime
        self.type = type
        self.reqSeq = reqSeq
        self.checksum = checksum
        self.status = status
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.message = message

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 10:
                    self.revision = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 10:
                    self.createdTime = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 8:
                    self.type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == 8:
                    self.reqSeq = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == 11:
                    self.checksum = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == 8:
                    self.status = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 10:
                if ftype == 11:
                    self.param1 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 11:
                if ftype == 11:
                    self.param2 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 12:
                if ftype == 11:
                    self.param3 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 20:
                if ftype == 12:
                    self.message = Message()
                    self.message.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Operation')
        if self.revision is not None:
            oprot.writeFieldBegin('revision', 10, 1)
            oprot.writeI64(self.revision)
            oprot.writeFieldEnd()
        if self.createdTime is not None:
            oprot.writeFieldBegin('createdTime', 10, 2)
            oprot.writeI64(self.createdTime)
            oprot.writeFieldEnd()
        if self.type is not None:
            oprot.writeFieldBegin('type', 8, 3)
            oprot.writeI32(self.type)
            oprot.writeFieldEnd()
        if self.reqSeq is not None:
            oprot.writeFieldBegin('reqSeq', 8, 4)
            oprot.writeI32(self.reqSeq)
            oprot.writeFieldEnd()
        if self.checksum is not None:
            oprot.writeFieldBegin('checksum', 11, 5)
            oprot.writeString(self.checksum.encode('utf-8') if sys.version_info[0] == 2 else self.checksum)
            oprot.writeFieldEnd()
        if self.status is not None:
            oprot.writeFieldBegin('status', 8, 7)
            oprot.writeI32(self.status)
            oprot.writeFieldEnd()
        if self.param1 is not None:
            oprot.writeFieldBegin('param1', 11, 10)
            oprot.writeString(self.param1.encode('utf-8') if sys.version_info[0] == 2 else self.param1)
            oprot.writeFieldEnd()
        if self.param2 is not None:
            oprot.writeFieldBegin('param2', 11, 11)
            oprot.writeString(self.param2.encode('utf-8') if sys.version_info[0] == 2 else self.param2)
            oprot.writeFieldEnd()
        if self.param3 is not None:
            oprot.writeFieldBegin('param3', 11, 12)
            oprot.writeString(self.param3.encode('utf-8') if sys.version_info[0] == 2 else self.param3)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', 12, 20)
            self.message.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class SyncParamMid(object):

    thrift_spec = (
    None,  # 0
    (1, 11, 'mid', 'UTF8', None, ),  # 1
    (2, 8, 'diff', None, None, ),  # 2
    (3, 10, 'revision', None, None, ),  # 3
    )

    def __init__(self, mid=None, diff=None, revision=None,):
        self.mid = mid
        self.diff = diff
        self.revision = revision

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 11:
                    self.mid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 8:
                    self.diff = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 10:
                    self.revision = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('SyncParamMid')
        if self.mid is not None:
            oprot.writeFieldBegin('mid', 11, 1)
            oprot.writeString(self.mid.encode('utf-8') if sys.version_info[0] == 2 else self.mid)
            oprot.writeFieldEnd()
        if self.diff is not None:
            oprot.writeFieldBegin('diff', 8, 2)
            oprot.writeI32(self.diff)
            oprot.writeFieldEnd()
        if self.revision is not None:
            oprot.writeFieldBegin('revision', 10, 3)
            oprot.writeI64(self.revision)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class SyncParamContact(object):

    thrift_spec = (
    None,  # 0
    (1, 12, 'syncParamMid', [SyncParamMid, None], None, ),  # 1
    (2, 8, 'contactStatus', None, None, ),  # 2
    )

    def __init__(self, syncParamMid=None, contactStatus=None,):
        self.syncParamMid = syncParamMid
        self.contactStatus = contactStatus

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 12:
                    self.syncParamMid = SyncParamMid()
                    self.syncParamMid.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 8:
                    self.contactStatus = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('SyncParamContact')
        if self.syncParamMid is not None:
            oprot.writeFieldBegin('syncParamMid', 12, 1)
            self.syncParamMid.write(oprot)
            oprot.writeFieldEnd()
        if self.contactStatus is not None:
            oprot.writeFieldBegin('contactStatus', 8, 2)
            oprot.writeI32(self.contactStatus)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class SyncRelations(object):

    thrift_spec = (
    None,  # 0
    (1, 2, 'syncAll', None, None, ),  # 1
    (2, 15, 'syncParamContact', (12, [SyncParamContact, None], False), None, ),  # 2
    (3, 15, 'syncParamMid', (12, [SyncParamMid, None], False), None, ),  # 3
    )

    def __init__(self, syncAll=None, syncParamContact=None, syncParamMid=None,):
        self.syncAll = syncAll
        self.syncParamContact = syncParamContact
        self.syncParamMid = syncParamMid

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 2:
                    self.syncAll = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 15:
                    self.syncParamContact = []
                    (_etype489, _size486) = iprot.readListBegin()
                    for _i490 in range(_size486):
                        _elem491 = SyncParamContact()
                        _elem491.read(iprot)
                        self.syncParamContact.append(_elem491)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 15:
                    self.syncParamMid = []
                    (_etype495, _size492) = iprot.readListBegin()
                    for _i496 in range(_size492):
                        _elem497 = SyncParamMid()
                        _elem497.read(iprot)
                        self.syncParamMid.append(_elem497)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('SyncRelations')
        if self.syncAll is not None:
            oprot.writeFieldBegin('syncAll', 2, 1)
            oprot.writeBool(self.syncAll)
            oprot.writeFieldEnd()
        if self.syncParamContact is not None:
            oprot.writeFieldBegin('syncParamContact', 15, 2)
            oprot.writeListBegin(12, len(self.syncParamContact))
            for iter498 in self.syncParamContact:
                iter498.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.syncParamMid is not None:
            oprot.writeFieldBegin('syncParamMid', 15, 3)
            oprot.writeListBegin(12, len(self.syncParamMid))
            for iter499 in self.syncParamMid:
                iter499.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class SyncScope(object):

    thrift_spec = (
    None,  # 0
    (1, 2, 'syncProfile', None, None, ),  # 1
    (2, 2, 'syncSettings', None, None, ),  # 2
    (3, 2, 'syncSticker', None, None, ),  # 3
    (4, 2, 'syncThemeShop', None, None, ),  # 4
    None,  # 5
    None,  # 6
    None,  # 7
    None,  # 8
    None,  # 9
    (10, 12, 'contact', [SyncRelations, None], None, ),  # 10
    (11, 12, 'group', [SyncRelations, None], None, ),  # 11
    (12, 12, 'room', [SyncRelations, None], None, ),  # 12
    (13, 12, 'chat', [SyncRelations, None], None, ),  # 13
    )

    def __init__(self, syncProfile=None, syncSettings=None, syncSticker=None, syncThemeShop=None, contact=None, group=None, room=None, chat=None,):
        self.syncProfile = syncProfile
        self.syncSettings = syncSettings
        self.syncSticker = syncSticker
        self.syncThemeShop = syncThemeShop
        self.contact = contact
        self.group = group
        self.room = room
        self.chat = chat

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 2:
                    self.syncProfile = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 2:
                    self.syncSettings = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 2:
                    self.syncSticker = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == 2:
                    self.syncThemeShop = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 10:
                if ftype == 12:
                    self.contact = SyncRelations()
                    self.contact.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 11:
                if ftype == 12:
                    self.group = SyncRelations()
                    self.group.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 12:
                if ftype == 12:
                    self.room = SyncRelations()
                    self.room.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 13:
                if ftype == 12:
                    self.chat = SyncRelations()
                    self.chat.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('SyncScope')
        if self.syncProfile is not None:
            oprot.writeFieldBegin('syncProfile', 2, 1)
            oprot.writeBool(self.syncProfile)
            oprot.writeFieldEnd()
        if self.syncSettings is not None:
            oprot.writeFieldBegin('syncSettings', 2, 2)
            oprot.writeBool(self.syncSettings)
            oprot.writeFieldEnd()
        if self.syncSticker is not None:
            oprot.writeFieldBegin('syncSticker', 2, 3)
            oprot.writeBool(self.syncSticker)
            oprot.writeFieldEnd()
        if self.syncThemeShop is not None:
            oprot.writeFieldBegin('syncThemeShop', 2, 4)
            oprot.writeBool(self.syncThemeShop)
            oprot.writeFieldEnd()
        if self.contact is not None:
            oprot.writeFieldBegin('contact', 12, 10)
            self.contact.write(oprot)
            oprot.writeFieldEnd()
        if self.group is not None:
            oprot.writeFieldBegin('group', 12, 11)
            self.group.write(oprot)
            oprot.writeFieldEnd()
        if self.room is not None:
            oprot.writeFieldBegin('room', 12, 12)
            self.room.write(oprot)
            oprot.writeFieldEnd()
        if self.chat is not None:
            oprot.writeFieldBegin('chat', 12, 13)
            self.chat.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class TalkException(Exception):

    thrift_spec = (
    None,  # 0
    (1, 8, 'code', None, None, ),  # 1
    (2, 11, 'reason', 'UTF8', None, ),  # 2
    (3, 13, 'parameterMap', (11, 'UTF8', 11, 'UTF8', False), None, ),  # 3
    )

    def __init__(self, code=None, reason=None, parameterMap=None,):
        self.code = code
        self.reason = reason
        self.parameterMap = parameterMap

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 8:
                    self.code = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 11:
                    self.reason = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 13:
                    self.parameterMap = {}
                    (_ktype912, _vtype913, _size911) = iprot.readMapBegin()
                    for _i915 in range(_size911):
                        _key916 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val917 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.parameterMap[_key916] = _val917
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TalkException')
        if self.code is not None:
            oprot.writeFieldBegin('code', 8, 1)
            oprot.writeI32(self.code)
            oprot.writeFieldEnd()
        if self.reason is not None:
            oprot.writeFieldBegin('reason', 11, 2)
            oprot.writeString(self.reason.encode('utf-8') if sys.version_info[0] == 2 else self.reason)
            oprot.writeFieldEnd()
        if self.parameterMap is not None:
            oprot.writeFieldBegin('parameterMap', 13, 3)
            oprot.writeMapBegin(11, 11, len(self.parameterMap))
            for kiter918, viter919 in self.parameterMap.items():
                oprot.writeString(kiter918.encode('utf-8') if sys.version_info[0] == 2 else kiter918)
                oprot.writeString(viter919.encode('utf-8') if sys.version_info[0] == 2 else viter919)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ShouldSyncException(Exception):

    thrift_spec = (
    None,  # 0
    (1, 10, 'syncOpRevision', None, None, ),  # 1
    (2, 12, 'syncScope', [SyncScope, None], None, ),  # 2
    (3, 8, 'syncReason', None, None, ),  # 3
    (4, 11, 'message', 'UTF8', None, ),  # 4
    )

    def __init__(self, syncOpRevision=None, syncScope=None, syncReason=None, message=None,):
        self.syncOpRevision = syncOpRevision
        self.syncScope = syncScope
        self.syncReason = syncReason
        self.message = message

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 1:
                if ftype == 10:
                    self.syncOpRevision = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == 12:
                    self.syncScope = SyncScope()
                    self.syncScope.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 8:
                    self.syncReason = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == 11:
                    self.message = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('ShouldSyncException')
        if self.syncOpRevision is not None:
            oprot.writeFieldBegin('syncOpRevision', 10, 1)
            oprot.writeI64(self.syncOpRevision)
            oprot.writeFieldEnd()
        if self.syncScope is not None:
            oprot.writeFieldBegin('syncScope', 12, 2)
            self.syncScope.write(oprot)
            oprot.writeFieldEnd()
        if self.syncReason is not None:
            oprot.writeFieldBegin('syncReason', 8, 3)
            oprot.writeI32(self.syncReason)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', 11, 4)
            oprot.writeString(self.message.encode('utf-8') if sys.version_info[0] == 2 else self.message)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class getLastOpRevision_args(object):

    thrift_spec = ()

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('getLastOpRevision_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class getLastOpRevision_result(object):

    thrift_spec = (
    (0, 10, 'success', None, None, ),  # 0
    (1, 12, 'e', [TalkException, None], None, ),  # 1
    )

    def __init__(self, success=None, e=None,):
        self.success = success
        self.e = e

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 0:
                if ftype == 10:
                    self.success = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == 12:
                    self.e = TalkException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('getLastOpRevision_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', 10, 0)
            oprot.writeI64(self.success)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', 12, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class fetchOperations_args(object):

    thrift_spec = (
    None,  # 0
    None,  # 1
    (2, 10, 'localRev', None, None, ),  # 2
    (3, 8, 'count', None, None, ),  # 3
    )

    def __init__(self, localRev=None, count=None,):
        self.localRev = localRev
        self.count = count

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 2:
                if ftype == 10:
                    self.localRev = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 8:
                    self.count = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('fetchOperations_args')
        if self.localRev is not None:
            oprot.writeFieldBegin('localRev', 10, 2)
            oprot.writeI64(self.localRev)
            oprot.writeFieldEnd()
        if self.count is not None:
            oprot.writeFieldBegin('count', 8, 3)
            oprot.writeI32(self.count)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class fetchOperations_result(object):

    thrift_spec = (
        (0, 15, 'success', (12, [Operation, None], False), None, ),  # 0
        (1, 12, 'e', [ShouldSyncException, None], None, ),  # 1
    )

    def __init__(self, success=None, e=None,):
        self.success = success
        self.e = e

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 0:
                if ftype == 15:
                    self.success = []
                    (_etype1492, _size1489) = iprot.readListBegin()
                    for _i1493 in range(_size1489):
                        _elem1494 = Operation()
                        _elem1494.read(iprot)
                        self.success.append(_elem1494)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == 12:
                    self.e = ShouldSyncException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('fetchOperations_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', 15, 0)
            oprot.writeListBegin(12, len(self.success))
            for iter1495 in self.success:
                iter1495.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', 12, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class fetchOps_args(object):

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, 10, 'localRev', None, None, ),  # 2
        (3, 8, 'count', None, None, ),  # 3
        (4, 10, 'globalRev', None, None, ),  # 4
        (5, 10, 'individualRev', None, None, ),  # 5
    )

    def __init__(self, localRev=None, count=None, globalRev=None, individualRev=None,):
        self.localRev = localRev
        self.count = count
        self.globalRev = globalRev
        self.individualRev = individualRev

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 2:
                if ftype == 10:
                    self.localRev = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == 8:
                    self.count = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == 10:
                    self.globalRev = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == 10:
                    self.individualRev = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('fetchOps_args')
        if self.localRev is not None:
            oprot.writeFieldBegin('localRev', 10, 2)
            oprot.writeI64(self.localRev)
            oprot.writeFieldEnd()
        if self.count is not None:
            oprot.writeFieldBegin('count', 8, 3)
            oprot.writeI32(self.count)
            oprot.writeFieldEnd()
        if self.globalRev is not None:
            oprot.writeFieldBegin('globalRev', 10, 4)
            oprot.writeI64(self.globalRev)
            oprot.writeFieldEnd()
        if self.individualRev is not None:
            oprot.writeFieldBegin('individualRev', 10, 5)
            oprot.writeI64(self.individualRev)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

class fetchOps_result(object):

    thrift_spec = (
    (0, 15, 'success', (12, [Operation, None], False), None, ),  # 0
    (1, 12, 'e', [ShouldSyncException, None], None, ),  # 1
    )

    def __init__(self, success=None, e=None,):
        self.success = success
        self.e = e

    def read(self, iprot):
        if iprot._fast_decode is not None and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            if fid == 0:
                if ftype == 15:
                    self.success = []
                    (_etype1499, _size1496) = iprot.readListBegin()
                    for _i1500 in range(_size1496):
                        _elem1501 = Operation()
                        _elem1501.read(iprot)
                        self.success.append(_elem1501)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == 12:
                    self.e = ShouldSyncException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('fetchOps_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', 15, 0)
            oprot.writeListBegin(12, len(self.success))
            for iter1502 in self.success:
                iter1502.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', 12, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()