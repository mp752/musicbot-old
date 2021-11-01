from asyncio import sleep
from discord import Embed
from discord import FFmpegPCMAudio
from discord_slash import SlashCommand
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError

# Options for both the youtube downloader and ffmpeg
YDL_OPTIONS = {'format': 'worstaudio', 'noplaylist': 'True', 'youtube_include_dash_manifest': False,
               'default_search': 'ytsearch'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

# Bot status, format = [Current Song, (Stopped|Playing|Paused), Repeat(T/F), Song Name]
BUTTONS = [
    create_button(
        style=ButtonStyle.red,
        label="Pause",
        custom_id="pause"
    ),
    create_button(
        style=ButtonStyle.green,
        label="Play",
        custom_id="resume"
    ),
    create_button(
        style=ButtonStyle.blue,
        label="Repeat",
        custom_id="repeat"
    )
]
SERVERS = {}
action_row = create_actionrow(*BUTTONS)


async def garbage_player(ctx, client, argument=""):

    if ctx.author.id == 134067571614941185:
        await ctx.send("You ruined the last bot, you aren't going to fuck this up >:(")

    if not ctx.author.voice:
        await ctx.send("User is not in a channel.")
        return
    if ctx.guild.voice_client and not ctx.author.voice.channel == ctx.guild.voice_client.channel:
        await ctx.send("You are not in a bot channel.")
        return

    global SERVERS
    if ctx.guild.id not in SERVERS.keys():
        SERVERS[ctx.guild.id] = {
            "track_url": "",
            "track_name": "",
            "status": "Stopped",
            "repeat": False,
            "thumbnail": "",
            "queue": [],

        }

    voice = ctx.guild.voice_client
    if ctx.command == "play":
        await play(ctx, argument, voice, client, SERVERS)

    if ctx.command == "pause":
        await pause(ctx, voice, SERVERS)

    if ctx.command == "resume":
        await resume(ctx, voice, SERVERS)

    if ctx.command == "repeat":
        await repeat(ctx, SERVERS)

    if ctx.command == "status":
        await status(ctx, client, SERVERS)

    if ctx.command == "queue":
        await queue(ctx, voice, SERVERS)

    if ctx.command == "skip":
        voice.stop()
        await ctx.send("Song skipped!")

    if ctx.command == "leave":
        await leave(ctx, SERVERS)

    if ctx.command == "remove":
        await remove(ctx, SERVERS, argument)


def after_play(ctx, voice, servers):
    if voice and voice.is_playing():
        voice.stop()
    if servers[ctx.guild.id]["repeat"] and voice:
        voice.play(FFmpegPCMAudio(servers[ctx.guild.id]["track_url"], **FFMPEG_OPTIONS),
                   after=lambda e: after_play(ctx, voice, servers))
        servers[ctx.guild.id]["status"] = "Playing"
    elif servers[ctx.guild.id]["queue"]:
        servers[ctx.guild.id]["track_url"] = servers[ctx.guild.id]["queue"][0][0]
        servers[ctx.guild.id]["track_name"] = servers[ctx.guild.id]["queue"][0][1]
        servers[ctx.guild.id]["thumbnail"] = servers[ctx.guild.id]["queue"][0][2]
        voice.play(FFmpegPCMAudio(servers[ctx.guild.id]["queue"].pop(0)[0], **FFMPEG_OPTIONS),
                   after=lambda e: after_play(ctx, voice, servers))
        servers[ctx.guild.id]["status"] = "Playing"

    else:
        servers[ctx.guild.id]["status"] = "Stopped"
        servers[ctx.guild.id]["track_url"] = ""
        servers[ctx.guild.id]["track_name"] = ""
        servers[ctx.guild.id]["thumbnail"] = ""


# The function for playing garbage... or music.
async def play(ctx, song, voice, client, servers):
    message = await ctx.send("Loading...")
    servers[ctx.guild.id]["repeat"] = False
    # Get song/video from URL
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            ydl.cache.remove()
            info = ydl.extract_info(song, download=False)
        except DownloadError:
            await message.edit(content="Error fetching the track.")
            return
    # Get direct URL
    try:
        url = info['formats'][0]['url']
    except KeyError:
        info = info['entries'][0]
        url = info['formats'][0]['url']
        print(url)
    # Check if bot is in a channel, if not then connect
    if not voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        voice = ctx.guild.voice_client
    if not servers[ctx.guild.id]["status"] == "Stopped":
        servers[ctx.guild.id]["queue"].append([url, info['title'], info['thumbnails'][0]['url']])
        await message.edit(content="Added: " + info['title'])
    else:
        servers[ctx.guild.id]["track_url"] = url
        servers[ctx.guild.id]["status"] = "Playing"
        servers[ctx.guild.id]["track_name"] = info['title']
        servers[ctx.guild.id]["thumbnail"] = info['thumbnails'][0]['url']
        await message.edit(content="Now playing: " + servers[ctx.guild.id]["track_name"] + "!")
        voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda e: after_play(ctx, voice, servers))


