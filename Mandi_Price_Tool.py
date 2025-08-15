import requests
import os
from dotenv import load_dotenv  
load_dotenv()

def format_state_data(records):
    """
    Converts a list of market records into a readable string summary.

    Args:
        records (list): List of dictionaries containing market data.

    Returns:
        str: Formatted summary of the records.
    """
    if not records:
        return "No data available for the selected state."

    summary_lines = []
    for record in records:
        line = (
            f"Market: {record['market']} | "
            f"Commodity: {record['commodity']} ({record['variety']}) | "
            f"Grade: {record['grade']} | "
            f"Arrival Date: {record['arrival_date']} | "
            f"Min Price: ₹{record['min_price']} | "
            f"Max Price: ₹{record['max_price']} | "
            f"Modal Price: ₹{record['modal_price']}"
        )
        summary_lines.append(line)

    return "\n".join(summary_lines)

def get_state_data(state: str):
    GOV_API_KEY = os.getenv("GOV_API_KEY")
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    all_records = []
    offset = 0
    limit = 500  # API max per request; you can adjust

    while True:
        params = {
            "api-key": GOV_API_KEY,
            "format": "json",
            "filters[state]": state,
            "limit": limit,
            "offset": offset
        }
        headers = {"accept": "application/xml"}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        records = data.get('records', [])

        if not records:
            break

        all_records.extend(records)
        offset += limit

    return format_state_data(all_records)

data = get_state_data("Chhattisgarh")
print(data)