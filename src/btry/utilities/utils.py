import os

def get_var_from_env(var_name: str, default: str = None) -> str:
    """
    Get the value of an environment variable, with an optional default value.
    """
    return os.getenv(var_name, default)