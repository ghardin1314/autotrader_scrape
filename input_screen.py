import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainArea(BoxLayout):
    def __init__(self, **kwargs):
        super(MainArea, self).__init__(**kwargs)

class SideMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(SideMenu, self).__init__(**kwargs)

class Body(BoxLayout):
    def __init__(self, **kwargs):
        super(Body, self).__init__(**kwargs)

class Header(BoxLayout):
    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)

class Footer(BoxLayout):
    def __init__(self, **kwargs):
        super(Footer, self).__init__(**kwargs)

class TotalSpace(BoxLayout):
    def __init__(self, **kwargs):
        super(TotalSpace, self).__init__(**kwargs)

class InputApp(App):
    def build(self):
        return TotalSpace()

if __name__ == '__main__':
    app = InputApp()
    app.run()