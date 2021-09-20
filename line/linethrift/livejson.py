import os
import json
import warnings

try:
    from typing import ( #alias from collections.abc
        MutableMapping,
        MutableSequence,
    )
except ImportError:
    from collections import (
        MutableMapping,
        MutableSequence,
    )

warnings.filterwarnings("once", category=DeprecationWarning)

def _initfile(path, data="dict"):
    data = {} if data.lower() == "dict" else []
    if not os.path.exists(path):
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            raise IOError(
                ("Could not initialize empty JSON file in non-existant "
                 "directory '{}'").format(os.path.dirname(path))
            )
        with open(path, "w") as f:
            json.dump(data, f)
        return True
    elif os.path.getsize(path) == 0:
        with open(path, "w") as f:
            json.dump(data, f)
    else:
        return False


class _ObjectBase(object):
    def __getitem__(self, key):
        out = self.data[key]

        if isinstance(out, (list, dict)):
            pathInData = self.pathInData if hasattr(self, "pathInData") else []
            newPathInData = pathInData + [key]
            toplevel = self.base if hasattr(self, "base") else self
            nestClass = _NestedList if isinstance(out, list) else _NestedDict
            return nestClass(toplevel, newPathInData)
        else:
            return out

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def _checkType(self, key):
        pass


class _NestedBase(_ObjectBase):
    def __init__(self, fileobj, pathToThis):
        self.pathInData = pathToThis
        self.base = fileobj

    @property
    def data(self):
        d = self.base.data
        for i in self.pathInData:
            d = d[i]
        return d

    def __setitem__(self, key, value):
        self._checkType(key)
        data = self.base.data
        d = data
        for i in self.pathInData:
            d = d[i]
        d[key] = value
        self.base.data = data

    def __delitem__(self, key):
        data = self.base.data
        d = data
        for i in self.pathInData:
            d = d[i]
        del d[key]
        self.base.data = data


class _NestedDict(_NestedBase, MutableMapping):
    def __iter__(self):
        return iter(self.data)

    def _checkType(self, key):
        if not isinstance(key, str):
            raise TypeError("JSON only supports strings for keys, not '{}'. {}"
                            .format(type(key).__name__, "Try using a list for"
                                    " storing numeric keys" if
                                    isinstance(key, int) else ""))


class _NestedList(_NestedBase, MutableSequence):
    def insert(self, index, value):
        data = self.base.data
        d = data
        for i in self.pathInData:
            d = d[i]
        d.insert(index, value)
        self.base.data = data

class _BaseFile(_ObjectBase):
    def __init__(self, path, pretty=False, sort_keys=False):
        self.path = path
        self.pretty = pretty
        self.sort_keys = sort_keys
        self.indent = 2

        _initfile(self.path,
                  "list" if isinstance(self, ListFile) else "dict")

    def _data(self):
        if self.is_caching:
            return self.cache
        with open(self.path, "r") as f:
            return json.load(f)

    @property
    def data(self):
        self._updateType()
        return self._data()

    @data.setter
    def data(self, data):
        if self.is_caching:
            self.cache = data
        else:
            fcontents = self.file_contents
            with open(self.path, "w") as f:
                try:
                    indent = self.indent if self.pretty else None
                    json.dump(data, f, sort_keys=self.sort_keys, indent=indent)
                except Exception as e:
                    f.seek(0)
                    f.truncate()
                    f.write(fcontents)
                    raise e
        self._updateType()

    def __setitem__(self, key, value):
        self._checkType(key)
        data = self.data
        data[key] = value
        self.data = data

    def __delitem__(self, key):
        data = self.data
        del data[key]
        self.data = data

    def _updateType(self):
        data = self._data()
        if isinstance(data, dict) and isinstance(self, ListFile):
            self.__class__ = DictFile
        elif isinstance(data, list) and isinstance(self, DictFile):
            self.__class__ = ListFile

    def set_data(self, data):
        warnings.warn(
            "set_data is deprecated; please set .data instead.",
            DeprecationWarning
        )
        self.data = data

    def remove(self):
        os.remove(self.path)

    @property
    def file_contents(self):
        with open(self.path, "r") as f:
            return f.read()

    @property
    def is_caching(self):
        return hasattr(self, "cache")

    def __enter__(self):
        self.cache = self.data
        return self  # This enables using "as"

    def __exit__(self, *args):
        with open(self.path, "w") as f:
            indent = self.indent if self.pretty else None
            json.dump(self.cache, f, sort_keys=self.sort_keys, indent=indent)
        del self.cache

class DictFile(_BaseFile, MutableMapping):
    def __iter__(self):
        return iter(self.data)

    def _checkType(self, key):
        if not isinstance(key, str):
            raise TypeError("JSON only supports strings for keys, not '{}'. {}"
                            .format(type(key).__name__, "Try using a list for"
                                    " storing numeric keys" if
                                    isinstance(key, int) else ""))

class ListFile(_BaseFile, MutableSequence):
    def insert(self, index, value):
        data = self.data
        data.insert(index, value)
        self.data = data

    def clear(self):
        self.data = []

class File(object):

    def __init__(self, path, pretty=False, sort_keys=True, indent=2):
        self.path = path
        self.pretty = pretty
        self.sort_keys = sort_keys
        self.indent = indent

        _initfile(self.path)

        with open(self.path, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            self.__class__ = DictFile
        elif isinstance(data, list):
            self.__class__ = ListFile

    @staticmethod
    def with_data(path, data, *args, **kwargs):
        if isinstance(data, str):
            data = json.loads(data)

        if os.path.exists(path):
            raise ValueError("File exists, not overwriting data. Set the "
                             "'data' attribute on a normally-initialized "
                             "'livejson.File' instance if you really "
                             "want to do this.")
        else:
            f = File(path, *args, **kwargs)
            f.data = data
            return f

class MergeJSON(object):
    def __init__(self, base, data):
        for item in data:
            if item not in base:
               base[item] = data[item]


Database = File
CreateDatabase = MergeJSON
ListDatabase = ListFile
DictDatabase = DictFile