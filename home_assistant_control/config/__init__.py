import json

from home_assistant_control.config.args import CLIArguments
from home_assistant_control.config.env import ConfigEnv
from home_assistant_control.config.file import ConfigFile


class ConfigManager:

    def __init__(self, config_file_path, config_json_path):
        self.config_json = None
        self.cli = CLIArguments()
        self.env = ConfigEnv()
        self.file = ConfigFile(config_file_path)
        self.config_json_path = config_json_path

    def add_argument(self, *args, **kwargs):
        self.cli.add_argument(*args, **kwargs)

    def load(self):
        self.file.load()
        with open(self.config_json_path, 'r') as f:
            self.config_json = json.load(f)

    def get(self, key, section='DEFAULT', default=None):
        return (
            getattr(self.cli.parse(), key, None)
            or self.env.get(key)
            or self.file.get(section, key)
            or self.config_json.get(key)
            or default
        )
