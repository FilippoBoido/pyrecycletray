from pyrecycletray.custom_types import IconName
from pyrecycletray.tray import Tray


def main():
    try:
        tray = Tray(name=IconName('test'))
        tray.run()
    finally:
        tray.stop()


if __name__ == '__main__':
    main()
