from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from database.db import Database
from services.pdf_service import create_exam_permit, create_payment_receipt

KV = r"""
#:import dp kivy.metrics.dp
<LoginScreen>:
    name: "login"
    BoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(12)
        canvas.before:
            Color:
                rgba: .95, .97, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Widget:
            size_hint_y: .5
        Label:
            text: "[b]STUDENT MENAGEMENT APP[/b]"
            markup: True
            font_size: "27sp"
            color: .08, .18, .35, 1
            size_hint_y: None
            height: dp(55)
        Label:
            text: "Sign in using your registration number"
            color: .25, .3, .4, 1
            size_hint_y: None
            height: dp(30)
        TextInput:
            id: regno
            hint_text: "Reg No."
            halign: "center"
            multiline: False
            size_hint_y: None
            height: dp(48)
        TextInput:
            id: password
            hint_text: "Password"
            halign: "center"
            password: True
            multiline: False
            size_hint_y: None
            height: dp(48)
        Button:
            text: "LOGIN"
            size_hint_y: None
            height: dp(48)
            background_normal: ""
            background_color: .1, .35, .72, 1
            on_release: root.login(regno.text, password.text)
        Label:
            id: message
            text: root.message
            color: .8, .1, .1, 1
            size_hint_y: None
            height: dp(38)
        Label:
            text: "Reg No: IA/BCS/2026/001  |  Password: student123"
            font_size: "12sp"
            color: .35, .4, .48, 1
            size_hint_y: None
            height: dp(30)
        Widget:
            size_hint_y: .5

<DashboardScreen>:
    name: "dashboard"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)
        Label:
            text: "[b]DASHBOARD[/b]"
            markup: True
            font_size: "23sp"
            size_hint_y: None
            height: dp(48)
            color: .08, .18, .35, 1
        Label:
            text: root.welcome
            size_hint_y: None
            height: dp(32)
            color: .2, .25, .35, 1
        ScrollView:
            GridLayout:
                cols: 2
                spacing: dp(10)
                padding: dp(2)
                size_hint_y: None
                height: self.minimum_height
                Button:
                    text: "My Profile"
                    on_release: app.show_data("profile")
                Button:
                    text: "My Courses"
                    on_release: app.show_data("courses")
                Button:
                    text: "Coursework"
                    on_release: app.show_data("coursework")
                Button:
                    text: "Examination"
                    on_release: app.show_data("examination")
                Button:
                    text: "Results"
                    on_release: app.show_data("results")
                Button:
                    text: "Fees & Payments"
                    on_release: app.show_data("payments")
                Button:
                    text: "Generate Control Number"
                    on_release: app.make_payment_request()
                Button:
                    text: "Logout"
                    on_release: app.logout()

<DataScreen>:
    name: "data"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)
        Label:
            text: root.heading
            font_size: "22sp"
            bold: True
            color: .08, .18, .35, 1
            size_hint_y: None
            height: dp(45)
        ScrollView:
            Label:
                id: body
                text: root.content
                markup: True
                color: .12, .16, .22, 1
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1] + dp(20)
                halign: "left"
                valign: "top"
        Button:
            text: "Download PDF"
            size_hint_y: None
            height: dp(46)
            on_release: app.download_pdf()
        Button:
            text: "Back to Dashboard"
            size_hint_y: None
            height: dp(46)
            on_release: app.root.current = "dashboard"
        Label:
            id: status
            text: root.status
            size_hint_y: None
            height: dp(28)
            color: .1, .4, .2, 1
"""

class LoginScreen(Screen):
    message = StringProperty("")
    def login(self, regno, password):
        student = App.get_running_app().db.authenticate(regno.strip(), password)
        if student:
            app = App.get_running_app()
            app.current_student = student
            self.message = ""
            app.root.get_screen("dashboard").welcome = f"Welcome, {student['full_name']}"
            app.root.current = "dashboard"
        else:
            self.message = "Invalid registration number or password."

class DashboardScreen(Screen):
    welcome = StringProperty("Welcome")

class DataScreen(Screen):
    heading = StringProperty("")
    content = StringProperty("")
    status = StringProperty("")

