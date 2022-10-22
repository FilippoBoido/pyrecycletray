import os
import pystray
from PIL import Image
from resources.constants import RECYCLE_IMAGE

working_dir = os.getcwd()


def get_tray_image():
    image = Image.open(
        os.path.join(
            working_dir,
            'resources',
            RECYCLE_IMAGE))

    return image


def main():
    icon = pystray.Icon(
        'recycletray',
        icon=get_tray_image())

    icon.run()


if __name__ == '__main__':
    main()
