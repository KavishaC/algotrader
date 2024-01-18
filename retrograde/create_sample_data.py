from chart_maker2 import records
from datetime import datetime, timedelta
import json

dt = datetime.fromisoformat("2023-01-04T18:00:00").date()

vol = []

for record in records:
    for asset in record["assets"]:
        if asset["ticker"] == "AAPL":
            vol.append({
                "date": record["date"],
                "units": asset["units"]
            })
    

with open("volume.json", "w") as json_file:
    json.dump({"volume": vol}, json_file, indent=2)