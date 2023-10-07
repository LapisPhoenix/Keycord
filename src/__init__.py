from src.client import Client

# Default config

VERSION = "0.0.1"
API_VERSION = "v9"                                  # * 9/10 you don't want to change this
API_BACKEND = "https://canary.discord.com/api/"     # * 9/10 you don't want to change this
USER_AGENT = f"keycord/{VERSION}"
TOKEN = None                                        # TODO: Need to add a way to get token.

client = Client(TOKEN)