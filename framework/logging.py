import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s:%(process)d %(thread)d %(message)s'
        },
        'development': {
            'format': '%(levelname)s: %(module)s:%(lineno)s | %(message)s'
        },
        'info': {
            'format': '%(levelname)s: %(module)s:%(lineno)s | %(message)s'
        },
        'warning': {
            'format': '%(levelname)s: %(asctime)s | %(name)s | %(module)s:%(lineno)s | %(message)s'
        },
        'error': {
            'format': '%(levelname)s: %(asctime)s | %(name)s | %(module)s:%(lineno)s | %(message)s'
        },
    },
    'handlers': {
        'simple': {
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'development',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'error',
            'filename': 'error.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10,
        },
        'mail': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost' : 'localhost',
            'fromaddr': 'monitoring@example.com',
            'toaddrs': ['dev@example.com', 'support@example.com'],
            'subject': 'Critical error with application name',
        }
    },
    'loggers': {
        '': { # root logger
            'handlers':['console'],
            'level':'NOTSET',
            'propagate': True,
        },
        'warning': { 
            'handlers': ['file', 'console' ],
            'level': 'WARNING',
            'propagate': False,
        },
        'error': { 
            'handlers': ['file', 'console' ],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger('')

warning_logger = logging.getLogger('warning')

error_logger = logging.getLogger('error')
