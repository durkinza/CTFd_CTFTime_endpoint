from CTFd.api.v1 import CTFd_API_v1
from routes import ctftime_namespace

def load(app):
    CTFd_API_v1.add_namespace(ctftime_namespace, "/ctftime")
