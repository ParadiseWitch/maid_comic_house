from logger import mlogger


def test_log():
    mlogger.error('error')
    mlogger.warning('warn')
    mlogger.info('info')


if __name__ == '__main__':
    # run()
    test_log()
