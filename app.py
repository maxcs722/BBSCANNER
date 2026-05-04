from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
from concurrent.futures import ThreadPoolExecutor
import socket

from scanner.utils import validate_target
from scanner.nmap_scan import run_nmap
from scanner.nuclei_scan import run_nuclei
from scanner.recon import headers, fingerprint
from scanner.fuzz import run_ffuf
from scanner.ai import classify_endpoint
from reports.pdf_report import generate_pdf

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

executor = ThreadPoolExecutor(max_workers=5)
scans = {}

def log(msg):
    socketio.emit("log", {"msg": msg})

def run_scan(target):
    try:
        scans[target] = {"status": "running"}

        log("Resolviendo dominio...")
        ip = socket.gethostbyname(target)
        socketio.emit("info", {"ip": ip})

        log("Nmap...")
        ports = run_nmap(target)
        socketio.emit("ports", ports)

        log("Headers...")
        hdr = headers(target)
        tech = fingerprint(hdr)
        socketio.emit("tech", tech)

        log("Nuclei...")
        vulns = run_nuclei(target)
        socketio.emit("vulns", vulns)

        log("Fuzzing...")
        raw = run_ffuf(target)

        fuzz, alerts = [], []

        for f in raw:
            t, sev = classify_endpoint(f["url"])
            item = {
                "url": f["url"],
                "status": f["status"],
                "type": t,
                "severity": sev
            }
            fuzz.append(item)
            if sev in ["high", "critical"]:
                alerts.append(item)

        socketio.emit("fuzz", fuzz)
        socketio.emit("alerts", alerts)

        result = {
            "ip": ip,
            "ports": ports,
            "tech": tech,
            "vulns": vulns,
            "fuzz": fuzz,
            "alerts": alerts
        }

        scans[target] = {
            "status": "done",
            "result": result
        }

        # ===== PDF AUTOMÁTICO =====
        try:
            pdf_path = generate_pdf(target, result)
            scans[target]["pdf"] = pdf_path
            log("PDF generado")
        except Exception as e:
            log(f"PDF error: {str(e)}")

        log("Scan completado")

    except Exception as e:
        scans[target] = {"status": "error"}
        log(f"ERROR: {str(e)}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pdf/<target>")
def pdf(target):
    scan = scans.get(target)

    if not scan or scan.get("status") != "done":
        return "Scan no listo"

    path = scan.get("pdf") or generate_pdf(target, scan["result"])
    return send_file(path, as_attachment=True)

@socketio.on("start_scan")
def start_scan(data):
    target = data.get("target")

    try:
        target = validate_target(target)
    except Exception as e:
        emit("log", {"msg": str(e)})
        return

    executor.submit(run_scan, target)

if __name__ == "__main__":
    socketio.run(app, debug=True)