import requests
import json
import os
from datetime import datetime

# Hakee tilastot API:sta ja tallentaa data/-kansioon

BASE_URL = "https://api.pesistulokset.fi/api/v1/stats-tool/players"

HAUT = [
    {
        "nimi": "2025_naisten_superpesis_karkilyonnit",
        "params": {
            "seasonSeries": "1956",
            "season": "109",
            "phase": "1",
            "level": "1",
            "series": "2",
            "sum": "true",
            "statfilter": "karkilyonnit_pesavaleittain",
            "columns": "matches,batpe_succeeded_0,batpe_tries_0,batpe_percent_0,batpe_succeeded_1,batpe_tries_1,batpe_percent_1,batpe_succeeded_2,batpe_tries_2,batpe_percent_2,batpe_succeeded_3,batpe_tries_3,batpe_percent_3,batpe_total_succeeded,batpe_total_tries,batpe_total_percent"
        }
    }
]

def hae_tilastot():
    os.makedirs("data", exist_ok=True)
    paivitetty = []

    for haku in HAUT:
        print(f"Haetaan: {haku['nimi']}...")
        try:
            r = requests.get(BASE_URL, params=haku["params"], timeout=15)
            r.raise_for_status()
            data = r.json()

            tiedosto = f"data/{haku['nimi']}.json"
            with open(tiedosto, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"  Tallennettu: {tiedosto}")
            paivitetty.append(haku["nimi"])

        except Exception as e:
            print(f"  Virhe: {e}")

    meta = {
        "paivitetty": datetime.now().isoformat(),
        "tiedostot": paivitetty
    }
    with open("data/meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\nValmis! {len(paivitetty)} tilastoa haettu.")

if __name__ == "__main__":
    hae_tilastot()