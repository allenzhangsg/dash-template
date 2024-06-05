bind = '0.0.0.0:8000'
workers = 2
loglevel = 'info'
accesslog = '-'
errorlog = '-'
timeout = 120
worker_class = 'sync'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s'
