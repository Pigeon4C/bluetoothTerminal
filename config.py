import os
import log

filePath = os.path.join("C:\\", "BluetoothTerminal", "config\\")


def init():
  try:
    global filePath
    if not os.path.isdir(filePath):
      os.makedirs(filePath)
    configFilePath = os.path.join(filePath, "config.txt")
    if not os.path.isfile(configFilePath):
      with open(configFilePath, "x"):
        pass
  except Exception as e:
    log.log(str(e))


def writeConfig(data: dict[str, str]):
  try:

    global filePath
    configFilePath = os.path.join(filePath, "config.txt")
    configData = readConfig()
    if configData == None:
      configData = {}  
    for key in data.keys():
      configData[key] = data[key]
      with open(configFilePath, "w") as configFile:
        for key in configData.keys():
          configFile.write(f"{key}={configData[key]}\n")
        configFile.close()
  except Exception as e:
    log.log(str(e))


def readConfig():
  try:
    global filePath
    dataDict = {}
    configFilePath = os.path.join(filePath, "config.txt")
    with open(configFilePath, "r") as configFile:
      lines = configFile.readlines()
      for line in lines:
        key, value = line.strip().split("=")
        dataDict[key] = value
      configFile.close()
      return dataDict
  except Exception as e:
    log.log(str(e))
    return
    

def getValue(key) -> str:
  try:
    config = readConfig()
    if str(key) in config.keys():
      value = config[str(key)]
      if value == "":
        raise ValueError("Value is a None value")
      return value
    else:
      raise KeyError("Key not available")
  except Exception as e:
    log.log(str(e))
    return "not available"

