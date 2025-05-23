import os

def _get_bool_env_var(key: str, default: bool) -> bool:
    var = os.environ.get(key)
    return var.lower() == 'true' if var else default


class Config:
    DEBUG = _get_bool_env_var('DEBUG', True)
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/user_registry_app.db')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my-secret-key')

    LOAD_USERS_ON_STARTUP = _get_bool_env_var('LOAD_USERS_ON_STARTUP', False)
