import requests

def search_cve(product, version):
    if not product:
        return ["No info"]

    query = f"{product} {version}".strip()

    try:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={query}"
        r = requests.get(url, timeout=5)
        data = r.json()

        results = []

        for v in data.get("vulnerabilities", [])[:3]:
            cve = v["cve"]["id"]
            desc = v["cve"]["descriptions"][0]["value"][:120]
            results.append(f"{cve} - {desc}")

        return results or ["No CVE relevante"]

    except:
        return ["Error CVE"]