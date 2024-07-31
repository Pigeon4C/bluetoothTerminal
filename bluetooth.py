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

def connectSerial(port, baudrate, timeout):
  try:
    ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
    log.log(f"Connected to Serial Port: '{port}' with baudrate: '{baudrate}' and timeout: '{timeout}'")
    return ser
  except Exception as e:
    log.log(str(e))
    return 

def sendMacroCommand(command, TerminalLog, ser):
  try:
    if command.strip() == "not available":
      TerminalLog.config(state=tk.NORMAL)
      now = datetime.now()
      TerminalLog.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] No Command associated with Macro\n")
      TerminalLog.config(state=tk.DISABLED)
      return
    ser.write(command.encode())
    TerminalLog.config(state=tk.NORMAL)
    now = datetime.now()
    TerminalLog.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] Send: {command}\n")
    TerminalLog.config(state=tk.DISABLED)
    log.log(f"Send command: '{command}'")
    return
  except Exception as e:
    log.log(str(e))
    return

def sendCommand(event, commandEntry: tk.Entry, ser: serial.Serial, TerminalLog: tk.Text):
  try:
    command = commandEntry.get()
    commandEntry.delete(0, tk.END)
    command = command.strip()
    if command == "":
      return
    ser.write(command.encode())
    TerminalLog.config(state=tk.NORMAL)
    now = datetime.now()
    TerminalLog.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] Send: {command}\n")
    TerminalLog.config(state=tk.DISABLED)
    log.log(f"Send command: '{command}'")
    return
  except Exception as e:
    log.log(str(e))
    return

def receiveMessage(ser: serial.Serial, TerminalLog) -> str:
  try:
    message = ser.readall()
    TerminalLog.config(state=tk.NORMAL)
    now = datetime.now()
    TerminalLog.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] {message}\n")
    TerminalLog.config(state=tk.DISABLED)
    log.log(f"Received Message: '{message}'")
    return str(message)
  except Exception as e:
    log.log(str(e))
    return