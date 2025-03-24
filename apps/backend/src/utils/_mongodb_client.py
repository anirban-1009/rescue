import pandas as pd
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Change this if needed
db = client["Rescue"]  # Database name
collection = db["EmergencyCentre"]  # Collection name

# Read CSV file
csv_file = "data/Health-centers-data.csv"  # Update with the correct path
df = pd.read_csv(csv_file)

# Rename columns to match MongoDB format
df.columns = [
    "state",
    "district",
    "taluka",
    "facility_name",
    "facility_type",
    "latitude",
    "longitude",
    "street",
    "landmark",
    "locality",
    "region_indicator",
    "operational_status",
    "ownership_authority",
]

# Remove duplicate entries based on unique constraints
df.drop_duplicates(subset=["facility_name", "district"], inplace=True)

# Convert DataFrame to dictionary format for MongoDB
records = df.to_dict(orient="records")

# Insert into MongoDB (ignore duplicates)
try:
    collection.insert_many(records, ordered=False)
    print(f"Inserted {len(records)} records into MongoDB.")
except Exception as e:
    print(f"Error inserting records: {e}")
