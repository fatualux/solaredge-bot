import requests
from urllib.parse import urljoin
import re

base_url = "https://monitoringapi.solaredge.com/"


class Overview:
    def __init__(self, token):
        self.token = token

    def get_site_overview(self, site_id):
        """
        Get site overview data.
        """
        url = urljoin(base_url, f"site/{site_id}/overview")
        params = {'api_key': self.token}

        print("Request URL:", url)
        print("Request Params:", params)
        r = requests.get(url, params=params)
        print("Response:", r.content)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def escape_markdown(text):
        """
        Helper function to escape special characters in MarkdownV2.
        """
        escape_chars = r'\_*[]()~`>#+-=|{}.!'
        return re.sub(
            f"([{re.escape(escape_chars)}])", r'\\\1', text)

    @staticmethod
    def convert_to_kwh(value):
        """
        Helper function to convert Wh to kWh.
        """
        return value / 1000.0

    @staticmethod
    def convert_to_kw(value):
        """
        Helper function to convert W to kW.
        """
        return value / 1000.0

    def print_site_overview(self, overview_data):
        overview = overview_data.get('overview')
        if overview:
            energy_life_time_kwh = self.convert_to_kwh(overview['lifeTimeData']['energy'])
            energy_last_year_kwh = self.convert_to_kwh(overview.get('lastYearData', {}).get('energy', 0))
            energy_last_month_kwh = self.convert_to_kwh(overview.get('lastMonthData', {}).get('energy', 0))
            energy_last_day_kwh = self.convert_to_kwh(overview.get('lastDayData', {}).get('energy', 0))
            power_kw = self.convert_to_kw(overview['currentPower']['power'])

            overview_str = "Site Overview:\n"
            overview_str += (
                f"Last Update Time: {self.escape_markdown(overview.get('lastUpdateTime'))}\n"
                "Life Time Data:\n"
                "  Energy: {:.3f} kWh\n".format(energy_life_time_kwh) +
                f"  Revenue: {self.escape_markdown(str(overview['lifeTimeData']['revenue']))} €\n"
                "Last Year Data:\n"
            )
            overview_str += (
                "  Energy: {:.3f} kWh\n".format(energy_last_year_kwh)
                if energy_last_year_kwh else "  No data available for last year.\n"
            )
            overview_str += "Last Month Data:\n"
            overview_str += (
                "  Energy: {:.3f} kWh\n".format(energy_last_month_kwh)
                if energy_last_month_kwh else "  No data available for last month.\n"
            )
            overview_str += "Last Day Data:\n"
            overview_str += (
                "  Energy: {:.3f} kWh\n".format(energy_last_day_kwh)
                if energy_last_day_kwh else "  No data available for last day.\n"
            )
            overview_str += (
                "Current Power:\n"
                f"  Power: {self.escape_markdown('{:.3f}'.format(power_kw))} kW\n"
            )
            return overview_str
        else:
            return "No site overview data found."


# Example usage
token = "your_api_key"
site_id = "your_site_id"
overview = Overview(token)
data = overview.get_site_overview(site_id)
print(overview.print_site_overview(data))
