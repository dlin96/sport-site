class Config(object):
    pass


class DevelopmentConfig(Config):
    DEBUG=True


class ProductionConfig(Config):
    DEBUG=False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}