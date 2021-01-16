# -*- coding: UTF-8 -*-

"""
    ~~~~~~~~~~~
    Simple linebot
    created by: 
    ©finbot alfino~nh
    ~~~~~~~~~~~
"""
from functools import wraps
from .lib.curve.ttypes import OpType, Operation, ShouldSyncException, TalkException
from .utility import config
from .utility.utils import ThreadPool
import line

import logging
import traceback, threading

log = logging.getLogger(__name__)


MAX_REV= 50
version = config.VERSION

class Poll():
    OpInterrupt = {}
    server = config
    client = None
    pool = None

    def __init__(self, client, workers=2, threaded=False):
        if not isinstance(client, line.LineClient):
            raise Exception('You need to set LineClient instance to initialize Poll')

        self.client: line.LineClient = client
        self.func_handler : list = []
        self.Opinterrupts: list = []
        self.workers = workers
        self.pool = ThreadPool(num_threads=self.workers)
        self.threaded = threaded
        self.next_step_handlers = {}
        self.next_step_saver = None

    def fetchOperations(self, revision, count):
        return self.client.line['poll'].fetchOperations(revision, count)

    def fetchOps(self, revision, count: int=10, globalRev: int=0, individualRev: int=0):
        return self.client.line['poll'].fetchOps(revision, count, globalRev, individualRev)

    def getLastOpRevision(self):
        return self.client.line['poll'].getLastOpRevision()

    def streams(self, op, threading):
        try:
            if threading:
                _td = threading.Thread(target=self.OpInterrupt[op.type](op))
                _td.daemon = False
                _td.start()
            else:
                self.OpInterrupt[op.type](op)
        except Exception:
            log.error(str(traceback.format_exc))

    def addOpInterruptWithDict(self, OpInterruptDict):
        self.OpInterrupt.update(OpInterruptDict)

    def addOpInterrupt(self, OperationType, DisposeFunc):
        self.OpInterrupt[OperationType] = DisposeFunc

    def setRevision(self, revision):
        self.client.revision = max(revision, self.client.revision)

    def singleTrace(self):
        try:
            operations = self.fetchOperations(self.client.revision, MAX_REV)
        except EOFError:
            return
        except KeyboardInterrupt:
            sys.exit()
        except ShouldSyncException:
            return []
        if operations is None:
            return []
        else:
            return operations

    def handler(self, types, *arg, **kwg):
        def decorator(func):
            @wraps(func)
            def wraper(self, *args, **kwgs):
                func(*args, **kwgs)
                return True

            data = {
                func:arg,
                "data":kwg
            }
            self.func_handler.append(data)
            return wraper, self.Opinterrupts.append({types:func}), True
        return decorator

    def _exec(self, ops, func):
        msg = ops.message
        for i in range(len(self.func_handler)):
            if func in self.func_handler[i]:
                if len(self.func_handler[i][func]) < 1:
                    self.do_job(c=i, ops=ops)
                else:
                    if self.func_handler[i][func][0] != None:
                        if self.func_handler[i][func][0](msg):
                            self.do_job(c=i, ops=ops)

    def do_job(self, ops, c):
        if self.threaded:
            self.pool.put(self.Opinterrupts[c][ops.type], ops)
        else:
            self.Opinterrupts[c][ops.type](ops)
			
    def start(self):
        while True:
            self.trace()

    def trace(self):
        try:
            ops = self.fetchOps(self.client.revision)
            for op in ops:
                if self.func_handler:
                    for i in range(len(self.Opinterrupts)):
                        if list(self.Opinterrupts[i].values())[0] in self.func_handler[i]:
                            if op.type in self.Opinterrupts[i].keys():
                                self._exec(op, self.Opinterrupts[i][op.type])
                            self.setRevision(op.revision)
        except EOFError:
            pass
        except Exception:
            log.error(traceback.format_exc())