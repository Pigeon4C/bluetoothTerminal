import tkinter as tk

import bluetooth as bl
import log


def createWindow(title: str, height: int, width: int):
  try:
    dimmension = f"{height}x{width}"
    window = tk.Tk()
    window.title(title)
    window.geometry(dimmension)
    return window
  except Exception as e:
    log.log(str(e))


def createMainGui(title: str, height: int, width: int, ):
  sGui = createWindow(title, height, width)
    

  for portName in bl.listSerialPorts():
    portButton = tk.Button(sGui, text=portName, command=lambda t=portName: openTerminal(t))
    portButton.pack(pady=5, padx=5, side=tk.TOP, anchor=tk.NW)

  return sGui


def createTerminalGui(title: str, height: int, width: int, ):
  tGui = createWindow(title, height, width)
  commandEntry = tk.Entry(tGui, width=width)
  commandEntry.pack(pady=5, padx=5, side=tk.BOTTOM, anchor=tk.S)
   
  ser = bl.connectSerial(title)
    

  tGui.bind("<Return>", lambda event="", c=commandEntry, s=ser: bl.sendCommand(event, c, s))
  return tGui, ser


def openTerminal(windowName):
  print("open Terminal "+ str(windowName))
  terminal, ser = createTerminalGui(str(windowName), 400, 200)
  if ser.in_waiting > 0:
    bl.receiveMessage()
  terminal.mainloop()

