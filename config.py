import os
import log

filePath = os.path.join("C:\\", "BluetoothTerminal", "config\\")


def init():
  try:
    global filePath
    print(filePath)
    if not os.path.isdir(filePath):
      os.makedirs(filePath)
      print("makedir")
    configFilePath = os.path.join(filePath, "config.txt")
    if not os.path.isfile(configFilePath):
      with open(configFilePath, "x"):
        pass
  except Exception as e:
    log.log(str(e))


def writeConfig(data: dict[str, str]):
  try:
    print(data)
    global filePath
    configFilePath = os.path.join(filePath, "config.txt")
    print(configFilePath)
    configData = readConfig()
    print(configData)
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

