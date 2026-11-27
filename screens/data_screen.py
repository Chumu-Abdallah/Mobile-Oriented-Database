from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class DataScreen(Screen):
    heading = StringProperty("")
    content = StringProperty("")
    status = StringProperty("")

