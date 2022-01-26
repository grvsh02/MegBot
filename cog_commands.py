import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class cog_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""
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
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    def play_previous(self):
        if len(self.music_queue) >= 0:
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.music_queue.position -= 2
            is_playing = True
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Kindly connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song will be played!!")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command()
    async def pause(self, ctx):
        if self.vc.is_playing():
            self.vc.pause()
        else:
            await ctx.send("Currently no audio is playing.")


    @commands.command()
    async def resume(self, ctx):
        if self.vc.is_paused():
            self.vc.resume()
        else:
            await ctx.send("The audio is not paused.")


    @commands.command()
    async def stop(self, ctx):
        await self.vc.stop()

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()

    @commands.command(name="previous", help="Plays previous song!")
    async def previous(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()

    @commands.command()
    async def disconnect(self, ctx):
        global music_queue
        if self.vc.is_connected():
            await self.vc.disconnect()
            self.music_queue.clear()
        else:
            await ctx.send("The bot is not connected to a voice channel.")