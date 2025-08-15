import os
import json
import ee
from dotenv import load_dotenv

load_dotenv()

service_account_json = os.getenv("EE_SERVICE_KEY")
if not service_account_json:
    raise ValueError("EE_SERVICE_KEY not set in environment variables")

key_data = json.loads(service_account_json)
service_account = key_data["client_email"]

temp_key_path = "/tmp/ee-key.json"
with open(temp_key_path, "w") as f:
    json.dump(key_data, f)

credentials = ee.ServiceAccountCredentials(service_account, temp_key_path)
ee.Initialize(credentials)
print("Google Earth Engine initialized")
