import sys
from scanner.utils import validate_target
from scanner.nmap_scan import run_nmap
from scanner.nuclei_scan import run_nuclei
from scanner.recon import subdomains, headers
from scanner.cve import search_cve

def run(target):
    target = validate_target(target)

    print("[*] Subdomains...")
    subs = subdomains(target)

    print("[*] Nmap...")
    ports = run_nmap(target)

    for p in ports:
        p["cves"] = search_cve(p["product"], p["version"])

    print("[*] Headers...")
    hdr = headers(target)

    print("[*] Nuclei...")
    vulns = run_nuclei(target)

    print("\n=== RESULTADOS ===")
    print("Subdominios:", subs[:5])
    print("Puertos:", ports)
    print("Headers:", hdr)
    print("Vulns:", vulns[:5])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python cli.py ejemplo.com")
    else:
        run(sys.argv[1])