import sys
import src.log
from src import version_check
from src import bot

if __name__ == '__main__': 
    # Verifying package versions
    version_check.check_version()
    # Starting bot
    bot.run_discord_bot()
