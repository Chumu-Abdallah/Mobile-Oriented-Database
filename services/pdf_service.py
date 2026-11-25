from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

OUTPUT_DIR = Path("generated_documents")

def _new_pdf(filename, title):
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    c.setTitle(title)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(25*mm, height-30*mm, title)
    c.setFont("Helvetica", 10)
    c.drawString(25*mm, height-38*mm, "STUDENT MANAGEMENT SYSTEM - DEMO DOCUMENT")
    c.line(25*mm, height-42*mm, width-25*mm, height-42*mm)
    return c, path, height

def create_exam_permit(student, exams):
    c, path, height = _new_pdf("examination_permit.pdf", "EXAMINATION PERMIT")
    y = height - 65*mm
    values = [
        ("Student name", student["full_name"]),
        ("Registration number", student["reg_no"]),
        ("Programme", student["programme"]),
        ("Department", student["department"]),
    ]
    for label, value in values:
        c.drawString(25*mm, y, f"{label}: {value}")
        y -= 10*mm
    y -= 8*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25*mm, y, "Examination details")
    y -= 10*mm
    c.setFont("Helvetica", 10)
    for exam in exams:
        for label, value in [("Examination", exam["exam_name"]), ("Examination number", exam["exam_number"]),
                             ("Date", exam["exam_date"]), ("Venue", exam["venue"])]:
            c.drawString(25*mm, y, f"{label}: {value}")
            y -= 9*mm
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(25*mm, 20*mm, "Demo document. An institution must verify and officially issue examination permits.")
    c.save()
    return str(path)

def create_payment_receipt(student, payment):
    c, path, height = _new_pdf("payment_record.pdf", "PAYMENT RECORD")
    y = height - 65*mm
    values = [
        ("Student name", student["full_name"]),
        ("Registration number", student["reg_no"]),
        ("Amount", f"TZS {payment['amount']:,.0f}"),
        ("Reference number", payment["control_number"]),
        ("Status", payment["status"]),
        ("Date", payment["created_at"]),
    ]
    for label, value in values:
        c.drawString(25*mm, y, f"{label}: {value}")
        y -= 11*mm
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(25*mm, 20*mm, "This is a locally generated demo record, not proof of bank payment.")
    c.save()
    return str(path)
