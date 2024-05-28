import telepot
from datetime import datetime
from modules.details import Details
from modules.overview import Overview
from modules.meters import Meters
from modules.production import Production
from modules.energy import Energy
from modules.power import Power
from modules.sensors import Sensors
import config as cfg


class MessageHandler:
    def __init__(self, bot, automate_module):
        self.bot = bot
        self.automate_module = automate_module
        self.handlers = {
            "/start": self.handle_start,
            "/help": self.handle_help,
            "/details": self.handle_details,
            "/overview": self.handle_overview,
            "/meters": self.handle_meters,
            "/production": self.handle_production,
            "/energy": self.handle_energy,
            "/power": self.handle_power,
            "/sensors": self.handle_sensors,
            "/automate": self.handle_automate
        }

        # Initialize APIs here if needed
        self.details_api = Details(cfg.site_token)
        self.overview_api = Overview(cfg.site_token)
        self.meters_api = Meters(cfg.site_token, cfg.site_id)
        self.production_api = Production(cfg.site_token)
        self.energy_api = Energy(cfg.site_token)
        self.power_api = Power(cfg.site_token)
        self.sensors_api = Sensors(cfg.site_token)

    def handle_message(self, msg):
        content_type, _, chat_id = telepot.glance(msg)
        if content_type == 'text':
            command = msg['text']
            if command in self.handlers:
                self.handlers[command](chat_id)
            else:
                msg = "Sorry, I didn't understand that command."
                self.bot.sendMessage(chat_id, msg)
        else:
            msg = "Sorry, I only understand text messages."
            self.bot.sendMessage(chat_id, msg)

    def handle_start(self, chat_id):
        msg = "Welcome to SolarEdge Bot. Type /help to see available commands."
        self.bot.sendMessage(chat_id, "Hello! " + msg)

    def handle_help(self, chat_id):
        help_message = (
            "Available commands:\n"
            "/details - Get site details\n"
            "/overview - Get site overview\n"
            "/meters - Get meter data\n"
            "/production - Get daily production\n"
            "/energy - Get site energy data\n"
            "/power - Get site power data\n"
            "/sensors - Get sensor data\n"
            "/automate - Set up automated notifications\n"
            "/start - Start the bot\n"
            "/help - Show this help message"
        )
        self.bot.sendMessage(chat_id, help_message)

    def handle_details(self, chat_id):
        details = self.details_api.get_details(cfg.site_id)
        formatted_details = self.details_api.format_site_details(details)
        self.bot.sendMessage(chat_id, formatted_details)

    def handle_overview(self, chat_id):
        overview_data = self.overview_api.get_site_overview(cfg.site_id)
        self.bot.sendMessage(
            chat_id, self.overview_api.print_site_overview(overview_data)
        )

    def handle_meters(self, chat_id):
        meters_data = self.meters_api.get_meter_data()
        self.bot.sendMessage(
            chat_id, self.meters_api.print_meter_data(meters_data)
        )

    def handle_production(self, chat_id):
        start_date = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_date = datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999
        )
        production_data = self.production_api.get_daily_production(
            start_date, end_date
        )
        self.bot.sendMessage(
            chat_id, self.production_api.print_daily_production(
                production_data
            )
        )

    def handle_energy(self, chat_id):
        start_date = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_date = datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999
        )
        energy_data = self.energy_api.get_site_energy(
            cfg.site_id,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        formatted_energy_data = self.energy_api.format_energy_data(energy_data)
        self.bot.sendMessage(chat_id, formatted_energy_data)

    def handle_power(self, chat_id):
        power_data = self.power_api.get_site_power(cfg.site_id)
        formatted_power_data = self.power_api.format_power_data(power_data)
        self.bot.sendMessage(chat_id, f"Power data:\n{formatted_power_data}")

    def handle_sensors(self, chat_id):
        sensor_data = self.sensors_api.get_sensor_data(cfg.site_id)
        if sensor_data is not None:
            formatted_sensor_data = self.sensors_api.format_sensor_data(
                sensor_data
            )
            self.bot.sendMessage(
                chat_id, f"Sensor data:\n{formatted_sensor_data}"
            )
        else:
            self.bot.sendMessage(chat_id, "No sensor data available.")

    def handle_automate(self, chat_id):
        self.automate_module.interval = 90
        self.automate_module.send_automated_messages(chat_id)
