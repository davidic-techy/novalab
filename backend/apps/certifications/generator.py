import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from django.utils import timezone

class CertificateGenerator:
    """
    Generates a PDF certificate in memory.
    """
    
    @staticmethod
    def generate(certificate):
        """
        Draws the PDF and returns the binary data (bytes).
        """
        buffer = io.BytesIO()
        
        # 1. Setup Canvas (Landscape Mode)
        p = canvas.Canvas(buffer, pagesize=landscape(letter))
        width, height = landscape(letter)
        
        # 2. Draw Border
        p.setStrokeColor(colors.darkblue)
        p.setLineWidth(5)
        p.rect(30, 30, width-60, height-60)
        
        # 3. Header
        p.setFont("Helvetica-Bold", 36)
        p.drawCentredString(width / 2, height - 100, "CERTIFICATE OF COMPLETION")
        
        p.setFont("Helvetica", 18)
        p.drawCentredString(width / 2, height - 140, "This is to certify that")
        
        # 4. Student Name
        p.setFont("Helvetica-Bold", 30)
        p.setFillColor(colors.darkblue)
        student_name = f"{certificate.user.first_name} {certificate.user.last_name}".upper()
        p.drawCentredString(width / 2, height - 200, student_name)
        
        # 5. Course Details
        p.setFillColor(colors.black)
        p.setFont("Helvetica", 18)
        p.drawCentredString(width / 2, height - 250, "Has successfully completed the course")
        
        p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(width / 2, height - 290, certificate.course.title)
        
        # 6. Footer (Date & ID)
        p.setFont("Helvetica", 12)
        date_str = certificate.issued_at.strftime("%B %d, %Y")
        p.drawString(50, 50, f"Date: {date_str}")
        
        p.drawRightString(width - 50, 50, f"ID: {str(certificate.id)}")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return buffer