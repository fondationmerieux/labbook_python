# -*- coding:utf-8 -*-


class Logs:

    @staticmethod
    def alerte():
        import inspect

        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return "ALERTE " + info.filename + ' ' + info.function + ' line ' + str(info.lineno)

    @staticmethod
    def fileline():
        import inspect

        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return info.filename + ' ' + info.function + ' line ' + str(info.lineno)
