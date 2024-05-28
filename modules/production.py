import requests
from urllib.parse import urljoin
import config as cfg


class Production:
    def __init__(self, token):
        self.token = token

    def get_daily_production(self, start_date, end_date):
        url = urljoin(cfg.BASEURL, f"site/{cfg.site_id}/energy")
        params = {
            'api_key': cfg.site_token,
            'timeUnit': 'DAY',
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d')
        }

        print("Request URL:", url)
        print("Request Params:", params)
        r = requests.get(url, params=params)
        print("Response:", r.content)
        r.raise_for_status()
        return r.json()

    def print_daily_production(self, daily_production):
        output = "Daily Production:\n"
        unit = daily_production['energy'].get('unit')
        for day in daily_production['energy']['values']:
            output += (
                f"Date: {day['date']}, \nProduction: {day['value']} {unit}\n"
            )
        return output
