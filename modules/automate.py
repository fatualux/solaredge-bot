import time
from datetime import datetime, time as dtime
import sys
import config as cfg
from modules.overview import Overview

sys.path.append('..')


class Automate:
    def __init__(self, bot):
        self.bot = bot
        self.interval = 60  # Set the interval to 60 minutes by default
        self.stop_requested = False
        self.overview_api = Overview(cfg.site_token)

    def send_automated_messages(self, chat_id):
        try:
            # Send start cycle message
            self.bot.sendMessage(chat_id, "Automated messages started.")

            while not self.stop_requested:
                # Check if current time is within the allowed range
                # (7.00 AM to 9.30 PM)
                current_time = datetime.now().time()
                if dtime(7, 0) <= current_time <= dtime(21, 30):
                    # Get overview data
                    overview_data = self.overview_api.get_site_overview(
                        cfg.site_id
                    )
                    overview_message = self.overview_api.print_site_overview(
                        overview_data
                    )

                    # Send overview message
                    self.bot.sendMessage(chat_id, overview_message)
                else:
                    # Send stop cycle message if outside allowed range
                    msg = "Automated messages stopped at 21:30."
                    self.bot.sendMessage(chat_id, msg)
                    self.stop_requested = True

                time.sleep(self.interval * 60)  # Convert minutes to seconds

            # Send stop cycle message
            self.bot.sendMessage(chat_id, "Automated messages stopped.")
        except Exception as e:
            self.bot.sendMessage(chat_id, f"An error occurred: {str(e)}")
