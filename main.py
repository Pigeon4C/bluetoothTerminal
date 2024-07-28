import gui
import log


def main():
  log.init()
  sGui = gui.createMainGui("Bluetooth Terminal", 600, 400)
  sGui.mainloop()

  return




if __name__ == "__main__":
  main() 