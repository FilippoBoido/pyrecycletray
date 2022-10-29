import functools
import os
from pathlib import Path

from pystray import Icon
from PIL import Image as ImageModule, ImageDraw
from PIL.Image import Image
from typing import Optional
from .resources.index import icon_map  # type: ignore
from .custom_types import IconName


class Tray:

    def __init__(self, name: IconName):
        self.name: IconName = name
        self.icon: Icon = Icon(name=name, icon=self.get_image())
        self.image: Optional[Image] = None

    @functools.cache
    def get_image(self) -> Image:
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
    def set_image(self, image: None) -> None:
        raise TypeError(f"{type(image)} is not an accepted type")

    @set_image.register
    def _(self, image: Image) -> None:
        self.icon.icon = image

    @set_image.register
    def _(self, color_1: str, color_2: str) -> None:
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

    def run(self) -> None:
        self.icon.run_detached()

    def stop(self) -> None:
        self.icon.stop()