async def pause(ctx, voice, servers):
    try:
        # Check if bot is even playing anything, if so then pause.
        if voice.is_playing():
            voice.pause()
            servers[ctx.guild.id]["status"] = "Paused"
            await ctx.send("Music paused.")
        # If not
        else:
            await ctx.send("Nothing is playing...")
    # If bot is not in a channel
    except AttributeError:
        await ctx.send("I'm not in a channel, dumdum.")


async def resume(ctx, voice, servers):
    try:
        # Check if bot is even playing anything, if so then pause.
        if voice.is_paused():
            voice.resume()
            servers[ctx.guild.id]["status"] = "Playing"
            await ctx.send("Music resumed.")
        # If not
        else:
            await ctx.send("Nothing is paused...")
    # If bot is not in a channel
    except AttributeError:
        await ctx.send("I'm not in a channel, dumdum.")


async def repeat(ctx, servers):
    if servers[ctx.guild.id]["repeat"]:
        servers[ctx.guild.id]["repeat"] = False
        await ctx.send("Repeat disabled.")
    else:
        servers[ctx.guild.id]["repeat"] = True
        await ctx.send("Repeat enabled.")


async def leave(ctx, servers):
    # See if the bot is in a channel, if so then disconnect it
    try:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("lolbye")

    # If not, then send this message
    except AttributeError:
        await ctx.send("I'm not in a channel, dumdum.")


async def queue(ctx, voice, servers):
    queue_list = "Nothing else to play."
    if voice and not servers[ctx.guild.id]["status"] == "Stopped":
        if servers[ctx.guild.id]["queue"]:
            queue_list = ""
            for track in range(0, len(servers[ctx.guild.id]["queue"])):
                queue_list += str(track + 1) + ". " + servers[ctx.guild.id]["queue"][track][1] + "\n"
        embed = Embed(title="K_K Queue", footer="Current track: " + servers[ctx.guild.id]["track_name"],
                      description=queue_list, inline=True)
        embed.set_footer(text="Current track: " + servers[ctx.guild.id]["track_name"])
        embed.set_thumbnail(url="https://i.imgur.com/NxVsIiC.gif")
        embed.set_image(url=servers[ctx.guild.id]["thumbnail"])
        await ctx.send(content=None, embed=embed)
    else:
        await ctx.send("Not connected/Empty")


async def status(ctx, client, servers):
    info = servers[ctx.guild.id]

    embed = Embed(title="K_K Status")
    embed.add_field(name="I am currently " + info["status"] + ": ", value=info["track_name"] + ' \u200b')
    if info["queue"]:
        embed.add_field(name="Next Track: ", value=info["queue"][0][1])
    if info["repeat"]:
        embed.add_field(name="\u200b", value="Repeat on")
    if not info["status"] == "Stopped":
        embed.set_thumbnail(url=info["thumbnail"])
    message = await ctx.send(content=None, embed=embed, components=[action_row])
    await sleep(30)
    await message.edit(content=None, embed=embed, components=None)


async def remove(ctx, servers, song):
    current_queue = servers[ctx.guild.id]["queue"]
    try:
        removed_song = current_queue.pop(int(song)-1)[1]
        await ctx.send("Removed " + removed_song + " from the queue.")
    except IndexError:
        await ctx.send("Track number not in queue.")
