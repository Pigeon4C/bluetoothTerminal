import gui
import log
import config


def main():
  log.init()
  config.init()
  sGui = gui.createMainGui("Bluetooth Terminal", 600, 400)
  sGui.mainloop()

  return




if __name__ == "__main__":
  main() 