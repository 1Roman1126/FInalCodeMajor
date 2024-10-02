import requests
import urllib3

# In nepseRequestParser.py
from datetime import date

def nepseReqParser(_dateToday):
    # Configurations for the request
    base_url = "https://www.nepalstock.com.np/api/nots/market/export/todays-price/"
    formatted_date = _dateToday.strftime("%Y-%m-%d")  # Ensure it's in YYYY-MM-DD format
    final_url = base_url + str(formatted_date)
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(final_url, headers=headers, verify=False)
    
    print(f"Request URL: {final_url}")  # Add logging to check URL
    print(f"Response Status Code: {response.status_code}")  # Log status code
    
    return response
