import json
from .utils import run_cmd

WORDLIST = "/usr/share/wordlists/dirb/common.txt"

def run_ffuf(target):
    url = f"http://{target}/FUZZ"

    cmd = [
        "ffuf",
        "-u", url,
        "-w", WORDLIST,
        "-mc", "200,301,302,403",
        "-of", "json"
    ]

    output = run_cmd(cmd, 120)

    results = []

    try:
        data = json.loads(output)
        for r in data.get("results", []):
            results.append({
                "url": r.get("url"),
                "status": r.get("status")
            })
    except:
        pass

    return results