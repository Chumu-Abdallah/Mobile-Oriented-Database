import sqlite3
import hashlib
import secrets
from datetime import datetime

DB_NAME = "student_management.db"

def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200000).hex()
    return salt, digest

class Database:
    def __init__(self, path=DB_NAME):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        self.seed_demo_data()

    def create_tables(self):
        self.conn.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            programme TEXT NOT NULL,
            department TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            semester TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER UNIQUE NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL,
            course_name TEXT NOT NULL,
            semester TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS student_courses (
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            PRIMARY KEY(student_id, course_id),
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
        );
        CREATE TABLE IF NOT EXISTS coursework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            assignment REAL DEFAULT 0,
            test REAL DEFAULT 0,
            practical REAL DEFAULT 0,
            total REAL DEFAULT 0,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
        );
        CREATE TABLE IF NOT EXISTS examinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            exam_name TEXT NOT NULL,
            exam_number TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            venue TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        );
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            coursework REAL DEFAULT 0,
            exam_mark REAL DEFAULT 0,
            total REAL DEFAULT 0,
            grade TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
        );
        CREATE TABLE IF NOT EXISTS fee_structures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            total_fee REAL NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            control_number TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            created_at TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        );
        """)
        self.conn.commit()

    def seed_demo_data(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM students WHERE reg_no=?", ("IA/BCS/2026/001",))
        if cur.fetchone():
            return
        cur.execute("""INSERT INTO students(reg_no,full_name,programme,department,academic_year,semester)
                       VALUES(?,?,?,?,?,?)""",
                    ("IA/BCS/2026/001", "Chumu", "Bachelor of Computer Science",
                     "Computer Science", "2026/2027", "Semester I"))
        sid = cur.lastrowid
        salt, digest = hash_password("student123")
        cur.execute("INSERT INTO users(student_id,salt,password_hash) VALUES(?,?,?)", (sid,salt,digest))
        course_data = [
            ("CS101", "Object Oriented Programming", "Semester I"),
            ("CS102", "Database Systems", "Semester I"),
            ("CS103", "Computer Networks", "Semester I"),
        ]
        for code, name, sem in course_data:
            cur.execute("INSERT INTO courses(course_code,course_name,semester) VALUES(?,?,?)", (code,name,sem))
            cid = cur.lastrowid
            cur.execute("INSERT INTO student_courses(student_id,course_id) VALUES(?,?)", (sid,cid))
            cw = {"CS101": (16,18,8,42), "CS102": (15,17,8,40), "CS103": (14,16,7,37)}[code]
            cur.execute("""INSERT INTO coursework(student_id,course_id,assignment,test,practical,total)
                           VALUES(?,?,?,?,?,?)""", (sid,cid,*cw))
            exam = {"CS101": 48, "CS102": 45, "CS103": 43}[code]
            total = cw[3] + exam
            grade = "A" if total >= 80 else "B" if total >= 70 else "C" if total >= 60 else "D" if total >= 50 else "F"
            cur.execute("""INSERT INTO results(student_id,course_id,coursework,exam_mark,total,grade)
                           VALUES(?,?,?,?,?,?)""", (sid,cid,cw[3],exam,total,grade))
        cur.execute("""INSERT INTO examinations(student_id,exam_name,exam_number,exam_date,venue)
                       VALUES(?,?,?,?,?)""", (sid,"Semester I Examination","EX-2026-0001","2026-12-01","Main Examination Hall"))
        cur.execute("INSERT INTO fee_structures(student_id,total_fee) VALUES(?,?)", (sid,1500000))
        cur.execute("""INSERT INTO payments(student_id,amount,control_number,status,created_at)
                       VALUES(?,?,?,?,?)""", (sid,800000,"DEMO-PAID-0001","PAID",datetime.now().isoformat(timespec="minutes")))
        self.conn.commit()

    def authenticate(self, reg_no, password):
        row = self.conn.execute("""
            SELECT s.*, u.salt, u.password_hash FROM students s
            JOIN users u ON u.student_id=s.id WHERE s.reg_no=?
        """, (reg_no,)).fetchone()
        if not row:
            return None
        _, digest = hash_password(password, row["salt"])
        if secrets.compare_digest(digest, row["password_hash"]):
            return dict(row)
        return None

    def get_courses(self, sid):
        return self.conn.execute("""SELECT c.* FROM courses c JOIN student_courses sc
            ON sc.course_id=c.id WHERE sc.student_id=? ORDER BY c.course_code""", (sid,)).fetchall()

    def get_coursework(self, sid):
        return self.conn.execute("""SELECT c.course_code,c.course_name,w.assignment,w.test,w.practical,w.total
            FROM coursework w JOIN courses c ON c.id=w.course_id WHERE w.student_id=?""", (sid,)).fetchall()

    def get_exam(self, sid):
        return self.conn.execute("SELECT * FROM examinations WHERE student_id=?", (sid,)).fetchall()

    def get_results(self, sid):
        return self.conn.execute("""SELECT c.course_code,c.course_name,r.coursework,r.exam_mark,r.total,r.grade
            FROM results r JOIN courses c ON c.id=r.course_id WHERE r.student_id=?""", (sid,)).fetchall()

    def fee_summary(self, sid):
        total = self.conn.execute("SELECT COALESCE(SUM(total_fee),0) FROM fee_structures WHERE student_id=?", (sid,)).fetchone()[0]
        paid = self.conn.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE student_id=? AND status='PAID'", (sid,)).fetchone()[0]
        return {"total": total, "paid": paid, "balance": max(total-paid,0)}

    def get_payments(self, sid):
        return self.conn.execute("SELECT * FROM payments WHERE student_id=? ORDER BY id DESC", (sid,)).fetchall()

    def create_payment(self, sid, amount):
        # Local demo reference only; not a valid bank/government control number.
        control = "LOCAL-" + secrets.token_hex(5).upper()
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO payments(student_id,amount,control_number,status,created_at)
                       VALUES(?,?,?,?,?)""", (sid, amount, control, "PENDING", datetime.now().isoformat(timespec="minutes")))
        self.conn.commit()
        return cur.lastrowid, control

    def close(self):
        self.conn.close()
