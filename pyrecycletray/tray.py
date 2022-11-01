import functools
import os
from typing import NoReturn
from pathlib import Path

from pystray import Icon
from PIL import Image as ImageModule, ImageDraw
from PIL.Image import Image
from .resources.index import icon_map  # type: ignore
from .custom_types import IconName


class Tray:

    def __init__(self, name: IconName = IconName('default')):
        """Tray base class

        Args:
            name: Name of the icon image
        """
        self.name: IconName = name
        self.image: Image = self.get_image()
        self.icon: Icon = Icon(name=name, icon=self.image)

    @functools.cache
    def get_image(self) -> Image:
        """This method is used during the Tray init.

        Fetches a default image or the image linked with the name specified
        during the init procedure.
        This method gets executed only once. All successive calls automatically
        return self.image due to the @functools.cache decorator

        Returns: The current image of the icon tray.

        """
        def join(name):
            self.image = ImageModule.open(
                os.path.join(
                    Path(__file__).parent,
                    'resources',
                    icon_map[name]))

        if self.name in icon_map:
            join(self.name)
        else:
            join('default')

        return self.image

    @functools.singledispatchmethod
    def set_image(self, *args) -> NoReturn:
        """Base implementation for the overloaded set_image method

        Args:
            *args:  If an unregistered type argument is passed to set_image
                    a TypeError will be raised

        """
        types = [type(arg).__name__ for arg in args]
        raise TypeError(f"set_image called with wrong argument type(s) {types}")

    @set_image.register
    def _(self, image: Image) -> None:
        """Overloaded set_image

        Args:
            image: The icon tray image to set

        """
        self.image = image
        self.icon.icon = image

    @set_image.register
    def _(self, color_1: str, color_2: str) -> None:
        """Overloaded set_image

        Args:
            color_1: The first color of the tray icon quadratic image pattern
            color_2: The second color of the tray icon quadratic image pattern

        """
        width = 64
        height = 64
        image = ImageModule.new('RGB', (width, height), color_1)
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (width / 2, 0, width, height / 2),
            fill=color_2)
        dc.rectangle(
            (0, height / 2, width / 2, height),
            fill=color_2)
        self.icon.icon = image
        self.image = image

    def run(self) -> None:
        """Starts the Tray"""
        self.icon.run_detached()

    def stop(self) -> None:
        """Stops the Tray"""
        self.icon.stop()
