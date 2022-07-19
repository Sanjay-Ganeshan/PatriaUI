from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    BooleanProperty,
)

from kivy.core.image import Image as CImage
from kivy.graphics.texture import Texture
from kivy.graphics import (
    Rectangle,
    Color,
    InstructionGroup,
)
import math

from .centered_label import CenteredLabel
from .box_sized_mixin import BoxSized
from .tooltip import OptionalTooltip
from kivy.uix.widget import Widget


class ProgressiveIconImpl:
    source = StringProperty("")
    current_value = NumericProperty(0.0)
    maximum_value = NumericProperty(1.0)
    pr_empty_color = ColorProperty([0, 0, 0])
    pr_full_color = ColorProperty([1.0, 0, 0])
    stacked = BooleanProperty(False)
    orientation = StringProperty("vertical")

    def progressive_init(self):
        # print(resource_find(self.source))
        self.color_and_rectangle = []
        self.igroups = []
        self._create_components()

        self.bind(
            source=self._create_components,
            maximum_value=self._create_components,
            stacked=self._create_components,
        )

        self.bind(
            pos=self.update,
            size=self.update,
            current_value=self.update,
            maximum_value=self.update,
            pr_empty_color=self.update,
            pr_full_color=self.update,
        )

    def _get_tex_coords(self, y, h):
        if self.orientation == "vertical":
            u = 0.0
            v = y
            w = 1.0
            return [
                u,
                1.0 - v,
                (u + w),
                1.0 - v,
                (u + w),
                1.0 - (v + h),
                u,
                1.0 - (v + h),
            ]
        else:
            u = y
            v = 0.0
            w = h
            h = 1.0
            return [
                u,
                1.0 - v,
                (u + w),
                1.0 - v,
                (u + w),
                1.0 - (v + h),
                u,
                1.0 - (v + h),
            ]

    def update(self, *args):
        (w, h) = self.size
        (x, y) = self.pos

        if self.orientation == "horizontal":
            x, y = y, x
            w, h = h, w

        if self.stacked:
            per_icon_height = int(h / self.maximum_value)
            for ix, (col, rect) in enumerate(self.color_and_rectangle):
                col.rgb = (
                    self.pr_full_color
                    if (ix < self.current_value)
                    else self.pr_empty_color
                )
                rect.pos = (x, ix * per_icon_height + y)
                rect.size = (w, per_icon_height)
                rect.tex_coords = self._get_tex_coords(y=0, h=1.0)
        else:
            ratio = min(self.current_value / self.maximum_value, 1.0)
            full_height = int(ratio * h)
            self.color_and_rectangle[0][0].rgb = self.pr_full_color
            self.color_and_rectangle[0][1].pos = (x, y)
            self.color_and_rectangle[0][1].size = (w, full_height)
            self.color_and_rectangle[0][1].tex_coords = self._get_tex_coords(
                y=0, h=ratio
            )

            self.color_and_rectangle[1][0].rgb = self.pr_empty_color
            self.color_and_rectangle[1][1].size = (w, h - full_height)
            self.color_and_rectangle[1][1].pos = (x, y + full_height)
            self.color_and_rectangle[1][1].tex_coords = self._get_tex_coords(
                y=ratio, h=1.0 - ratio
            )

        if self.orientation == "horizontal":
            for (_, rect) in self.color_and_rectangle:
                x, y = rect.pos
                w, h = rect.size

                rect.size = h, w
                rect.pos = y, x

    def _create_components(self, *args):
        for each_igroup in self.igroups:
            self.canvas.before.remove(each_igroup)

        self.color_and_rectangle.clear()
        self.igroups.clear()
        if self.source == "":
            self.tex = None
        if self.source != "":
            self.tex = CImage(self.source).texture
            if self.stacked:
                n_components = int(math.ceil(self.maximum_value))
            else:
                n_components = 2

            for each_component in range(n_components):
                group = InstructionGroup()
                c = Color(*self.pr_full_color)
                rect = Rectangle(
                    size=self.size,
                    pos=self.pos,
                    texture=self.tex,
                    tex_coords=self._get_tex_coords(0.0, 1.0),
                )
                group.add(c)
                group.add(rect)
                self.canvas.before.add(group)
                self.color_and_rectangle.append((c, rect))
                self.igroups.append(group)


class ProgressiveIcon(Widget, ProgressiveIconImpl, BoxSized, OptionalTooltip):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_init()
        self.progressive_init()


class ProgressiveText(CenteredLabel, ProgressiveIconImpl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progressive_init()

    def update(self, *args):
        super().update(*args)
        self.text = f"{self.current_value} / {self.maximum_value}"


class AnyIcon(ProgressiveIcon, BoxSized):
    def __init__(self, **kwargs):
        super().__init__(
            maximum_value=1,
            current_value=1,
            pr_empty_color="white",
            pr_full_color=kwargs.pop("pr_full_color", "white"),
            stacked=False,
            **kwargs,
        )
        self.box_init()
