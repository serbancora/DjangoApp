import json
from myapp.models import Ierarhie
from pathlib import Path

def importa_nod(nod_json, parinte=None):
    nume = nod_json["nume"]
    obiect = Ierarhie.objects.create(nume=nume, parinte=parinte)
    for copil in nod_json.get("copii", []):
        importa_nod(copil, obiect)

def run():
    cale = Path("ierarhie_anki.json")
    with open(cale, encoding="utf-8") as f:
        date = json.load(f)
        importa_nod(date)

if __name__ == "__main__":
    run()
