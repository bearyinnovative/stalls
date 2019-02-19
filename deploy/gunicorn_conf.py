from envcfg.raw import stalls as config

bind = "{}:{}".format(config.HOST, config.PORT)
workers = int(config.GUNICORN_WORKERS)

del config
