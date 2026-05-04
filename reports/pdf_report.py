from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

os.makedirs("reports", exist_ok=True)

def generate_pdf(scan_id, data):
    path = f"reports/{scan_id}.pdf"

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("BBScanner Report", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"IP: {data.get('ip')}", styles["Normal"]))
    elements.append(Paragraph(f"Tech: {', '.join(data.get('tech', []))}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    for p in data.get("ports", []):
        elements.append(Paragraph(f"{p['port']} - {p['service']}", styles["Normal"]))

    for v in data.get("vulns", []):
        elements.append(Paragraph(f"[{v['severity']}] {v['name']}", styles["Normal"]))

    elements.append(Paragraph("Critical Findings:", styles["Heading2"]))

    for p in data.get("ports", []):
       port = p["port"]

    if port == "21":
        elements.append(Paragraph("FTP abierto → riesgo de acceso no autorizado", styles["Normal"]))

    if port == "25":
        elements.append(Paragraph("SMTP expuesto → posible relay o enumeración", styles["Normal"]))

    if port == "3306":
        elements.append(Paragraph("MySQL expuesto → riesgo crítico si no protegido", styles["Normal"]))

    doc.build(elements)
    return path