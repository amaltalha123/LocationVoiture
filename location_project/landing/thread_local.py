import threading

_user_local = threading.local()

def set_raw_password(password):
    _user_local.raw_password = password

def get_raw_password():
    return getattr(_user_local, 'raw_password', None)

def clear_raw_password():
    if hasattr(_user_local, 'raw_password'):
        del _user_local.raw_password
