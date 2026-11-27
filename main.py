from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from database.db import Database
from screens.login_screen import LoginScreen
from screens.dashboard_screen import DashboardScreen
from screens.data_screen import DataScreen
from services.pdf_service import create_exam_permit, create_payment_receipt

class StudentManagementApp(App):
    def build(self):
        self.title = "Student Management System"
        self.db = Database()
        self.current_student = None
        self.current_view = ""
        self.current_payment_id = None

        sm = ScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(DashboardScreen())
        sm.add_widget(DataScreen())
        return sm

    def show_home(self):
        screen = self.root.get_screen("dashboard")
        screen.heading = "Home"
        screen.showing_home = True
        screen.status = ""
        screen.content = (
            "[b]Welcome to Student Management System[/b]\n\n"
            "Access your academic information using the "
            "navigation menu.\n\n"
            "You can view your profile, courses, coursework, "
            "examination details, results and payment information."
        )
        self.current_view = ""

    def show_data(self, section):
        s = self.current_student
        screen = self.root.get_screen("dashboard")
        self.current_view = section
        screen.status = ""
        screen.showing_home = False
        if section == "profile":
            screen.heading = "Student Profile"
            screen.content = (
                f"[b]Full name:[/b] {s['full_name']}\n"
                f"[b]Registration number:[/b] {s['reg_no']}\n"
                f"[b]Programme:[/b] {s['programme']}\n"
                f"[b]Department:[/b] {s['department']}\n"
                f"[b]Academic year:[/b] {s['academic_year']}\n"
                f"[b]Semester:[/b] {s['semester']}"
            )
        elif section == "courses":
            screen.heading = "My Courses"
            rows = self.db.get_courses(s["id"])
            screen.content = "\n".join([
                f"• [b]{r['course_code']}[/b] — "
                f"{r['course_name']} ({r['semester']})"
                for r in rows
            ]) or "No course records."
        elif section == "coursework":
            screen.heading = "Coursework"
            rows = self.db.get_coursework(s["id"])
            screen.content = "\n".join([
                f"[b]{r['course_code']} — {r['course_name']}[/b]\n"
                f"Assignment: {r['assignment']} | "
                f"Test: {r['test']} | "
                f"Practical: {r['practical']} | "
                f"Total: {r['total']}"
                for r in rows
            ]) or "No coursework records."
        elif section == "examination":
            screen.heading = "Examination Details"
            rows = self.db.get_exam(s["id"])
            screen.content = "\n".join([
                f"[b]{r['exam_name']}[/b]\n"
                f"Exam number: {r['exam_number']}\n"
                f"Date: {r['exam_date']}\n"
                f"Venue: {r['venue']}"
                for r in rows
            ]) or "No examination details."
        elif section == "results":
            screen.heading = "Semester Results"
            rows = self.db.get_results(s["id"])
            screen.content = "\n".join([
                f"[b]{r['course_code']} — {r['course_name']}[/b]\n"
                f"Coursework: {r['coursework']} | "
                f"Examination: {r['exam_mark']} | "
                f"Total: {r['total']} | "
                f"Grade: {r['grade']}"
                for r in rows
            ]) or "No results published."
        elif section == "payments":
            screen.heading = "Fees and Payment History"
            summary = self.db.fee_summary(s["id"])
            rows = self.db.get_payments(s["id"])
            history = "\n".join([
                f"{r['created_at']} | "
                f"TZS {r['amount']:,.0f} | "
                f"{r['control_number']} | "
                f"{r['status']}"
                for r in rows
            ])
            screen.content = (
                f"[b]Total fees:[/b] TZS {summary['total']:,.0f}\n"
                f"[b]Paid:[/b] TZS {summary['paid']:,.0f}\n"
                f"[b]Balance:[/b] TZS {summary['balance']:,.0f}\n\n"
                f"[b]Payment requests/history[/b]\n"
                f"{history or 'No payment records.'}\n\n"
                "Note: Control numbers in this demo are local "
                "references only. They are not bank/government "
                "payment control numbers."
            )

    def make_payment_request(self):
        payment_id, control = self.db.create_payment(
            self.current_student["id"], 100000
        )
        self.current_payment_id = payment_id
        self.show_data("payments")
        self.root.get_screen("dashboard").status = (
            f"Demo payment request created: {control} (TZS 100,000)"
        )

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
            self.root.get_screen("dashboard").status = f"PDF created: {path}"
        except Exception as exc:
            self.root.get_screen("dashboard").status = str(exc)

    def logout(self):
        self.current_student = None
        self.current_view = ""
        d = self.root.get_screen("dashboard")
        d.welcome = ""
        d.reg_no = ""
        d.programme_name = ""
        d.academic_year = ""
        d.semester = ""
        self.root.current = "login"

    def on_stop(self):
        self.db.close()

if __name__ == "__main__":
    StudentManagementApp().run()