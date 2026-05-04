import re, socket, subprocess

def validate_target(target):
    if not re.match(r"^[a-zA-Z0-9.-]+$", target):
        raise ValueError("Target inválido")

    ip = socket.gethostbyname(target)

    blocked = ["127.", "10.", "192.168", "172.16"]
    if any(ip.startswith(b) for b in blocked):
        raise ValueError("SSRF bloqueado")

    return target


def run_cmd(cmd, timeout=180):
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        return result.stdout
    except:
        return ""


def severity_score(sev):
    return {"critical":4,"high":3,"medium":2,"low":1}.get(sev,0)