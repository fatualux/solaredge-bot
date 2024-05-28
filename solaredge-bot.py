import telepot
import sys
from modules.message_handler import MessageHandler
from modules.automate import Automate
from modules.overview import Overview
from modules.production import Production
import config as cfg

# config.py is in the parent directory
sys.path.append("..")

# Initialize the Telegram bot
bot = telepot.Bot(cfg.bot_token)

# Initialize overview and production APIs
overview_api = Overview(cfg.site_token)
production_api = Production(cfg.site_token)

# Initialize Automate with bot
automate_module = Automate(bot)

# Initialize MessageHandler with Automate module
message_handler = MessageHandler(bot, automate_module)


# Function to handle incoming messages
def handle(msg):
    message_handler.handle_message(msg)


# Start listening for messages
bot.message_loop(handle)

# Keep the script running
while True:
    pass
