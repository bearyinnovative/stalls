from envcfg.raw import stalls as config

bind = "{}:{}".format(config.HOST, config.PORT)
workers = int(config.GUNICORN_WORKERS)

errorlog = '-'
accesslog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

del config
