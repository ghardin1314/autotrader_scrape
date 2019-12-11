# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:38:00 2019

@author: Garrett
"""


import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainArea(BoxLayout):
    def __init__(self, **kwargs):
        super(MainArea, self).__init__(**kwargs)

# class SideMenu(BoxLayout):
#     def __init__(self, **kwargs):
#         super(SideMenu, self).__init__(**kwargs)

# class Body(BoxLayout):
#     def __init__(self, **kwargs):
#         super(Body, self).__init__(**kwargs)

class InputApp(App):
    def build(self):
        return Button(text="Hello World")

if __name__ == '__main__':
    app = InputApp()
    app.run