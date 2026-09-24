# -*- coding:utf-8 -*-
import inspect


class Logs:

    @staticmethod
    def alert():
        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return "ALERT " + info.filename + ' ' + info.function + ' line ' + str(info.lineno)

    @staticmethod
    def fileline():
        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return info.filename + ' ' + info.function + ' line ' + str(info.lineno)
