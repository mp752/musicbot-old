from discord_slash import SlashCommand, ComponentContext
from garbageplayer import garbage_player


# Function for parsing the commands
def listeners(client, token):
    # Guilds where this bot will work
    guild_ids = [537261336351211528, 474158226439667712, 827623437400801280, 757859064939282463]
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
        ctx.is_button = False
        await garbage_player(ctx, client)

    # Status command
    @slash.slash(name="status", guild_ids=guild_ids,
                 description="Get the current bot status.")
    async def _status(ctx):
        await garbage_player(ctx, client)

    # Queue command
    @slash.slash(name="queue", guild_ids=guild_ids,
                 description="Get the current track queue.")
    async def _status(ctx):
        await garbage_player(ctx, client)

    # Skip command
    @slash.slash(name="skip", guild_ids=guild_ids,
                 description="Skips the current track.")
    async def _skip(ctx):
        await garbage_player(ctx, client)

    @slash.slash(name="remove", guild_ids=guild_ids,
                 description="Remove song from queue.")
    async def _remove(ctx, number):
        await garbage_player(ctx, client, number)

    # Leave command
    @slash.slash(name="leave", guild_ids=guild_ids,
                 description="Disconnect the bot from a voice channel.")
    async def _leave(ctx):
        await garbage_player(ctx, client)

    @slash.component_callback()
    async def repeat(ctx: ComponentContext):
        ctx.command = "repeat"
        await garbage_player(ctx, client)

    @slash.component_callback()
    async def pause(ctx: ComponentContext):
        ctx.command = "pause"
        await garbage_player(ctx, client)

    @slash.component_callback()
    async def resume(ctx: ComponentContext):
        ctx.command = "resume"
        await garbage_player(ctx, client)



    # Run the client with the needed token

    client.run(token)
