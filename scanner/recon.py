import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def headers(target):
    try:
        try:
            r = requests.get(f"https://{target}", timeout=5, verify=False)
        except:
            r = requests.get(f"http://{target}", timeout=5)

        h = r.headers

        issues = []
        if "X-Frame-Options" not in h:
            issues.append("No XFO")
        if "Content-Security-Policy" not in h:
            issues.append("No CSP")

        return {"server": h.get("Server"), "issues": issues or ["OK"]}
    except:
        return {"server":"", "issues":["error"]}


def fingerprint(h):
    tech = []
    s = str(h.get("server","")).lower()

    if "apache" in s: tech.append("Apache")
    if "nginx" in s: tech.append("Nginx")

    return tech