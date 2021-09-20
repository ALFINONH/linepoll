
import threading, sys, traceback

MAX_REV = 50

class Poll:

    OpInterrupt = {}

    def __init__(self):
        pass

    def __fetchOperations(self, revision, count: int=100):
        return self.poll.fetchOperations(revision, count)

    def __fetchOps(self, revision, count: int=10, globalRev: int=0, individualRev: int=0):
        return self.poll.fetchOps(revision, count, globalRev, individualRev)

    def __getLastOpRevision(self):
        return self.poll.getLastOpRevision()

    def __execute(self, op, func):
        try:
            func(op, self)
        except Exception as e:
            traceback.format_exc()

    def addOpInterruptWithDict(self, OpInterruptDict):
        self.OpInterrupt.update(OpInterruptDict)

    def addOpInterrupt(self, OperationType, DisposeFunc):
        self.OpInterrupt[OperationType] = DisposeFunc

    def setRevision(self, revision):
        self.revision = max(revision, self.revision)

    def trace(self, func, _threading=True):
        while True:
            ops = self.__fetchOps(self.revision)
            for op in ops:
                if op.type != 0 and op.type != -1:
                    self.setRevision(op.revision)
                    if _threading:
                        _td = threading.Thread(target=self.__execute, args=(op, func))
                        _td.daemon = True
                        _td.start()
                    else:
                        self.__execute(op, func)

    def singleTrace(self):
        try:
            operations = self.__fetchOperations(self.revision, count =MAX_REV)
        except EOFError:
            return
        except KeyboardInterrupt:
            sys.exit()
        except self._func.ShouldSyncException:
            return []
        if operations is None:
            return []
        else:
            return operations