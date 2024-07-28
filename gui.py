import tkinter as tk
import tkinter.scrolledtext as st
from tkinter.simpledialog import askstring

import bluetooth as bl
import log
import config


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

  sGui.portButtons = []

  refreshButton = tk.Button(sGui, text="Refresh", command=lambda s=sGui: createPortButtons(s))
  refreshButton.pack(padx=5, pady=5, side=tk.TOP, anchor=tk.NW)
  
  sGui.portButtonFrame = tk.Frame(sGui)
  sGui.portButtonFrame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

  createPortButtons(sGui)

  

  return sGui


def createTerminalGui(title: str, height: int, width: int, ):
  tGui = createWindow(title, height, width)
  commandEntry = tk.Entry(tGui, width=width)
  commandEntry.pack(pady=5, padx=5, side=tk.BOTTOM, anchor=tk.S)

  tGui.macroButtonFrame = tk.Frame(tGui)
  tGui.macroButtonFrame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

  createMacroButtons(tGui)

  log = st.ScrolledText(tGui, state=tk.DISABLED, wrap=tk.WORD)
  log.pack(padx=5, pady=5)

  ser = bl.connectSerial(title)
  tGui.bind("<Return>", lambda event="", c=commandEntry, s=ser, l=log: bl.sendCommand(event, c, s, l))
  return tGui, ser, log


def openTerminal(windowName):
  print("open Terminal "+ str(windowName))
  terminal, ser, log = createTerminalGui(str(windowName), 400, 200)
  if ser.in_waiting > 0:
    bl.receiveMessage(ser, log)
  terminal.mainloop()


def excecuteMacro(macroName):
  return


def configMacro(event, idx, macroButton):
  print(idx)
  displayName = askstring("Rename", "Enter the new display name")
  buttonContent = askstring("Button function", "Enter macro command for this macro")
  macroDict = {
    str(idx): displayName,
    str(idx) + "-command": buttonContent,
  }
  config.writeConfig(macroDict)
  macroButton.config(text=displayName)



def createPortButtons(sGui):
  if len(sGui.portButtons) > 0:
    for portButton in sGui.portButtons:
      portButton.destroy()
    sGui.portButtons.clear()
  for idx, portName in enumerate(bl.listSerialPorts()):
    portButton = tk.Button(sGui.portButtonFrame, text=portName, command=lambda t=portName: openTerminal(t))
    portButton.grid(row=0, column=idx, padx=5, pady=5)
    sGui.portButtons.append(portButton)


def createMacroButtons(tGui):
  for idx, macroName in enumerate(range(1,6)):
    macroButton = tk.Button(tGui.macroButtonFrame, text=config.getValue(idx), command=lambda t=macroName: excecuteMacro(t))
    macroButton.bind("<Button-3>", lambda event, t=idx, b=macroButton: configMacro(event, t ,b))
    macroButton.grid(row=0, column=idx, padx=5, pady=5)
