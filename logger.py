import logging
import functools

def create():
    LOG_FORMAT='%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(filename="/home/andres/Documentos/python_WorkSpace/exampleFlask/AppLog.log",format=LOG_FORMAT)
    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)
    return logger

def exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = create()
        try:
            return func(*args, **kwargs)
        except Exception:
            err = "Hubo un error en "+str(func.__name__)
            logger.exception(err)
            raise
    return wrapper
