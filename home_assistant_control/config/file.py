import configparser


class ConfigFile:

    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()

    def load(self):
        self.config.read(self.file_path)

    def save(self):
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)

    def get(self, section, key, default=None):
        return self.config.get(section, key, fallback=default)

    def set(self, section, key, value):
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, key, value)
