import importlib
from pandas_reader.setup import global_settings

CONFIG_MODULE = "config"

class Config:
    def __init__(self, config_module):
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))
        
        self.CONFIG_MODULE = config_module
        mod = importlib.import_module(self.CONFIG_MODULE)
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

config = Config(CONFIG_MODULE)
