def classify_endpoint(url):
    url = url.lower()

    if "admin" in url:
        return ("admin panel", "high")

    if "login" in url:
        return ("login page", "medium")

    if "api" in url:
        return ("api endpoint", "medium")

    if ".env" in url or "config" in url:
        return ("sensitive file", "critical")

    if "backup" in url or ".zip" in url:
        return ("backup file", "critical")

    return ("unknown", "low")