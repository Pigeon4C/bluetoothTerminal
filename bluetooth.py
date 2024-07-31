import tkinter as tk
import serial
import serial.tools.list_ports
from datetime import datetime


def listSerialPorts():
  return [port.device for port in serial.tools.list_ports.comports()]


def connectSerial(port):
  return serial.Serial(port, baudrate=9600, timeout=1)


def sendMacroCommand(command, log, ser):
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


def sendCommand(event, commandEntry: tk.Entry, ser: serial.Serial, log: tk.Text):
  command = commandEntry.get()
  commandEntry.delete(0, tk.END)
  command = command.strip()
  if command == "":
    return
  print(command)
  ser.write(command.encode())
  log.config(state=tk.NORMAL)
  now = datetime.now()
  log.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] Send: {command}\n")
  log.config(state=tk.DISABLED)
  return


def receiveMessage(ser: serial.Serial, log) -> str:
  message = ser.readall()
  log.config(state=tk.NORMAL)
  now = datetime.now()
  log.insert("1.0", f"[{now.strftime('%H:%M:%S.%f')[:-3]}] {message}\n")
  log.config(state=tk.DISABLED)
  return str(message)