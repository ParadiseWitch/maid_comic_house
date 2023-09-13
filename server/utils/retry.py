import logging
import traceback


def retry(fn, on_error=lambda: ()):
    i = 1
    err = None
    while i <= 3:
        try:
            return fn()
        except Exception as e:
            err = e
            traceback.print_exc()
            logging.warning('重试第{}次报错, e={}'.format(i, e))
            i = i+1
            continue
    on_error()
    logging.error('重试三次报错', err)
    raise ValueError('重试三次失败', err)
