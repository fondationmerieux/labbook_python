# -*- coding:utf-8 -*-


# Generic exception class
class GenericException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
