import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class cog_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue = []
        self.hidden_music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.voice = ""
        self.greeting_message = "Hey there! I am your new music assistant!!"
        self.help_message = """
!help - Shows this message
!play <song_name> - Plays the song
!queue - displays the current music queue
!skip - skips to the next song
!previous - Plays previous played song
!disconnect - bot leaves from current vc
"""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            video_source = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.voice.play(discord.FFmpegPCMAudio(video_source, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    def play_previous(self):
        if len(self.music_queue) >= 0:
            video_source = self.hidden_music_queue[0][0]['source']
            self.is_playing = True
            self.voice.play(discord.FFmpegPCMAudio(video_source, **self.FFMPEG_OPTIONS), after=lambda e: self.play_previous())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            video_source = self.music_queue[0][0]['source']

            if self.voice == "" or not self.voice.is_connected() or self.voice == None:
                self.voice = await self.music_queue[0][1].connect()
            else:
                await self.voice.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)

            self.voice.play(discord.FFmpegPCMAudio(video_source, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(self.greeting_message)

    @commands.command(name="play")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        song = self.search_yt(query)
        if type(song) == type(True):
            await ctx.send("Error : Could not find/download the song.")
        else:
            await ctx.send("Song will be played!!")
            self.music_queue.append([song, voice_channel])
            self.hidden_music_queue.append([song, voice_channel])
                
            if self.is_playing == False:
                await self.play_music()

    @commands.command(name="queue")
    async def queue(self, ctx):
        music_list_queue = ""
        for i in range(0, len(self.music_queue)):
            music_list_queue += self.music_queue[i][0]['title'] + "\n"

        print(music_list_queue)
        if music_list_queue != "":
            await ctx.send(music_list_queue)
        else:
            await ctx.send("Queue is empty!!")

    @commands.command()
    async def pause(self, ctx):
        if self.voice.is_playing():
            self.voice.pause()
        else:
            await ctx.send("Error : Nothing playing!")


    @commands.command()
    async def resume(self, ctx):
        if self.voice.is_paused():
            self.voice.resume()
        else:
            await ctx.send("The audio is not paused.")


    @commands.command()
    async def stop(self, ctx):
        await self.voice.stop()

    @commands.command(name="skip")
    async def skip(self, ctx):
        if self.voice != "" and self.voice:
            self.voice.stop()
            await self.play_music()

    @commands.command(name="previous")
    async def previous(self, ctx):
        if self.voice != "" and self.voice:
            self.voice.stop()
            await self.play_music()

    @commands.command()
    async def disconnect(self, ctx):
        global music_queue
        if self.voice.is_connected():
            await self.voice.disconnect()
            self.music_queue.clear()
        else:
            await ctx.send("Error : Bot is already diconnected!!")