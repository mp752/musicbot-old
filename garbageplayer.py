

from discord_slash import ComponentContext
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from asyncio import sleep, run_coroutine_threadsafe
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle

# Options for both the youtube downloader and ffmpeg
YDL_OPTIONS = {'format': 'worstaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

# Bot status, format = [Current Song, (Stopped|Playing|Paused), Repeat(T/F), Song Name]
STATUS = ["", 0, False, ""]
BUTTONS = [
    create_button(
        style=ButtonStyle.blue,
        label="🔁"
    )
]
action_row = create_actionrow(*BUTTONS)


async def garbage_player(ctx, client, song="",):
    voice = ctx.guild.voice_client
    if ctx.command == "play":
        await play(ctx, song, voice, client)

    if ctx.command == "pause":
        await pause(ctx, voice)

    if ctx.command == "resume":
        await resume(ctx, voice)

    if ctx.command == "repeat":
        await repeat(ctx)

    if ctx.command == "status":
        await status(ctx, client)


def after_play(ctx, voice):
    if voice and voice.is_playing():
        voice.stop()
    if STATUS[2]:
        voice.play(FFmpegPCMAudio(STATUS[0], **FFMPEG_OPTIONS), after=lambda e: after_play(ctx, voice))


# The function for playing garbage... or music.
async def play(ctx, song, voice, client):
    message = await ctx.send("Loading...")
    # Get song/video from URL
    STATUS[2] = False
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(song, download=False)
    # Get direct URL
    url = info['formats'][0]['url']
    # Check if bot is in a channel, if not then connect
    if not voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        voice = ctx.guild.voice_client
    # If music is already being played, then stop the current song and restart with the new one
    if voice.is_playing():
        voice.stop()
    await sleep(2)
    # Play music and stop when done
    voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda e: after_play(ctx, voice))
    STATUS[0] = url
    STATUS[1] = 1
    STATUS[3] = info['title']
    await message.edit(content="Now playing: " + STATUS[3] + "!")


async def pause(ctx, voice):
    try:
        # Check if bot is even playing anything, if so then pause.
        if voice.is_playing():
            voice.pause()
            STATUS[1] = 2
            await ctx.send("Music paused.")
        # If not
        else:
            await ctx.send("Nothing is playing...")
    # If bot is not in a channel
    except AttributeError:
        await ctx.send("I'm not in a channel, dumdum.")


async def resume(ctx, voice):
    try:
        # Check if bot is even playing anything, if so then pause.
        if voice.is_paused():
            voice.resume()
            STATUS[1] = 1
            await ctx.send("Music resumed.")
        # If not
        else:
            await ctx.send("Nothing is playing...")
    # If bot is not in a channel
    except AttributeError:
        await ctx.send("I'm not in a channel, dumdum.")


async def repeat(ctx):
    if STATUS[2]:
        STATUS[2] = False
        await ctx.send("Repeat disabled.")
    else:
        STATUS[2] = True
        await ctx.send("Repeat enabled.")


async def status(ctx, client):
    send_message = "I am currently"
    if STATUS[1] == 0:
        send_message += " stopped"
    elif STATUS[1] == 1:
        send_message += " playing **" + STATUS[3] + "**"
    elif STATUS[1] == 2:
        send_message += " paused **" + STATUS[3] + "**"
    if STATUS[2]:
        send_message += " with repeat enabled"

    await ctx.send(send_message + ".", components=[action_row])
    button_ctx: ComponentContext = await wait_for_component(client, components=action_row)
    STATUS[2] = True
    await button_ctx.edit_origin(content="Repeat toggled")


