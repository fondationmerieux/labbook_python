# -*- coding:utf-8 -*-
import datetime


class Logs:

    @staticmethod
    def alert():
        import inspect

        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return "ALERT " + info.filename + ' ' + info.function + ' line ' + str(info.lineno)

    @staticmethod
    def fileline():
        import inspect

        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return info.filename + ' ' + info.function + ' line ' + str(info.lineno)

    @staticmethod
    def log_script(message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line_number = Logs.fileline()
        print(f"{timestamp} : {message}")
