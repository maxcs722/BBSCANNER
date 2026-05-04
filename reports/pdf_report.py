from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

os.makedirs("reports", exist_ok=True)

def generate_pdf(scan_id, data):
    path = f"reports/{scan_id}.pdf"
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path)

    elements = []

    # TITLE
    elements.append(Paragraph("BBScanner AI Hunter Report", styles["Title"]))
    elements.append(Spacer(1,10))

    # SUMMARY
    elements.append(Paragraph(
        "Resumen: Se detectaron servicios expuestos que podrían representar riesgos de seguridad.",
        styles["Normal"]
    ))
    elements.append(Spacer(1,10))

    # INFO
    elements.append(Paragraph(f"IP: {data.get('ip')}", styles["Normal"]))
    elements.append(Spacer(1,10))

    # PORTS
    elements.append(Paragraph("Servicios detectados:", styles["Heading2"]))
    for p in data.get("ports", []):
        elements.append(Paragraph(
            f"{p['port']} - {p['service']} ({p.get('product','')})",
            styles["Normal"]
        ))

    elements.append(Spacer(1,10))

    # ===== INTELIGENCIA =====
    elements.append(Paragraph("Critical Findings:", styles["Heading2"]))

    risk = 0

    for p in data.get("ports", []):
        port = p["port"]

        if port == "3306":
            elements.append(Paragraph(
                "MySQL expuesto → riesgo crítico de acceso a base de datos",
                styles["Normal"]
            ))
            risk += 4

        if port == "21":
            elements.append(Paragraph(
                "FTP abierto → posible acceso no autorizado",
                styles["Normal"]
            ))
            risk += 2

        if port == "2121":
            elements.append(Paragraph(
                "FTP en puerto no estándar → evasión de controles",
                styles["Normal"]
            ))
            risk += 2

        if port == "25":
            elements.append(Paragraph(
                "SMTP expuesto → posible relay o enumeración",
                styles["Normal"]
            ))
            risk += 2

    elements.append(Spacer(1,10))

    # SCORE
    elements.append(Paragraph(f"Risk Score: {risk}/10", styles["Heading2"]))

    elements.append(Spacer(1,10))

    # IMPACT
    elements.append(Paragraph("Impacto:", styles["Heading2"]))
    elements.append(Paragraph(
        "Un atacante podría acceder a servicios internos, exfiltrar datos o comprometer el sistema.",
        styles["Normal"]
    ))

    doc.build(elements)
    return path