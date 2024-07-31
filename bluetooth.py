import tkinter as tk
import serial
import serial.tools.list_ports
from datetime import datetime
import log


def listSerialPorts():
  try:
    return [port.device for port in serial.tools.list_ports.comports()]
  except Exception as e:
    log.log(str(e))
    return

def connectSerial(port):
  try:
    return serial.Serial(port, baudrate=9600, timeout=1)
  except Exception as e:
    log.log(str(e))
    return 

def sendMacroCommand(command, log, ser):
  try:
    if command.strip() == "not available":
      log.config(state=tk.NORMAL)
      now = datetime.now()
      log.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] No Command associated with Macro\n")
      log.config(state=tk.DISABLED)
      return
    ser.write(command.encode())
    log.config(state=tk.NORMAL)
    now = datetime.now()
    log.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] Send: {command}\n")
    log.config(state=tk.DISABLED)
    return
  except Exception as e:
    log.log(str(e))
    return

def sendCommand(event, commandEntry: tk.Entry, ser: serial.Serial, log: tk.Text):
  try:
    command = commandEntry.get()
    commandEntry.delete(0, tk.END)
    command = command.strip()
    if command == "":
      return
    ser.write(command.encode())
    log.config(state=tk.NORMAL)
    now = datetime.now()
    log.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] Send: {command}\n")
    log.config(state=tk.DISABLED)
    return
  except Exception as e:
    log.log(str(e))

def receiveMessage(ser: serial.Serial, log) -> str:
  try:
    message = ser.readall()
    log.config(state=tk.NORMAL)
    now = datetime.now()
    log.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] {message}\n")
    log.config(state=tk.DISABLED)
    return str(message)
  except Exception as e:
    log.log(str(e))
    return