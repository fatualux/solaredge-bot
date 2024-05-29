import requests

BASEURL = "https://monitoringapi.solaredge.com/equipment/"


class Components:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_inverters_list(self, SITE_ID):
        url = f"{BASEURL}{SITE_ID}/list"
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_inverter_data(self, SITE_ID, serial_number, start_time, end_time):
        url = f"{BASEURL}{SITE_ID}/{serial_number}/data"
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

    def get_equipment_change_log(self, SITE_ID, serial_number):
        url = f"{BASEURL}/{SITE_ID}/{serial_number}/changeLog"
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
