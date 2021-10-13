from discord_slash import SlashCommand
from garbageplayer import garbage_player


# Function for parsing the commands
def listeners(client, token):
    # Guilds where this bot will work
    guild_ids = [537261336351211528, 474158226439667712]
    # Enable slash commands
    slash = SlashCommand(client, sync_commands=True)

    # Bot is ready to go!
    @client.event
    async def on_ready():
        print("Ready for action!")

    # Play command
    @slash.slash(name="play", guild_ids=guild_ids,
                 description="Play a song from a youtube link, format: /play [song_url]")
    async def _play(ctx, url):
        await garbage_player(ctx, client, url)

    # Pause command
    @slash.slash(name="pause", guild_ids=guild_ids,
                 description="Pause the current song.")
    async def _pause(ctx):
        await garbage_player(ctx, client)

    # Resume command
    @slash.slash(name="resume", guild_ids=guild_ids,
                 description="Resume a paused song.")
    async def _resume(ctx):
        await garbage_player(ctx, client)

    # Repeat command
    @slash.slash(name="repeat", guild_ids=guild_ids,
                 description="Toggle the current track to repeat.")
    async def _repeat(ctx):
        await garbage_player(ctx, client)

    # Status command
    @slash.slash(name="status", guild_ids=guild_ids,
                 description="Get the current bot status.")
    async def _status(ctx):
        await garbage_player(ctx, client)

    # Leave command
    @slash.slash(name="leave", guild_ids=guild_ids,
                 description="Disconnect the bot from a voice channel.")
    async def _leave(ctx):
        # See if the bot is in a channel, if so then disconnect it
        try:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("lolbye")
        # If not, then send this message
        except AttributeError:
            await ctx.send("I'm not in a channel, dumdum.")

    # Run the client with the needed token
    client.run(token)
