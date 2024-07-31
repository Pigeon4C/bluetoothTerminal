import gui
import log
import config


def main():
  log.init()
  config.init()
  try:
    sGui = gui.createMainGui("Bluetooth Terminal", 600, 400)
    sGui.mainloop()
    return
  except Exception as e:
    log.log(str(e))
    return


if __name__ == "__main__":
  main()