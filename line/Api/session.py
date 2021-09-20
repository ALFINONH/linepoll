from requests.sessions import Session
from requests.adapters import DEFAULT_POOLSIZE, HTTPAdapter

import concurrent.futures
import functools
import logging, json, urllib.parse, shutil, os

def wrap(self, sup, background_callback, *args_, **kwargs_):
    resp = sup(*args_, **kwargs_)
    return background_callback(self, resp) or resp

class LinepollSession(Session):
    def __init__(self, executor=None, max_workers=3, session=None,
                 adapter_kwargs=None, *args, **kwargs):
        _adapter_kwargs = {}
        super(LinepollSession, self).__init__(*args, **kwargs)
        self._owned_executor = executor is None
        if executor is None:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
            if max_workers > DEFAULT_POOLSIZE:
                _adapter_kwargs.update({'pool_connections': max_workers,
                                        'pool_maxsize': max_workers})
        _adapter_kwargs.update(adapter_kwargs or {})

        if _adapter_kwargs:
            self.mount('https://', HTTPAdapter(**_adapter_kwargs))
            self.mount('http://', HTTPAdapter(**_adapter_kwargs))

        self.executor = executor
        self.session = session

    def request(self, *args, **kwargs):
        if self.session:
            func = self.session.request
        else:
            func = functools.partial(Session.request, self)

        background_callback = kwargs.pop('background_callback', None)

        if background_callback:
            logger = logging.getLogger(self.__class__.__name__)
            logger.warning('`background_callback` is deprecated and will be '
                        'removed in 1.0, use `hooks` instead')
            func = functools.partial(wrap, self, func, background_callback)

        if isinstance(self.executor, concurrent.futures.ProcessPoolExecutor):
            try:
                dumps(func)
            except (TypeError, PickleError):
                raise RuntimeError(PICKLE_ERROR)

        return self.executor.submit(func, *args, **kwargs)

    def close(self):
        super(LinepollSession, self).close()
        if self._owned_executor:
            self.executor.shutdown()

    def get(self, url, **kwargs):
        return super(LinepollSession, self).get(url, **kwargs)

    def options(self, url, **kwargs):
        return super(LinepollSession, self).options(url, **kwargs)

    def head(self, url, **kwargs):
        return super(LinepollSession, self).head(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return super(LinepollSession, self).post(url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return super(LinepollSession, self).put(url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return super(LinepollSession, self).patch(url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return super(LinepollSession, self).delete(url, **kwargs)

class Server:

    def __init__(self):
        self._session = Session()
        self.headers = {}
        self.timelineHeaders = {}

    def additionalHeaders(self, source, newSource):
        headerList={}
        headerList.update(source)
        headerList.update(newSource)
        return headerList

    def urlEncode(self, url, path, params=[]):
        return url + path + '?' + urllib.parse.urlencode(params)

    def getJson(self, url, allowHeader=False):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            return json.loads(self._session.get(url, headers=self.headers).text)

    def optionsContent(self, url, headers=None, data=None):
        if headers is None:
            headers=self.headers

        return self._session.options(url, headers=headers, data=data)

    def postContent(self, url, headers=None, data=None, files=None):
        if headers is None:
            headers=self.headers

        return self._session.post(url, headers=headers, data=data, files=files)

    def getContent(self, url, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.get(url, headers=headers, stream=True)

    def deleteContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.delete(url, headers=headers, data=data)

    def putContent(self, url, headers=None, data=None):
        if headers is None:
            headers=self.headers

        return self._session.put(url, headers=headers, data=data)

    def saveFile(self, path, raw):
        with open(path, 'wb') as f:
            shutil.copyfileobj(raw, f)

    def deleteFile(self, path):
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False