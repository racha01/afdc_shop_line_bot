import os

class LineConfig:
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'WaYSIv7uIgRWmwW0GEOJRbzhXHEVd3hG4MoVP9bsYImKRY/fJwj9Huwf41c1eTCnGVvkZcKSz7UD1FdXAuc9vniv6ZDFcvnO14Cb3dImIO6OHCFMHE/D67E43kyzExutIIvkyU/KlbyVcZrsFeKV/gdB04t89/1O/w1cDnyilFU=')
    WEBHOOK_HEADER = os.getenv('WEBHOOK_HEADER', '8317d31c0bef0e0539cd02f68c4dad13')
    DEBUG = False

class DevelopmentConfig(LineConfig):
    DEBUG = True