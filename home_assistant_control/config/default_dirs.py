from appdirs import user_config_dir, user_data_dir, user_cache_dir
from home_assistant_control.__about__ import __PROG_NAME__ as PROG, __AUTHOR__ as AUTHOR

CONFIG_DIR = user_config_dir(PROG, AUTHOR)
DATA_DIR = user_data_dir(PROG, AUTHOR)
CACHE_DIR = user_cache_dir(PROG, AUTHOR)
