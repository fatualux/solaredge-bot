import requests
from urllib.parse import urljoin

BASEURL = "https://monitoringapi.solaredge.com/equipment/"


class Overview:
    def __init__(self, token):
        self.token = token

    def get_site_overview(self, site_id):
        """
        Get site overview data.
        """
        url = urljoin(BASEURL, f"site/{site_id}/overview")
        params = {
            'api_key': cfg.site_token
        }

        print("Request URL:", url)
        print("Request Params:", params)
        r = requests.get(url, params=params)
        print("Response:", r.content)
        r.raise_for_status()
        return r.json()

    def print_site_overview(self, overview_data):
        overview = overview_data.get('overview')
        if overview:
            overview_str = "Site Overview:\n"
            overview_str += (
                f"Last Update Time: {overview.get('lastUpdateTime')}\n"
                "Life Time Data:\n"
                f"  Energy: {overview['lifeTimeData']['energy']}\n"
                f"  Revenue: {overview['lifeTimeData']['revenue']}\n"
                "Last Year Data:\n"
            )
            last_year_data = overview.get('lastYearData')
            if last_year_data:
                overview_str += (
                    f"  Energy: {last_year_data.get('energy')}\n"
                    f"  Revenue: {last_year_data.get('revenue')}\n"
                )
            else:
                overview_str += "  No data available for last year.\n"
            overview_str += "Last Month Data:\n"
            last_month_data = overview.get('lastMonthData')
            if last_month_data:
                overview_str += (
                    f"  Energy: {last_month_data.get('energy')}\n"
                    f"  Revenue: {last_month_data.get('revenue')}\n"
                )
            else:
                overview_str += "  No data available for last month.\n"
            overview_str += "Last Day Data:\n"
            last_day_data = overview.get('lastDayData')
            if last_day_data:
                overview_str += (
                    f"  Energy: {last_day_data.get('energy')}\n"
                    f"  Revenue: {last_day_data.get('revenue')}\n"
                )
            else:
                overview_str += "  No data available for last day.\n"
            overview_str += "Current Power:\n"
            overview_str += f"  Power: {overview['currentPower']['power']}\n"
            return overview_str
        else:
            return "No site overview data found."
