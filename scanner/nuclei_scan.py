import json
from .utils import run_cmd

def run_nuclei(target):
    cmd = [
        "nuclei",
        "-u", target,
        "-json",
        "-severity", "low,medium,high,critical",
        "-rl", "150",
        "-c", "50"
    ]

    output = run_cmd(cmd, 300)

    findings = []

    for line in output.splitlines():
        try:
            j = json.loads(line)
            findings.append({
                "name": j.get("info", {}).get("name"),
                "severity": j.get("info", {}).get("severity")
            })
        except:
            pass

    return findings