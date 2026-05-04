import xml.etree.ElementTree as ET
from .utils import run_cmd

def run_nmap(target):
    cmd = ["nmap", "-Pn", "-sV", "-T4", "-oX", "-", target]
    output = run_cmd(cmd)

    ports = []

    try:
        root = ET.fromstring(output)
        for p in root.iter("port"):
            if p.find("state").get("state") == "open":
                svc = p.find("service")
                ports.append({
                    "port": p.get("portid"),
                    "service": svc.get("name"),
                    "product": svc.get("product") or "",
                    "version": svc.get("version") or ""
                })
    except:
        pass

    return ports