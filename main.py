import os
import discord
from dotenv import load_dotenv
from listener import listeners
from discord.ext import commands

if __name__ == '__main__':
    # Load ENV file with API key
    load_dotenv()
    # Load token from ENV file
    TOKEN = os.getenv('DISCORD_TOKEN')
    # Create a new discord client
    client = commands.Bot(command_prefix=" - - - - - - - - - - - - -")
    # Move the client and token to the command listener
    listeners(client, TOKEN)
