import csv

def generate_csv(path, data):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)

        w.writerow(["Tipo", "Dato"])

        for p in data["ports"]:
            w.writerow(["Puerto", f"{p['port']} {p['service']}"])

        for v in data["nuclei"]:
            w.writerow(["VULN", f"{v['severity']} {v['name']}"])