import discord
from garbageplayer import garbage_player

def listeners(client, token):
    @client.event
    async def on_ready():
        print("Bot is live!")

    @client.event
    async def on_message(message):
        command = message.content.split()
        if command[0] == "$play" and len(command) == 2:
            await garbage_player(message, command[1])
        elif message.content == "$leave" or message.content == "$begone_thot":
            try:
                await message.guild.voice_client.disconnect()
            except AttributeError:
                await message.channel.send("I'm not in any channel nimrod.")

    client.run(token)
