# -*- coding:utf-8 -*-
import datetime
import inspect


class Logs:

    @staticmethod
    def alert():
        """
        Same as fileline, prefixed with ALERT, for errors that need attention.
        """
        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return "ALERT " + info.filename + ' ' + info.function + ' line ' + str(info.lineno)

    @staticmethod
    def fileline():
        """
        Return 'file function line N' of the caller, the prefix of every log line.
        inspect.stack() reads the whole call stack, so it costs a little at each call.
        """
        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return info.filename + ' ' + info.function + ' line ' + str(info.lineno)

    @staticmethod
    def clean(value):
        """
        Make a user-supplied value safe to write in a log line.
        Line breaks and tabs are turned into spaces so nobody can forge an extra
        log entry by submitting a crafted value.
        """
        return str(value).replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')

    @staticmethod
    def log_script(message):
        """
        Print a message with the current date and time, for the scripts run outside Flask.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} : {message}")
