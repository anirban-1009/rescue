from pymongo import MongoClient
import csv

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Change this if needed
db = client["Rescue"]  # Database name
collection = db["EmergencyCentre"]  # Collection name
# Path to the CSV file
csv_file_path = "data/firefighters.csv"  # Update with the actual file path

# Read CSV File and Process Data
documents = []
with open(csv_file_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)
        document = {
            "state": "Telangana",
            "district": "Hyderabad",
            "taluka": row["Zone"].strip(),
            "facility_name": f"{row['Assessor Address'].strip()} Fire Station",
            "facility_type": "Fire Station",
            "latitude": float(row["Latitude"]),
            "longitude": float(row["Longitude"]),
            "street": None,  # Can be updated if street data is available
            "landmark": None,  # Can be updated if landmark data is available
            "locality": row["Wardno Name"].strip(),
            "region_indicator": "Urban",
            "operational_status": "Functional",
            "ownership_authority": "State Government",
        }
        documents.append(document)

# Insert Data into MongoDB
if documents:
    collection.insert_many(documents)
    print(f"{len(documents)} records inserted successfully into MongoDB.")
else:
    print("No data found in the CSV file.")
