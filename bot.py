import discord
from os import environ
import requests
from discord.ext import commands
import json
import quote_manager
import asyncio
from datetime import datetime
from youtube_dl import YoutubeDL

client = discord.Client()
client = commands.Bot(command_prefix='!')


is_playing = False
music_queue = []
hidden_music_queue = []
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
voice = ""
help_message_music = """
!help - Shows this message
!play <song_name> - Plays the song
!queue - displays the current music queue
!skip - skips to the next song
!skip <track no> - skips to the track selected
!previous - Plays previous played song
!disconnect - bot leaves from current vc
!remove <track no> - removes the track from the queue
!pause - pause the current track
!resume - resume the current track
"""
help_message_chat = """
!m <ur msg> - replies to almost all questions :)
"""
help_message_quote = """
!q <channel id> - sends a daily quote to a specified channel
"""


def search_yt(item):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info("ytsearch:%s" %
                                    item, download=False)['entries'][0]
        except Exception:
            return False

    return {'source': info['formats'][0]['url'], 'title': info['title']}


def play_next():
    global is_playing
    if len(music_queue) > 0:
        is_playing = True
        video_source = music_queue[0][0]['source']
        music_queue.pop(0)
        voice.play(discord.FFmpegPCMAudio(video_source, **
                   FFMPEG_OPTIONS), after=lambda e: play_next())
    else:
        is_playing = False

# def play_previous():
#     if len(music_queue) >= 0:
#         video_source = hidden_music_queue[0][0]['source']
#         is_playing = True
#         voice.play(discord.FFmpegPCMAudio(video_source, **FFMPEG_OPTIONS), after=lambda e: play_previous())
#     else:
#         is_playing = False


async def play_music():
    global is_playing, voice
    if len(music_queue) > 0:
        is_playing = True
        video_source = music_queue[0][0]['source']

        if voice == "" or not voice.is_connected() or voice == None:
            voice = await music_queue[0][1].connect()
        else:
            await voice.move_to(music_queue[0][1])
        music_queue.pop(0)

        voice.play(discord.FFmpegPCMAudio(video_source, **
                   FFMPEG_OPTIONS), after=lambda e: play_next())
    else:
        is_playing = False
# cog_commands.send_message(client)

@client.event
async def q(ctx,*args):
    channel_id = args[0]
    while True:
        time = datetime.now().strftime("%H:%M:%S")
        if time >= "10:00:00" and time <= "10:10:00":
            post = quote_manager.quote_time()
            quoteObj = client.get_channel(int(environ.get("id")))
            await quoteObj.send(post)
            await asyncio.sleep((24*60*60)-100)
        else:
            await asyncio.sleep(1)

@client.event
async def on_ready():
    await client.wait_until_ready()
    print('We have logged in as {0.user}'.format(client))
    


# @client.command(name="help")
# async def help(ctx):
#         await ctx.send(help_message)


@client.command(name="play")
async def play(ctx, *args):
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel
    song = search_yt(query)
    if type(song) == type(True):
        await ctx.send("Error : Could not find/download the song.")
    else:
        await ctx.send("Song will be played!!")
        music_queue.append([song, voice_channel])
        hidden_music_queue.append([song, voice_channel])

        if is_playing == False:
            await play_music()


@client.command(name="queue")
async def queue(ctx):
    music_list_queue = ""
    for i in range(0, len(music_queue)):
        music_list_queue += music_queue[i][0]['title'] + "\n"

    print(music_list_queue)
    if music_list_queue != "":
        await ctx.send(music_list_queue)
    else:
        await ctx.send("Queue is empty!!")


@client.command()
async def pause(ctx):
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Error : Nothing playing!")


@client.command()
async def resume(ctx):
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    await voice.stop()


@client.command(name="skip")
async def skip(ctx):
    if voice != "" and voice:
        voice.stop()
        await play_music()


@client.command(name="previous")
async def previous(ctx):
    if voice != "" and voice:
        voice.stop()
        await play_music()


@client.command()
async def disconnect(ctx):
    global music_queue
    if voice.is_connected():
        await voice.disconnect()
        music_queue.clear()
    else:
        await ctx.send("Error : Bot is already diconnected!!")


@client.command()
async def m(ctx, *message):
    query = ""
    for word in message:
        query = query + word + " "
    print(query)
    response = requests.get(
        f"https://api.simsimi.net/v2/?text={query}&lc=en&cf=[chatfuel]")
    data = json.loads(response.text)
    reply = data['success']
    await ctx.send(reply)


client.run(environ.get("bot_token"))
