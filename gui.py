import tkinter as tk
import tkinter.scrolledtext as st
from tkinter.simpledialog import askstring
from tkinter import messagebox

import bluetooth as bl
import log
import config

terminalLog = ""
ser = ""

def createWindow(title: str, width: int, height: int):
  try:
    dimmension = f"{width}x{height}"
    window = tk.Tk()
    window.title(title)
    window.geometry(dimmension)
    return window
  except Exception as e:
    log.log(str(e))
    return

def createMainGui(title: str, width: int, height: int):
  try:
    sGui = createWindow(title, width, height)

    sGui.portButtons = []

    refreshButton = tk.Button(sGui, text="Refresh", command=lambda s=sGui: createPortButtons(s))
    refreshButton.pack(padx=5, pady=5, side=tk.TOP, anchor=tk.NW)
    
    sGui.portButtonFrame = tk.Frame(sGui)
    sGui.portButtonFrame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    createPortButtons(sGui)
    log.log(f"Created Main Gui with title: {title}, width: {width}, height: {height}")
    return sGui
  except Exception as e:
    log.log(str(e))
    return


def createTerminalGui(title: str, port: str, width: int, height: int):
  try:
    tGui = createWindow(title, width, height)
    commandEntry = tk.Entry(tGui, width=width)
    commandEntry.pack(pady=5, padx=5, side=tk.BOTTOM, anchor=tk.S)

    tGui.macroButtonFrame = tk.Frame(tGui)
    tGui.macroButtonFrame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    createMacroButtons(tGui)
    global terminalLog, ser
    terminalLog = st.ScrolledText(tGui, state=tk.DISABLED, wrap=tk.WORD)
    terminalLog.pack(padx=5, pady=5)

    ser = bl.connectSerial(port, baudrate=9600, timeout=1)
    if ser == None:
      tGui.destroy()
      messagebox.showerror("Error", f"There was an issue creating a connection\
                                      \nwith port {port}")  
      raise ConnectionRefusedError("Connection wasn't established")
    tGui.bind("<Return>", lambda event="", c=commandEntry, s=ser, l=terminalLog: bl.sendCommand(event, c, s, l))
    log.log(f"Created Terminal Window with title: {title}, width: {width}, height: {height}")
    return tGui, ser, terminalLog
  except Exception as e:
    log.log(str(e))
    return


def openTerminal(portName):
  try:
    if not config.getValue(portName) == "not available":
      displayName = f"{config.getValue(portName)} ({portName})"
    else:
      displayName = portName
    global ser, terminalLog
    terminal, ser, terminalLog = createTerminalGui(displayName, portName, 600, 400)
    if ser.in_waiting > 0:
      bl.receiveMessage(ser, terminalLog)
    terminal.mainloop()
    return
  except Exception as e:
    log.log(str(e))
    return

def excecuteMacro(idx):
  try:
    command = config.getValue(f"Macro{str(idx)}-command")
    log.log(f"Excecuted Macro: 'Macro{idx}' with command: '{command}'")
    global terminalLog, ser
    bl.sendMacroCommand(command, terminalLog, ser)
    return
  except Exception as e:
    log.log(str(e))
    return


def configMacro(event, idx, macroButton):
  try:
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
    log.log(f"Created Macro with Name: '{displayName}' and function: '{buttonContent}'")
    return
  except Exception as e:
    log.log(str(e))
    return


def configPortName(event, portName, portButton):
  try:
    displayName = askstring("Rename", "Enter the new display name\
                                     \nMax length 20 characters")
    if len(displayName) > 20:
      displayName = displayName[0:20]
    buttonDict = {
      portName: displayName,
    }
    config.writeConfig(buttonDict)
    portButton.config(text=f"{displayName} ({portName})")
    log.log(f"Configured Port name to: '{displayName}'")
    return
  except Exception as e:
    log.log(str(e))
    return


def createPortButtons(sGui):
  try:
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
  except Exception as e:
    log.log(str(e))
    return
  

def createMacroButtons(tGui):
  try:
    row = 1
    column = 0
    for idx in range(1,22):
      if not config.getValue(f"Macro{idx}") == "not available":
        macroName = config.getValue(f"Macro{idx}")
      else:
        macroName = f"Macro{idx}"
      if idx == 8 or idx == 15 or idx == 24:
        row += 1
        column = 0
      macroButton = tk.Button(tGui.macroButtonFrame, text=macroName, command=lambda t=idx: excecuteMacro(t))
      macroButton.bind("<Button-3>", lambda event, t=idx, b=macroButton: configMacro(event, t ,b))
      macroButton.grid(row=row - 1, column=column, padx=5, pady=5)
      column += 1
    return
  except Exception as e:
    log.log(str(e))
    return