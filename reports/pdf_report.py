from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(path, data):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path)

    elements = []

    # ===== TITLE =====
    elements.append(Paragraph("BBScanner AI Hunter Report", styles["Title"]))
    elements.append(Spacer(1, 10))

    # ===== BASIC INFO =====
    elements.append(Paragraph(f"IP: {data.get('ip','N/A')}", styles["Normal"]))
    elements.append(Paragraph(f"Tech: {', '.join(data.get('tech',[]))}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    # ===== PORTS =====
    elements.append(Paragraph("Open Ports:", styles["Heading2"]))

    ports = data.get("ports", [])
    if ports:
        for p in ports:
            elements.append(Paragraph(
                f"{p['port']} - {p['service']} ({p.get('product','')})",
                styles["Normal"]
            ))
    else:
        elements.append(Paragraph("No ports found", styles["Normal"]))

    elements.append(Spacer(1, 10))

    # ===== ALERTS =====
    elements.append(Paragraph("Critical Alerts:", styles["Heading2"]))

    alerts = data.get("alerts", [])
    if alerts:
        for a in alerts:
            elements.append(Paragraph(
                f"[{a['severity']}] {a['type']} → {a['url']}",
                styles["Normal"]
            ))
    else:
        elements.append(Paragraph("No critical alerts", styles["Normal"]))

    elements.append(Spacer(1, 10))

    # ===== VULNS =====
    elements.append(Paragraph("Vulnerabilities:", styles["Heading2"]))

    vulns = data.get("vulns", [])
    if vulns:
        for v in vulns:
            elements.append(Paragraph(
                f"[{v['severity']}] {v['name']}",
                styles["Normal"]
            ))
    else:
        elements.append(Paragraph("No vulnerabilities found", styles["Normal"]))

    elements.append(Spacer(1, 10))

    # ===== FUZZ =====
    elements.append(Paragraph("Discovered Endpoints:", styles["Heading2"]))

    fuzz = data.get("fuzz", [])
    if fuzz:
        for f in fuzz[:20]:  # limitar
            elements.append(Paragraph(
                f"[{f['status']}] {f['url']}",
                styles["Normal"]
            ))
    else:
        elements.append(Paragraph("No endpoints found", styles["Normal"]))

    doc.build(elements)