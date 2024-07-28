import tkinter as tk
import serial
import serial.tools.list_ports


def listSerialPorts():
  return [port.device for port in serial.tools.list_ports.comports()]


def connectSerial(port):
  return serial.Serial(port, baudrate=9600, timeout=1)

def sendCommand(event, commandEntry: tk.Entry, ser: serial.Serial):
  command = commandEntry.get()
  commandEntry.delete(0, tk.END)
  command = command.strip()
  if command == "":
    return
  print(command)
  ser.write(command.encode())
  return


def receiveMessage(ser: serial.Serial):
  return ser.readall()