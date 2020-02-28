# -*- coding:utf-8 -*-
from app.exception.GenericException import GenericException


class DBException(GenericException):
    def __init__(self, msg):
        super(self.__class__, self).__init__("DBException: " + msg)