class StudentManagementApp(App):
    def build(self):
        self.title = "Student Management System"
        self.db = Database()
        self.current_student = None
        self.current_view = ""
        self.current_payment_id = None
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(DashboardScreen())
        sm.add_widget(DataScreen())
        return sm

    def show_data(self, section):
        s = self.current_student
        screen = self.root.get_screen("data")
        self.current_view = section
        screen.status = ""
        if section == "profile":
            screen.heading = "Student Profile"
            screen.content = (
                f"[b]Full name:[/b] {s['full_name']}\\n"
                f"[b]Registration number:[/b] {s['reg_no']}\\n"
                f"[b]Programme:[/b] {s['programme']}\\n"
                f"[b]Department:[/b] {s['department']}\\n"
                f"[b]Academic year:[/b] {s['academic_year']}\\n"
                f"[b]Semester:[/b] {s['semester']}"
            )
        elif section == "courses":
            screen.heading = "My Courses"
            rows = self.db.get_courses(s["id"])
            screen.content = "\\n".join([f"• [b]{r['course_code']}[/b] — {r['course_name']} ({r['semester']})" for r in rows]) or "No course records."
        elif section == "coursework":
            screen.heading = "Coursework"
            rows = self.db.get_coursework(s["id"])
            screen.content = "\\n".join([f"[b]{r['course_code']} — {r['course_name']}[/b]\\nAssignment: {r['assignment']} | Test: {r['test']} | Practical: {r['practical']} | Total: {r['total']}" for r in rows]) or "No coursework records."
        elif section == "examination":
            screen.heading = "Examination Details"
            rows = self.db.get_exam(s["id"])
            screen.content = "\\n".join([f"[b]{r['exam_name']}[/b]\\nExam number: {r['exam_number']}\\nDate: {r['exam_date']}\\nVenue: {r['venue']}" for r in rows]) or "No examination details."
        elif section == "results":
            screen.heading = "Semester Results"
            rows = self.db.get_results(s["id"])
            screen.content = "\\n".join([f"[b]{r['course_code']} — {r['course_name']}[/b]\\nCoursework: {r['coursework']} | Examination: {r['exam_mark']} | Total: {r['total']} | Grade: {r['grade']}" for r in rows]) or "No results published."
        elif section == "payments":
            screen.heading = "Fees and Payment History"
            summary = self.db.fee_summary(s["id"])
            rows = self.db.get_payments(s["id"])
            history = "\\n".join([f"{r['created_at']} | TZS {r['amount']:,.0f} | {r['control_number']} | {r['status']}" for r in rows])
            screen.content = (f"[b]Total fees:[/b] TZS {summary['total']:,.0f}\\n"
                              f"[b]Paid:[/b] TZS {summary['paid']:,.0f}\\n"
                              f"[b]Balance:[/b] TZS {summary['balance']:,.0f}\\n\\n"
                              f"[b]Payment requests/history[/b]\\n{history or 'No payment records.'}\\n\\n"
                              "Note: Control numbers in this demo are local references only. They are not bank/government payment control numbers.")
        self.root.current = "data"

    def make_payment_request(self):
        # Demo amount; production UI should request and validate the amount.
        payment_id, control = self.db.create_payment(self.current_student["id"], 100000)
        self.current_payment_id = payment_id
        self.show_data("payments")
        self.root.get_screen("data").status = f"Demo payment request created: {control} (TZS 100,000)"

    def download_pdf(self):
        s = self.current_student
        try:
            if self.current_view == "examination":
                rows = self.db.get_exam(s["id"])
                if not rows:
                    raise ValueError("No examination number is available.")
                path = create_exam_permit(s, rows)
            elif self.current_view == "payments":
                rows = self.db.get_payments(s["id"])
                if not rows:
                    raise ValueError("No payment record is available.")
                path = create_payment_receipt(s, rows[0])
            else:
                raise ValueError("PDF is available on Examination or Fees & Payments pages.")
            self.root.get_screen("data").status = f"PDF created: {path}"
        except Exception as exc:
            self.root.get_screen("data").status = str(exc)

    def logout(self):
        self.current_student = None
        self.root.current = "login"

    def on_stop(self):
        self.db.close()

if __name__ == "__main__":
    StudentManagementApp().run()
