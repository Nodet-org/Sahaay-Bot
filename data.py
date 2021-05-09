import json
import requests
from datetime import datetime
import uuid

OXYGEN_DATA = "https://raw.githubusercontent.com/coronasafe/life/main/data/oxygen_v2.json"
AMBULANCE_DATA = "https://raw.githubusercontent.com/coronasafe/life/main/data/ambulance_v2.json"
FOOD_DATA = "https://raw.githubusercontent.com/coronasafe/life/main/data/food_v2.json"

final_data = {}
last_date = datetime.strptime("4/30/2021", "%m/%d/%Y")

def get_JSON_data(row):
    global final_data
    r_id = str(uuid.uuid4())
    phone = ""
    is_verified = "Pending"
    if "verification_status" in row:
        is_verified = row["verification_status"] if not row["verification_status"] == "" else "Pending"
    if len(row["phone_1"]) > 9:
        phone = "phone_1"
    elif len(row["phone_2"]) > 9:
        phone = "phone_2"
    if not phone == "":
        newResource = {
            "id": r_id,
            "phone": row[phone],
            "name": row["title"],
            "isVerified": is_verified,
            "reports": 0,
            "price": -1,
            "quantity": -1,
            "date": -1,
            "time": -1
        }
        row["district"] = row["district"].lower()
        if row["district"] in final_data:
            if row["category"] in final_data[row["district"]]:
                if r_id in final_data[row["district"]][row["category"]]:
                    final_data[row["district"]][row["category"]][r_id] = newResource
                else:
                    final_data[row["district"]][row["category"]][r_id] = newResource
            else:
                final_data[row["district"]][row["category"]] = {}
                final_data[row["district"]][row["category"]][r_id] = newResource
        else:
            final_data[row["district"]] = {}
            final_data[row["district"]][row["category"]] = {}
            final_data[row["district"]][row["category"]][r_id] = newResource


data = requests.get(OXYGEN_DATA).json()
print("Oxygen -> ", len(data["data"]))
for row in data["data"]:
    get_JSON_data(row)
print("Final data -> ", len(final_data))


data = requests.get(AMBULANCE_DATA).json()
print("Ambulance -> ", len(data["data"]))
for row in data["data"]:
    get_JSON_data(row)
print("Final data -> ", len(final_data))


i = 0
data = requests.get(FOOD_DATA).json()
print("Food -> ", len(data["data"]))
for row in data["data"]:
    i += 1
    if i <= 500:
        get_JSON_data(row)
    else:
        break 
print("Final data -> ", len(final_data))

print(i)
JSON_file = open("data.json", "w") 
JSON_file.write(json.dumps(final_data, indent = 4))
