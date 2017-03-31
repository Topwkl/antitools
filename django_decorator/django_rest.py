#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by ChenXin on 2017/3/23
from collections import namedtuple


def restful(para, result):
    def wrapping(task):
        def decorator(*a, **k):
            _args = list(a)
            cls = _args.pop(0)
            request = _args.pop(0)

            paras = JsonDict(**para)

            results = JsonDict(**result)

            info = JsonDict({"msg": "",
                             "status": -1})

            return task(cls, request, paras, results, info, *_args, **k)

        return decorator

    return wrapping


class RField(object):
    def __init__(self, field_name, verbose_name=None, field_type="str", null=True, blank=True, validators=None):
        self._field_name = field_name,
        self._verbose_name = verbose_name if verbose_name else field_name
        self._field_type = field_type
        self._null = null
        self._blank = blank
        self._validators = validators

        self._value = None
        self._convert = {"str": str,
                         "int": int}

    @property
    def value(self):
        return self._convert[self._field_type](self._value)

    @value.setter
    def value(self, value):
        print 1
        if not self._validators:
            self._value = value
        else:
            if self._validators(value):
                self._value = value
            else:
                raise ValueError("%s value error", self._field_name)

    # def __set__(self, instance, value):
    #     print 1
    #
    #     self.value = value
    #
    # def __get__(self, instance, owner):
    #     print 2
    #     return self.value


class JsonDict(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' objectg has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


@restful({"username": "",
          "password": ""},
         {"result": ""})
def test(self, request, para, result, info):
    print self
    print request
    print dir(result)
    print info
    import json
    print json.dumps(para)
    print para.username


class Test(object):
    def __init__(self):
        self.username = RField("username", validators=lambda x: True if x < 20 else False)


if __name__ == "__main__":
    # test("self", {"username": "username", "password": "password"}
    t = Test()
    t.username = 100
    print t.username
    # print type(b.a)
    # field = RField("username", validators=lambda x: True if x < 20 else False)
    # field = 10
    # print field._field_name
    # print type(field)
