from oasis2018.settings import BASE_DIR

import logging
import logging.config


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'wallet_debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'file',
            'filename': BASE_DIR + '/shop/log/wallet_debug.log',
            'maxBytes': 1024000,
            'backupCount': 3,
        },
        'wallet_info': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'file',
            'filename': BASE_DIR + '/shop/log/wallet_info.log',
        },
        'wallet_warning': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'file',
            'filename': BASE_DIR + '/shop/log/wallet_warning.log',
        }
    },
    'loggers': {
        'wallet': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'wallet_debug', 'wallet_info', 'wallet_warning'],
            'propagate': False,
        },
    },
})