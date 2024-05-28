import requests

base_url = "https://monitoringapi.solaredge.com/equipment/"


class Components:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_inverters_list(self, site_id):
        url = f"{base_url}{site_id}/list"
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_inverter_data(self, site_id, serial_number, start_time, end_time):
        url = f"{base_url}{site_id}/{serial_number}/data"
        params = {
            'startTime': start_time,
            'endTime': end_time,
            'api_key': self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_equipment_change_log(self, site_id, serial_number):
        url = f"{base_url}/{site_id}/{serial_number}/changeLog"
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
