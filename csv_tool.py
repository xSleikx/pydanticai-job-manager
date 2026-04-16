import json
import os
import pandas as pd
from pydantic_ai import RunContext

# JSON Datei laden
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "jobs.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

async def save_tocsv(ctx: RunContext) -> str: 
    for job in data:
        jobtitel = job.get("job_role", "")
        unternehmen = job.get("company", "")
        status_raw = job.get("status", "")
        ort = job.get("location", "")
        anforderungen = job.get("tasks", "").replace("\n", " ").replace("\t", " ")
        link = job.get("link", "")

        # Status & Bewerbungsdatum trennen
        if "applied" in status_raw:
            status = "Beworben"
            beworben = status_raw.replace("applied", "").strip(" ()")
        else:
            status = status_raw
            beworben = ""

        rueckmeldung = ""

        rows.append({
            "Jobtitel": jobtitel,
            "Unternehmen": unternehmen,
            "Status": status,
            "Beworben": beworben,
            "Rückmeldung": rueckmeldung,
            "Ort": ort,
            "Anforderungen": anforderungen,
            "Link": link
        })

    df = pd.DataFrame(rows)

    # CSV speichern
    output_file = os.path.join(script_dir, "copy_jobs.csv")
    df.to_csv(output_file, index=False, encoding="utf-8")

    # print(f"CSV gespeichert unter: {output_file}")
    # result = df.to_string(index=False)
    #    
    return f"{output_file}"