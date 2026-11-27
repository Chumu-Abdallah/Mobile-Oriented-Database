from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.animation import Animation

KV_LOGIN = r"""
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<LoginScreen>:
    name: "login"
    FloatLayout:
        canvas.before:
            Color:
                rgba: get_color_from_hex("#00537A")
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            id: login_card
            orientation: "vertical"
            padding: dp(24)
            spacing: dp(12)
            size_hint: 0.88, 0.62
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            opacity: 0
            canvas.before:
                Color:
                    rgba: get_color_from_hex("#FFFFFF")
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(6)]
            Widget:
                size_hint_y: .18
            Label:
                id: title_label
                text: "[b]STUDENT MANAGEMENT APP[/b]"
                markup: True
                font_size: "27sp"
                color: get_color_from_hex("#00537A")
                size_hint_y: None
                height: dp(55)
                opacity: 0
            Label:
                text: "Sign in using your registration number"
                color: get_color_from_hex("#404040")
                size_hint_y: None
                height: dp(30)
            TextInput:
                id: regno
                hint_text: "Reg No."
                halign: "center"
                multiline: False
                size_hint_y: None
                height: dp(48)
                background_normal: ""
                background_active: ""
                background_color: get_color_from_hex("#FFFFFF")
                foreground_color: get_color_from_hex("#000000")
                cursor_color: get_color_from_hex("#00537A")
                font_size: "15sp"
                canvas.after:
                    Color:
                        rgba: get_color_from_hex("#000000")
                    Line:
                        rectangle: self.x, self.y, self.width, self.height
                        width: 1
            TextInput:
                id: password
                hint_text: "Password"
                halign: "center"
                password: True
                multiline: False
                size_hint_y: None
                height: dp(48)
                background_normal: ""
                background_active: ""
                background_color: get_color_from_hex("#FFFFFF")
                foreground_color: get_color_from_hex("#000000")
                cursor_color: get_color_from_hex("#00537A")
                font_size: "15sp"
                canvas.after:
                    Color:
                        rgba: get_color_from_hex("#000000")
                    Line:
                        rectangle: self.x, self.y, self.width, self.height
                        width: 1
            Button:
                id: login_btn
                text: "LOGIN"
                size_hint_y: None
                height: dp(48)
                background_normal: ""
                background_color: get_color_from_hex("#A50000")
                color: get_color_from_hex("#FFFFFF")
                font_size: "15sp"
                bold: True
                on_release: root.login(regno.text, password.text)
            Label:
                id: message
                text: root.message
                color: get_color_from_hex("#A50000")
                size_hint_y: None
                height: dp(38)
            Label:
                text: "Reg No: IA/BCS/2026/001  |  Password: student123"
                font_size: "12sp"
                color: get_color_from_hex("#595959")
                size_hint_y: None
                height: dp(30)
            Widget:
                size_hint_y: .18
"""

Builder.load_string(KV_LOGIN)

class LoginScreen(Screen):
    message = StringProperty("")

    def on_enter(self, *args):
        card = self.ids.login_card
        title = self.ids.title_label
        card.opacity = 0
        card.pos_hint = {'center_x': 0.5, 'center_y': 0.44}
        title.opacity = 0
        Animation(opacity=1, pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=0.7, t='out_cubic').start(card)
        Clock.schedule_once(lambda dt: Animation(opacity=1, duration=0.5).start(title), 0.3)

    def login(self, regno, password):
        btn = self.ids.login_btn
        Animation(opacity=0.7, duration=0.08) + Animation(opacity=1, duration=0.08)
        Animation(opacity=0.7, duration=0.08).start(btn)
        student = App.get_running_app().db.authenticate(regno.strip(), password)
        if student:
            app = App.get_running_app()
            app.current_student = student
            self.message = ""
            dashboard = app.root.get_screen("dashboard")
            # Data kutoka database - kila mtu anaona vyake
            dashboard.welcome = student["full_name"]
            dashboard.reg_no = student["reg_no"]
            dashboard.programme_name = student["programme"]
            dashboard.academic_year = student["academic_year"]
            dashboard.semester = student["semester"]
            app.show_home()
            Clock.schedule_once(lambda dt: setattr(app.root, 'current', "dashboard"), 0.25)
        else:
            self.message = "Invalid registration number or password."
            card = self.ids.login_card
            shake = Animation(pos_hint={'center_x': 0.48, 'center_y': 0.5}, duration=0.06) + \
                    Animation(pos_hint={'center_x': 0.52, 'center_y': 0.5}, duration=0.06) + \
                    Animation(pos_hint={'center_x': 0.49, 'center_y': 0.5}, duration=0.06) + \
                    Animation(pos_hint={'center_x': 0.51, 'center_y': 0.5}, duration=0.06) + \
                    Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=0.06)
            shake.start(card)