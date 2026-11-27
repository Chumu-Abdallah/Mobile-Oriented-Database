from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


# Import operating system library
import os

# Import Kivy font registration
from kivy.core.text import LabelBase

# Get the current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Locate Material Icons font
ICON_FONT = os.path.join(
    BASE_DIR,
    "assets",
    "MaterialIcons-Regular.ttf"
)
# Size of icones
print("FONT PATH:", ICON_FONT)
print("FONT EXISTS:", os.path.exists(ICON_FONT))

# Register Google Material Icons font
LabelBase.register(
    name="MaterialIcons",
    fn_regular=ICON_FONT
)

KV_DASHBOARD = r"""
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<HomeCard@Button>:
    markup: True
    background_normal: ""
    background_color: get_color_from_hex("#FFFFFF")
    color: get_color_from_hex("#1E2A5A")
    font_size: "15sp"
    bold: True
    size_hint: 1, None
    height: dp(110)
    halign: "center"
    valign: "middle"
    text_size: self.width, None

<BottomNavButton@Button>:
    markup: True
    background_normal: ""
    background_color: get_color_from_hex("#FFFFFF")
    color: get_color_from_hex("#1E2A5A")
    font_size: "13sp"
    bold: True
    size_hint: 1, 1

<DashboardScreen>:
    name: "dashboard"
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: dp(218)
            padding: dp(16), dp(12)
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: get_color_from_hex("#1E2A5A")
                Rectangle:
                    pos: self.pos
                    size: self.size
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: dp(52)
                spacing: dp(10)
                Label:
                    text: "◉"
                    font_size: "34sp"
                    color: get_color_from_hex("#FFFFFF")
                    size_hint_x: None
                    width: dp(48)
                BoxLayout:
                    orientation: "vertical"
                    Label:
                        text: "Welcome,"
                        color: get_color_from_hex("#FFFFFF")
                        font_size: "16sp"
                        halign: "left"
                        valign: "bottom"
                        text_size: self.width, None
                    Label:
                        text: root.welcome
                        color: get_color_from_hex("#FFFFFF")
                        font_size: "16sp"
                        bold: True
                        halign: "left"
                        valign: "top"
                        text_size: self.width, None
                Label:
                    text: "⚙"
                    font_size: "28sp"
                    color: get_color_from_hex("#FFFFFF")
                    size_hint_x: None
                    width: dp(38)
            Widget:
                size_hint_y: None
                height: dp(1)
                canvas.before:
                    Color:
                        rgba: get_color_from_hex("#FFFFFF")
                    Rectangle:
                        pos: self.pos
                        size: self.size
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: dp(30)
                Label:
                    text: root.academic_year
                    color: get_color_from_hex("#FFFFFF")
                    font_size: "18sp"
                    halign: "left"
                    text_size: self.width, None
                Label:
                    text: root.semester
                    color: get_color_from_hex("#FFFFFF")
                    font_size: "18sp"
                    halign: "right"
                    text_size: self.width, None
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: dp(82)
                padding: dp(14), dp(10)
                spacing: dp(4)
                canvas.before:
                    Color:
                        rgba: get_color_from_hex("#FFFFFF")
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(8)]
                Label:
                    text: root.reg_no
                    color: get_color_from_hex("#1E2A5A")
                    font_size: "19sp"
                    bold: True
                    halign: "left"
                    valign: "middle"
                    text_size: self.width, None
                    size_hint_y: None
                    height: dp(30)
                Label:
                    text: root.programme_name
                    color: get_color_from_hex("#1E2A5A")
                    font_size: "17sp"
                    bold: True
                    halign: "left"
                    valign: "middle"
                    text_size: self.width, None
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height
                canvas.before:
                    Color:
                        rgba: get_color_from_hex("#A8A8A8")
                    Rectangle:
                        pos: self.pos
                        size: self.size
                GridLayout:
                    cols: 3
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(110)
                    HomeCard:
                        text: "[size=40][font=MaterialIcons][/font][/size]\n[size=15]Courses[/size]"
                        on_release: app.show_data("courses")
                    HomeCard:
                        text: "[size=40][font=MaterialIcons][/font][/size]\n[size=15]Exam Number[/size]"
                        on_release: app.make_payment_request()
                    HomeCard:
                        text: "[size=40][font=MaterialIcons][/font][/size]\n[size=15]ID[/size]"
                        on_release: app.show_data("profile")
                GridLayout:
                    cols: 3
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(110)
                    HomeCard:
                        text:  "[size=40][font=MaterialIcons][/font][/size]\n[size=15]Results[/size]"
                        on_release: app.show_data("results")
                BoxLayout:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(340)
                    canvas.before:
                        Color:
                            rgba: get_color_from_hex("#FFFFFF")
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(10)]
                    Label:
                        text: root.heading
                        font_size: "19sp"
                        bold: True
                        color: get_color_from_hex("#1E2A5A")
                        size_hint_y: None
                        height: dp(32)
                        halign: "left"
                        text_size: self.width, None

             # Result (cousework and Semester result button)           

                    GridLayout:
                        cols: 1
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(100) if root.heading.lower() == "results" else 0
                        opacity: 1 if root.heading.lower() == "results" else 0
                        disabled: root.heading.lower() != "results"

                    Button:
                        text: "Coursework"
                        size_hint_y: None
                        height: dp(45)
                        on_release: app.show_data("coursework")

                    Button:
                        text: "Examination Results"
                        size_hint_y: None
                        height: dp(45)
                        on_release: app.show_data("examination")
                    ScrollView:
                        do_scroll_x: False
                        Label:
                            text: root.content
                            markup: True
                            color: get_color_from_hex("#1E2A5A")
                            font_size: "15sp"
                            text_size: self.width, None
                            size_hint_y: None
                            height: self.texture_size[1] + dp(20)
                            halign: "left"
                            valign: "top"
                    Button:
                        text: "Download PDF"
                        size_hint_y: None
                        height: dp(44)
                        background_normal: ""
                        background_color: get_color_from_hex("#A50000")
                        color: get_color_from_hex("#FFFFFF")
                        opacity: 0 if root.showing_home else 1
                        disabled: root.showing_home
                        on_release: app.download_pdf()
                    Label:
                        text: root.status
                        color: get_color_from_hex("#1A6A2A")
                        size_hint_y: None
                        height: dp(28)
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(64)
            canvas.before:
                Color:
                    rgba: get_color_from_hex("#FFFFFF")
                Rectangle:
                    pos: self.pos
                    size: self.size
            BottomNavButton:
                text: "[size=30][font=MaterialIcons][/font][/size]\n[size=13]Home[/size]"
                markup: True
                background_color: get_color_from_hex("#E6F0FF")
                on_release: app.show_home()
            BottomNavButton:
                text: "[size=30][font=MaterialIcons][/font][/size]\n[size=13]Payments[/size]"
                markup: True
                on_release: app.show_data("payments")
            BottomNavButton:
                text: "[size=30][font=MaterialIcons][/font][/size]\n[size=13]Profile[/size]"
                on_release: app.show_data("profile")
            BottomNavButton:
                text: "[size=30][font=MaterialIcons][/font][/size]\n[size=13]Logout[/size]"
                markup: True
                on_release: app.logout()
"""

Builder.load_string(KV_DASHBOARD)

class DashboardScreen(Screen):
    welcome = StringProperty("")
    reg_no = StringProperty("")
    programme_name = StringProperty("")
    academic_year = StringProperty("")
    semester = StringProperty("")
    heading = StringProperty("Home")
    content = StringProperty("")
    status = StringProperty("")
    showing_home = True