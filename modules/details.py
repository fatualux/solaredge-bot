import requests
from urllib.parse import urljoin
import sys
import config as cfg

sys.path.append('..')


class Details:
    def __init__(self, token):
        self.token = token

    def get_details(self, site_id):
        base_url = urljoin(cfg.BASEURL, f"site/{site_id}/details")
        url = f"{base_url}?api_key={self.token}"
        print("Request URL:", url)
        response = requests.get(url)
        response.raise_for_status()
        try:
            site_details = response.json()
        except ValueError:
            raise ValueError("Failed to parse response as JSON")
        return site_details

    def format_site_details(self, details):
        details = details['details']
        formatted_details = "Site Details:\n"
        formatted_details += (
            f"id: {details['id']}\n"
            f"name: {details['name']}\n"
            f"accountId: {details['accountId']}\n"
            f"status: {details['status']}\n"
            f"peakPower: {details['peakPower']}\n"
            f"lastUpdateTime: {details['lastUpdateTime']}\n"
            f"installationDate: {details['installationDate']}\n"
            f"ptoDate: {details['ptoDate']}\n\n"
            f"Location:\n"
            f"country: {details['location']['country']}\n"
            f"city: {details['location']['city']}\n"
            f"address: {details['location']['address']}\n\n"
            f"PrimaryModule:\n"
            f"manufacturerName: {details['primaryModule']['manufacturerName']}\n"
            f"modelName: {details['primaryModule']['modelName']}\n"
            f"maximumPower: {details['primaryModule']['maximumPower']}\n"
            f"temperatureCoef: {details['primaryModule']['temperatureCoef']}\n"
            f"{urljoin(cfg.BASEURL, '/site/' + str(details['id']))}\n"
            f"\n"
        )
        return formatted_details
