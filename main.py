import os
import discord
from dotenv import load_dotenv
from listener import listeners

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client=discord.Client()
    listeners(client, TOKEN)



