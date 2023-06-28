import discord
from discord import app_commands
from discord.ext import commands, tasks
from youtube_dl import YoutubeDL
from config import Guild_OBJ


class music_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = ""
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
    @app_commands.command(name = "play", description = "Puszcza wybraną piosenke.")
    async def p(self, ctx: discord.Interaction, args:str):
        qs = []
        qs.append(args)
        print(args)
        query = " ".join(qs)
        voice_channel = ctx.user.voice.channel
        if voice_channel is None:
            await ctx.response.send_message("Połącz się z kanałem głosowym aby aktywować bota.")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.response.send_message("Nie można pobrać piosenki spróbuj inną fraze bądź link.")
            else:
                await ctx.response.send_message("Piosenka dodana do kolejki.")
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music()
    @app_commands.command(name = "queue", description = "Pokazuje kolejke piosenek.")
    async def q(self, ctx: discord.Interaction):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"
        if retval != "":
            await ctx.response.send_message(retval)
        else:
            await ctx.response.send_message("Brak piosenek w kolejce")
    @app_commands.command(name = "skip", description = "Pomija piosenke.")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()
            await ctx.response.send_message("Pomijam piosenke.")
            
    @app_commands.command(name = "disconnect", description = "Opuszcza voicechat.")
    async def dc(self, ctx):
        await self.vc.disconnect()
        await ctx.response.send_message("Opuszczam voicechat")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(music_commands(bot), guilds=[Guild_OBJ])