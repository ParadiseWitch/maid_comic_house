from logger import logger


def test_log():
    logger.error('error')
    logger.warning('warn')
    logger.info('info')


if __name__ == '__main__':
    # run()
    test_log()
