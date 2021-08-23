import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'loggers': {
        '': {  # root logger
            'level': 'NOTSET',
            'handlers': ['debug_console_handler', 'info_rotating_file_handler', 'error_file_handler', 'critical_mail_handler'],
        },
        'warning': { 
            'level': 'WARNING',
            'propagate': False,
            'handlers': ['info_rotating_file_handler', 'error_file_handler' ],
        },
        'error': { 
            'level': 'ERROR',
            'propagate': False,
            'handlers': ['info_rotating_file_handler', 'error_file_handler' ],
        },
    },
    'handlers': {
        'debug_console_handler': {
            'level': 'DEBUG',
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_rotating_file_handler': {
            'level': 'INFO',
            'formatter': 'info',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'info.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'error_file_handler': {
            'level': 'WARNING',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'mode': 'a',
        },
        'critical_mail_handler': {
            'level': 'CRITICAL',
            'formatter': 'error',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost' : 'localhost',
            'fromaddr': 'monitoring@example.com',
            'toaddrs': ['dev@example.com', 'qa@example.com'],
            'subject': 'Critical error with application name'
        }
    },
    'formatters': {
        'info': {
            'format': '%(levelname)s:   %(message)s'
        },
        'warning': {
            'format': '%(levelname)s: %(asctime)s | %(name)s | %(module)s:%(lineno)s | %(message)s'
        },
        'error': {
            'format': '%(levelname)s: %(asctime)s | %(name)s | %(module)s:%(lineno)s | %(message)s'
        },
    },

}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger('')

error_logger = logging.getLogger('error')
