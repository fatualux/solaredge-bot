import requests
from datetime import datetime, timedelta


class Power:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_site_power(self, SITE_ID):
        current_time = datetime.now()
        # Adjust start time to 6 hours before the current time
        start_time = current_time - timedelta(hours=6)
        end_time = current_time
        url = f"https://monitoringapi.solaredge.com/site/{SITE_ID}/power"
        params = {
            'startTime': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'endTime': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'api_key': self.api_key
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def format_power_data(self, power_data):
        if power_data is None:
            return "No data available"

        if 'power' in power_data:
            power_data = power_data['power']

        if 'timeUnit' in power_data:
            time_unit = power_data['timeUnit']
        else:
            time_unit = "Unknown"

        if 'unit' in power_data:
            unit = power_data['unit']
        else:
            unit = "Unknown"

        if 'values' in power_data:
            values = power_data['values']
        else:
            values = []
        formatted_data = (
            f"Time Unit: {time_unit}\n"
            f"Unit: {unit}\n"
            f"Measurement Interval: \n"
            f"  From {values[0]['date']} to {values[-1]['date']}\n"
        )
        formatted_data += "Power Data:\n"
        for entry in values:
            date = entry.get('date', 'Unknown')
            value = entry.get('value', 'Unknown')
            formatted_data += f"Date: {date}, Value: {value}\n"

        return formatted_data
