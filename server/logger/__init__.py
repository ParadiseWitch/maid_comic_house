import datetime
import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

from setting import DOWNLOAD_PATH

logger: logging.Logger


class LogFilter:
    @staticmethod
    def info_filter(record):
        if record.levelname == 'INFO':
            return True
        return False

    @staticmethod
    def warning_filter(record):
        if record.levelname == 'WARNING':
            return True
        return False

    @staticmethod
    def error_filter(record):
        if record.levelname == 'ERROR':
            return True
        return False


class TimeLoggerRolloverHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backup_count=0, encoding=None, delay=False, utc=False):
        super(TimeLoggerRolloverHandler, self).__init__(filename, when, interval, backup_count, encoding, delay, utc)

    def doRollover(self):
        """
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]
        log_type = 'info' if self.level == 20 else 'error'
        dfn = f"my.{datetime.datetime.now().strftime('%Y%m%d')}.{log_type}.log"
        self.baseFilename = dfn
        if not self.delay:
            self.stream = self._open()
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:
                    addend = -3600
                else:
                    addend = 3600
                new_rollover_at += addend
        self.rolloverAt = new_rollover_at


logs_dir = '{}/logs'.format(DOWNLOAD_PATH)
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)8s | %(module)s | [%(filename)s:%(lineno)d]: %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

# TODO '{}/{}/error.log' 不能分日期文件夹
log_error_file = '{}/{}.error.log'.format(logs_dir, datetime.datetime.now().strftime('%Y%m%d'))
log_warning_file = '{}/{}.warn.log'.format(logs_dir, datetime.datetime.now().strftime('%Y%m%d'))
log_info_file = '{}/{}.info.log'.format(logs_dir, datetime.datetime.now().strftime('%Y%m%d'))

error_handler = TimeLoggerRolloverHandler(log_error_file, when='midnight')
error_handler.addFilter(LogFilter.error_filter)
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)

warning_handler = TimeLoggerRolloverHandler(log_warning_file, when='midnight')
warning_handler.addFilter(LogFilter.warning_filter)
warning_handler.setFormatter(formatter)
warning_handler.setLevel(logging.WARNING)

info_handel = TimeLoggerRolloverHandler(log_info_file, when='midnight')
info_handel.setFormatter(formatter)
info_handel.addFilter(LogFilter.info_filter)
info_handel.setLevel(logging.INFO)

logger.addHandler(error_handler)
logger.addHandler(warning_handler)
logger.addHandler(info_handel)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

__all__ = [logger]
