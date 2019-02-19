import logging
import sys

__LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'error': logging.ERROR,
}

def build_logger(textlevel: str) -> logging.Logger:
    level = __LOG_LEVELS.get(textlevel)
    if not level:
        raise KeyError(f"Invallid log level: {level}")

    logger = logging.getLogger('moviememes')
    print(textlevel, level)
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    
    stdout = logging.StreamHandler(sys.stdout)
    stdout.addFilter(lambda record: record.levelno < logging.ERROR)
    stdout.setFormatter(formatter)
    logger.addHandler(stdout)

    stderr = logging.StreamHandler(sys.stderr)
    stderr.addFilter(lambda record: record.levelno >= logging.ERROR)
    stderr.setFormatter(formatter)
    logger.addHandler(stderr)

    return logger