import config
import status
from manager import fetch

if __name__ == "__main__":
    if config.MODEL_INSTANCE is None:
        raise Exception(status.MODEL_INSTANCE_CONFIG_ERROR)
    if config.FILNAME is None:
        raise Exception(status.FILENAME_CONFIG_ERROR)

    data = fetch(config.MODEL_INSTANCE, config.FILNAME)
    print(data)
