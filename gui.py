import tkinter as tk
import tkinter.scrolledtext as st
from tkinter.simpledialog import askstring

import bluetooth as bl
import log
import config

log = ""
ser = ""

def createWindow(title: str, width: int, height: int):
  try:
    dimmension = f"{height}x{width}"
    window = tk.Tk()
    window.title(title)
    window.geometry(dimmension)
    return window
  except Exception as e:
    log.log(str(e))
    return

def createMainGui(title: str, height: int, width: int):
  sGui = createWindow(title, height, width)

  sGui.portButtons = []

  refreshButton = tk.Button(sGui, text="Refresh", command=lambda s=sGui: createPortButtons(s))
  refreshButton.pack(padx=5, pady=5, side=tk.TOP, anchor=tk.NW)
  
  sGui.portButtonFrame = tk.Frame(sGui)
  sGui.portButtonFrame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

  createPortButtons(sGui)
  return sGui


def createTerminalGui(title: str, width: int, height: int, ):
  tGui = createWindow(title, height, width)
  commandEntry = tk.Entry(tGui, width=width)
  commandEntry.pack(pady=5, padx=5, side=tk.BOTTOM, anchor=tk.S)

  tGui.macroButtonFrame = tk.Frame(tGui)
  tGui.macroButtonFrame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

  createMacroButtons(tGui)
  global log, ser
  log = st.ScrolledText(tGui, state=tk.DISABLED, wrap=tk.WORD)
  log.pack(padx=5, pady=5)

  ser = bl.connectSerial(title)
  tGui.bind("<Return>", lambda event="", c=commandEntry, s=ser, l=log: bl.sendCommand(event, c, s, l))
  return tGui, ser, log


def openTerminal(portName):
  if not config.getValue(portName) == "not available":
    displayName = f"{config.getValue(portName)} ({portName})"
  else:
    displayName = portName
  print("open Terminal "+ str(displayName))
  global ser
  terminal, ser, log = createTerminalGui(str(displayName), 600, 400)
  if ser.in_waiting > 0:
    bl.receiveMessage(ser, log)
  terminal.mainloop()
  return

def excecuteMacro(macroIdx):
  command = config.getValue(str(macroIdx) + "-command")
  global log, ser
  bl.sendMacroCommand(command, log, ser)
  return  


def configMacro(event, idx, macroButton):
  print(idx)
  displayName = askstring("Rename", "Enter the new display name\
                                   \nMax length 20 characters")
  buttonContent = askstring("Button function", "Enter macro command for this macro")
  if len(displayName) > 20:
    displayName = displayName[0:20]
  macroDict = {
    f"Macro{str(idx)}": displayName,
    f"Macro{str(idx)}-command": buttonContent,
  }
  config.writeConfig(macroDict)
  macroButton.config(text=displayName)
  return


def configPortName(event, portName, portButton):
  displayName = askstring("Rename", "Enter the new display name\
                                   \nMax length 20 characters")
  if len(displayName) > 20:
    displayName = displayName[0:20]
  buttonDict = {
    portName: displayName,
  }
  config.writeConfig(buttonDict)
  portButton.config(text=f"{displayName} ({portName})")
  return



def createPortButtons(sGui):
  if len(sGui.portButtons) > 0:
    for portButton in sGui.portButtons:
      portButton.destroy()
    sGui.portButtons.clear()
  for idx, portName in enumerate(bl.listSerialPorts()):
    if not config.getValue(portName) == "not available":
      displayName = f"{config.getValue(portName)} ({portName})"
    else:
      displayName = portName

    portButton = tk.Button(sGui.portButtonFrame, text=displayName, command=lambda t=portName: openTerminal(t))
    portButton.bind("<Button-3>", lambda event, t=portName, b=portButton: configPortName(event, t, b))
    portButton.grid(row=0, column=idx, padx=5, pady=5)
    sGui.portButtons.append(portButton)
  return

def createMacroButtons(tGui):
  for idx in range(1,6):
    if not config.getValue(f"Macro{idx}") == "not available":
      macroName = config.getValue(f"Macro{idx}")
    else:
      macroName = f"Macro{idx}"
    macroButton = tk.Button(tGui.macroButtonFrame, text=macroName, command=lambda t=idx: excecuteMacro(t))
    macroButton.bind("<Button-3>", lambda event, t=idx, b=macroButton: configMacro(event, t ,b))
    macroButton.grid(row=0, column=idx, padx=5, pady=5)
  return