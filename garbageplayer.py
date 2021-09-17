from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from asyncio import sleep


async def garbage_player(message, song):
    YDL_OPTIONS = {'format': 'worstaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(song, download=False)
    URL = info['formats'][0]['url']
    if not message.guild.voice_client:
        channel = message.author.voice.channel
        await channel.connect()
    if message.guild.voice_client.is_playing:
        message.guild.voice_client.stop()
    message.guild.voice_client.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    try:
        while message.guild.voice_client.is_playing:
            await sleep(30)
        await message.guild.voice_client.disconnect()
    except AttributeError:
        pass
