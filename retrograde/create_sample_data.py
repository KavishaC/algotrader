from chart_maker2 import records
from datetime import datetime, timedelta
import json

dt = datetime.fromisoformat("2023-01-04T18:00:00").date()

for record in records:
    record["date"] = dt.isoformat()
    record.pop("datetime")
    dt += timedelta(days=1)

with open("output_daily.json", "w") as json_file:
    json.dump({"records": records}, json_file, indent=2)