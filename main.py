from pandas_reader.setup import config
from pandas_reader import status
from pandas_reader.manager import fetch

if __name__ == "__main__":
    if config.MODEL_INSTANCE is None:
        raise Exception(status.MODEL_INSTANCE_CONFIG_ERROR)
    if config.FILENAME is None:
        raise Exception(status.FILENAME_CONFIG_ERROR)

    data = fetch(config.MODEL_INSTANCE, config.FILENAME)
    print(data)
