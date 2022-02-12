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
current_track = 0
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
voice = ""
greeting_message = "Hey there! I am your new music assistant!!"
help_message = """
!help - Shows this message
!play <song_name> - Plays the song
!queue - displays the current music queue
!skip - skips to the next song
!previous - Plays previous played song
!disconnect - bot leaves from current vc
"""


def search_yt(item):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info("ytsearch:%s" %
                                    item, download=False)['entries'][0]
        except Exception:
            return False

    return {'source': info['formats'][0]['url'], 'title': info['title']}


async def send_music_info(ctx, embed):
    print("hello")
    await ctx.send(embed=embed)


def play_next(ctx):
    global is_playing, current_track
    if len(music_queue) > 0:
        is_playing = True
        print(current_track, len(music_queue))
        if current_track < len(music_queue) - 1:
            current_track += 1
        else:
            current_track = 0
        video_source = music_queue[current_track][0]['source']
        voice.play(discord.FFmpegPCMAudio(video_source, **
                   FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
        embed = discord.Embed(title="Track info",
                              description=f"**Playing track {current_track + 1}**\n```{music_queue[current_track][0]['title']}```", color=discord.Color.blue())
        client.loop.create_task(ctx.send(embed=embed))
    else:
        is_playing = False

# def play_previous():
#     if len(music_queue) >= 0:
#         video_source = hidden_music_queue[0][0]['source']
#         is_playing = True
#         voice.play(discord.FFmpegPCMAudio(video_source, **FFMPEG_OPTIONS), after=lambda e: play_previous())
#     else:
#         is_playing = False


async def play_music(ctx):
    global is_playing, voice
    if len(music_queue) > 0:
        is_playing = True
        video_source = music_queue[current_track][0]['source']

        if voice == "" or not voice.is_connected() or voice == None:
            voice = await music_queue[0][1].connect()
            voice.play(discord.FFmpegPCMAudio(video_source, **
                                              FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
        else:
            await voice.move_to(music_queue[0][1])

    else:
        is_playing = False
# cog_commands.send_message(client)


@client.event
async def on_ready():
    await client.wait_until_ready()
    print('We have logged in as {0.user}'.format(client))
    while True:
        time = datetime.now().strftime("%H:%M:%S")
        if time >= "10:00:00" and time <= "10:10:00":
            post = quote_manager.quote_time()
            quoteObj = client.get_channel(int(environ.get("id")))
            embed = discord.Embed(title="Queue info",
                                  description=f"**{post}**", color=discord.Color.blue())
            await quoteObj.send(embed=embed)
            await asyncio.sleep((24*60*60)-100)
        else:
            await asyncio.sleep(1)


# @client.command(name="help")
# async def help(ctx):
#         await ctx.send(help_message)

@client.command(name="hello")
async def hello(ctx):
    await ctx.send(greeting_message)


@client.command(name="play")
async def play(ctx, *args):
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel
    song = search_yt(query)
    if type(song) == type(True):
        embed = discord.Embed(title="Error info",
                              description=f"**Error : Could not find/download the song.**", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        music_queue.append([song, voice_channel])
        embed = discord.Embed(title="Track info",
                              description=f"**Added to Queue at Track {len(music_queue)}:**\n```{music_queue[-1][0]['title']}```", color=discord.Color.blue())
        await ctx.send(embed=embed)
        if is_playing == False:
            await play_music(ctx)


@client.command(name="queue")
async def queue(ctx):
    music_list_queue = ""
    for i in range(0, len(music_queue)):
        if i == current_track:
            music_list_queue += "🎶" + music_queue[i][0]['title'] + "\n"
        else:
            music_list_queue += "  " + music_queue[i][0]['title'] + "\n"
    print(music_list_queue)
    if music_list_queue != "":
        embed = discord.Embed(title="Queue info",
                              description=f"```{music_list_queue}```", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Queue info",
                              description=f"**Queue is empty!!**", color=discord.Color.blue())
        await ctx.send(embed=embed)


@client.command()
async def pause(ctx):
    if voice.is_playing():
        voice.pause()
    else:
        embed = discord.Embed(title="Error info",
                              description=f"**Error : nothing is playing**", color=discord.Color.blue())
        await ctx.send(embed=embed)


@client.command()
async def resume(ctx):
    if voice.is_paused():
        voice.resume()
    else:
        embed = discord.Embed(title="Error info",
                              description=f"**The audio is not paused.**", color=discord.Color.blue())
        await ctx.send(embed=embed)


@client.command()
async def stop(ctx):
    await voice.stop()


@client.command(name="skip")
async def skip(ctx, *args):
    global current_track
    if args != () and voice != "" and voice and int(args[0]) > 0 and int(args[0]) <= len(music_queue):
        current_track = int(args[0]) - 2
        voice.stop()
    elif voice != "" and voice:
        voice.stop()


@client.command(name="previous")
async def previous(ctx):
    global current_track
    if voice != "" and voice:
        current_track -= 2
        voice.stop()


@client.command()
async def disconnect(ctx):
    global music_queue
    if voice.is_connected():
        await voice.disconnect()
        music_queue.clear()
    else:
        embed = discord.Embed(title="Error info",
                              description=f"**Error : Bot is already diconnected!!**", color=discord.Color.blue())
        await ctx.send(embed=embed)


@client.command()
async def remove(ctx, *args):
    global current_track, music_queue
    if int(args[0]) > 0 and int(args[0]) <= len(music_queue):
        embed = discord.Embed(title="Track info",
                              description=f"**Removed track {args[0]}**\n```{music_queue[int(args[0])-1][0]['title']}```", color=discord.Color.blue())
        await ctx.send(embed=embed)
        music_queue.pop(int(args[0]) - 1)


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
