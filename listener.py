# from discord_slash import SlashCommand, ComponentContext
from player import garbage_player


# Function for parsing the commands
def listeners(client, token):
    # Guilds where this bot will work
    guild_ids = [537261336351211528, 474158226439667712, 827623437400801280, 757859064939282463, 846060380597125122,
                 876163978097741840, 137075099097497601, 988816967311953930]

    # Enable slash commands
    # slash = SlashCommand(client, sync_commands=True)

    # Bot is ready to go!
    @client.event
    async def on_ready():
        print("Ready for action!")

    # Play command
    @client.slash_command(name="play", guild_ids=guild_ids,
                          description="Play a song from a youtube link, format: /play [song_url]")
    async def _play(ctx, url):
        await garbage_player(ctx, client, url)

    # Pause command
    @client.slash_command(name="pause", guild_ids=guild_ids,
                          description="Pause the current song.")
    async def _pause(ctx):
        await garbage_player(ctx, client)

    # Resume command
    @client.slash_command(name="resume", guild_ids=guild_ids,
                          description="Resume a paused song.")
    async def _resume(ctx):
        await garbage_player(ctx, client)

    # Repeat command
    @client.slash_command(name="repeat", guild_ids=guild_ids,
                          description="Toggle the current track to repeat.")
    async def _repeat(ctx):
        await garbage_player(ctx, client)

    # Status command
    @client.slash_command(name="status", guild_ids=guild_ids,
                          description="Get the current bot status.")
    async def _status(ctx):
        await garbage_player(ctx, client)

    # Queue command
    @client.slash_command(name="queue", guild_ids=guild_ids,
                          description="Get the current track queue.")
    async def _queue(ctx):
        await garbage_player(ctx, client)

    # Skip command
    @client.slash_command(name="skip", guild_ids=guild_ids,
                          description="Skips the current track.")
    async def _skip(ctx):
        await garbage_player(ctx, client)

    @client.slash_command(name="remove", guild_ids=guild_ids,
                          description="Remove song from queue.")
    async def _remove(ctx, number):
        await garbage_player(ctx, client, number)

    # Leave command
    @client.slash_command(name="leave", guild_ids=guild_ids,
                          description="Disconnect the bot from a voice channel.")
    async def _leave(ctx):
        await garbage_player(ctx, client)

    # Leave command
    @client.slash_command(name="maintenance", guild_ids=guild_ids,
                          description="Allows the bot admin to put the bot in maintenance mode.")
    async def _maintenance(ctx):
        if ctx.author.id == 123646058340417537:
            await garbage_player(ctx, client)
        else:
            await ctx.send("Bruh...")

    # Run the client with the needed token

    client.run(token)
