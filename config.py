import os
import log

filePath = os.path.join("C:\\", "BluetoothTerminal", "config")


def init():
    global filePath
    print(filePath)
    try:
        if not os.path.isdir(filePath):
            os.makedirs(filePath)
            print("makedir")
        config_file_path = os.path.join(filePath, "config.txt")
        if not os.path.isfile(config_file_path):
            with open(config_file_path, "x"):
                pass
    except Exception as e:
        log.log(str(e))


def writeConfig(data: dict[str, str]):
    global filePath
    try:
        config_file_path = os.path.join(filePath, "config.txt")
        configData = readConfig()
        if configData is None:
            configData = {}
        
        for key in data.keys():
            configData[key] = data[key]

        with open(config_file_path, "w") as config_file:
            for key in configData.keys():
                config_file.write(f"{key}={configData[key]}\n")
    except Exception as e:
        log.log(str(e))


def readConfig():
    global filePath
    dataDict = {}
    config_file_path = os.path.join(filePath, "config.txt")
    try:
        with open(config_file_path, "r") as configFile:
            lines = configFile.readlines()
        for line in lines:
            key, value = line.strip().split("=")
            dataDict[key] = value
        return dataDict
    except Exception as e:
        log.log(str(e))
        return None
    

def getValue(key) -> str:
  try:
    print(key)
    config = readConfig()
    print(config)
    if str(key) in config.keys():
      print("yes")
      value = config[str(key)]
      print(value)
      if value == "":
        raise ValueError("Value is a None value")
      return value
    else:
      raise KeyError("Key not available")
  except Exception as e:
    log.log(str(e))
    return "not available"

