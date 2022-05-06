from kivy.uix.boxlayout import BoxLayout


class NomScoreView(BoxLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(BoxLayout, self).on_touch_down(touch)

