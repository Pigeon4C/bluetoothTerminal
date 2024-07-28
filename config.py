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
    

def getValue(thing) -> str:
  try:
    print(thing)
    names = readConfig()
    print(names)
    if thing in names.keys():
      name = names[thing]
      print("Name" + name)
      return name
    else:
      raise KeyError
  except Exception as e:
    log.log(str(e))
    print("why")
    return "not aviable"

