from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from concurrent.futures import ThreadPoolExecutor
import socket

from scanner.utils import validate_target
from scanner.nmap_scan import run_nmap
from scanner.nuclei_scan import run_nuclei
from scanner.recon import headers, fingerprint
from scanner.fuzz import run_ffuf
from scanner.ai import classify_endpoint

# ===== INIT =====
app = Flask(__name__)

# 🔥 WebSocket (elige uno)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

executor = ThreadPoolExecutor(max_workers=5)

# ===== LOG STREAM =====
def log(msg):
    socketio.emit("log", {"msg": msg})

# ===== SCAN =====
def run_scan(target):
    try:
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

        fuzz = []
        alerts = []

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

        log("Scan completado")

    except Exception as e:
        log(f"ERROR: {str(e)}")

# ===== ROUTES =====
@app.route("/")
def home():
    return render_template("index.html")

# ===== SOCKET EVENT =====
@socketio.on("start_scan")
def start_scan(data):
    target = data.get("target")

    try:
        target = validate_target(target)
    except Exception as e:
        emit("log", {"msg": str(e)})
        return

    executor.submit(run_scan, target)

# ===== RUN =====
if __name__ == "__main__":
    socketio.run(app, debug=True)