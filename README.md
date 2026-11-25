# Student Management Mobile System (Phase 1)

Python + Kivy + SQLite. This is a learning/demo prototype for a local-first Android student portal.

## Features
- Login with registration number and password
- Student profile
- View assigned courses (no course registration feature)
- Coursework marks
- Examination number/details
- Results and grades
- Fee summary and payment history
- Create a local demo payment reference
- Generate examination permit and payment record PDFs

## Demo account
- Registration number: `IA/BCS/2026/001`
- Password: `student123`

The demo records are sample data. Replace them with authorised institutional records.

## Run on a computer
1. Install Python 3.10 or 3.11.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

SQLite database `student_management.db` is created automatically in the project folder.
Generated PDFs are saved in `generated_documents/`.

## Important limitations
- This phase does not contain Django, a server, or cloud database.
- A locally generated payment reference is NOT an official bank/Government control number and does not confirm payment.
- Real payments require an authorised payment provider/institution integration in a later phase.
- Exam permit and payment PDFs are demo documents, not official institutional documents.
- The demo has student read-only screens. Admin/lecturer/accountant data-entry portals are not included yet.
- Passwords are stored as PBKDF2 hashes, not plain text.
- Forgot-password and account registration are intentionally not enabled: real student accounts should be issued or verified by the institution.

## Android APK (Buildozer)
Buildozer is generally easiest to run on Linux/WSL, not native Windows:
1. Install Buildozer and its Android build dependencies in Ubuntu.
2. In this project directory run `buildozer init`.
3. Edit `buildozer.spec`:
   - `title = Student Management System`
   - `package.name = studentmanagement`
   - `package.domain = org.example`
   - `source.include_exts = py,kv,png,jpg,ttf`
   - `requirements = python3,kivy,reportlab`
   - `orientation = portrait`
4. Run `buildozer android debug`.
5. Install the generated APK on your Android device.

Test on a computer first. Android PDF file access and sharing may need platform-specific handling before production release.
