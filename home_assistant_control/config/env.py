import os


class ConfigEnv:

    @staticmethod
    def get(key, default=None):
        return os.getenv(key, default)
