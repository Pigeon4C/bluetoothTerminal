import os
from datetime import datetime
from tkinter import messagebox

filePath = os.path.join("C:\\", "BluetoothTerminal", "logs\\")

def init():
  try:
    global filePath
    if not os.path.isdir(filePath):
      os.makedirs(filePath)
    now = datetime.now()
    logFilePath = os.path.join(filePath, "log-" + now.strftime("%Y-%m-%d") + ".log")
    if not os.path.isfile(logFilePath):
      with open(logFilePath, "x"):
        pass
    return
  except Exception as e:
    messagebox.showerror("Error", f"There was an issue initializing logging\
                                 \nError: '{str(e)}'")


def log(logMessage: str) -> None:
  try:
    now = datetime.now()
    with open(filePath + "log-" + now.strftime("%Y-%m-%d") + ".log", "a") as logFile:
      logFile.write(f'[{now.strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]}] {logMessage}\n')
      logFile.close()
    return
  except Exception as e: 
    messagebox.showerror("Error", f"There was an issue logging an error\
                                 \nError: '{str(e)}'")