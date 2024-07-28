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
   
  log = tk.Text(tGui, state=tk.DISABLED, wrap=tk.WORD)
  log.pack(padx=10, pady=5)

  ser = bl.connectSerial(title)
  tGui.bind("<Return>", lambda event="", c=commandEntry, s=ser: bl.sendCommand(event, c, s))
  return tGui, ser


def openTerminal(windowName):
  print("open Terminal "+ str(windowName))
  terminal, ser = createTerminalGui(str(windowName), 400, 200)
  if ser.in_waiting > 0:
    bl.receiveMessage()
  terminal.mainloop()


def createPortButtons(sGui):
  if len(sGui.portButtons) > 0:
    for portButton in sGui.portButtons:
      portButton.destroy()
    sGui.portButtons.clear()
  for idx, portName in enumerate(bl.listSerialPorts()):
    portButton = tk.Button(sGui.portButtonFrame, text=portName, command=lambda t=portName: openTerminal(t))
    portButton.grid(row=0, column=idx, padx=5, pady=5)
    sGui.portButtons.append(portButton)