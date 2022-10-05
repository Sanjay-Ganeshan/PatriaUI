class TouchableMixin:
    """
    Lets you add "on left click" and "on right click", which will be called
    when a touch collides with the widget
    """
    def touch_init(self):
        self.bind(on_touch_down=self.touch_ev_handler)

    def touch_ev_handler(self, me, touch):
        position = tuple(touch.pos)

        if self.collide_point(*position):
            if touch.button == "right":
                self.on_right_click(position)
            else:
                self.on_left_click(position)

    def on_left_click(self, position):
        pass

    def on_right_click(self, position):
        pass

