import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
from cogs.error_msg import Error
import typing;import requests
import random

from config import Guild_OBJ, Guild_ID, rules_id, accept_role_id, rules_channel_id

class basic_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == int(rules_id) and payload.emoji.name == "SataniaThumbsUp":
            guild = self.bot.get_guild(int(Guild_ID))
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=int(accept_role_id))
            await member.add_roles(role)
            try:
                ch = self.bot.get_channel(rules_channel_id)
                msg = await ch.fetch_message(payload.message_id)
                await msg.add_reaction("SataniaThumbsUp")
            except:
                pass
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == int(rules_id) and payload.emoji.name == "SataniaThumbsUp":
            guild = self.bot.get_guild(int(Guild_ID))
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, id=int(accept_role_id))
            await member.remove_roles(role)

    @app_commands.command(name = "art", description = "Daje zwykłego arta.")
    @app_commands.describe(tag="Podaj tag.")
    @app_commands.choices(tag= [
        Choice(name="uniform", value="uniform"),
        Choice(name="maid", value="maid"),
        Choice(name="waifu", value="waifu"),
        Choice(name="marin-kitagawa", value="marin-kitagawa"),
        Choice(name="mori-calliope", value="mori-calliope"),
        Choice(name="raiden-shogun", value="raiden-shogun"),
        Choice(name="oppai", value="oppai"),
        Choice(name="selfies", value="selfies"),
        Choice(name="ass", value="ass"),
        Choice(name="hentai", value="hentai"),
        Choice(name="milf", value="milf"),
        Choice(name="oral", value="oral"),
        Choice(name="paizuri", value="paizuri"),
        Choice(name="ecchi", value="ecchi"),
        Choice(name="ero", value="ero"),
    ])
    # @app_commands.describe(choices=['uniform', 'maid', 'waifu', 'marin-kitagawa', 'mori-calliope', 'raiden-shogun', 'oppai', 'selfies', 'ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero', 'deamovsky', None])
    async def art_command(self, ctx: discord.Interaction, tag: typing.Optional[str]):
        try:
            existing_list = ['uniform', 'maid', 'waifu', 'marin-kitagawa', 'mori-calliope', 'raiden-shogun', 'oppai', 'selfies', 'ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero', 'deamovsky', None]
            if tag in existing_list or None:
                if tag == None:
                    url = 'https://api.waifu.im/search/?included_tags=waifu'
                else:
                    url = 'https://api.waifu.im/search/?included_tags={}'.format(tag)
                r = requests.get(url)
                r_js = r.json()
                forbbiden_list = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero', 'deamovsky']
                # forbbiden_list = ['deamovsky']
                if tag in forbbiden_list:
                    embed = discord.Embed(title='Hentai!')
                    embed.set_image(url='https://c.tenor.com/t2pLAIENp_EAAAAC/anime-kanna.gif')
                    embed.set_footer(text = 'TokyoSubs', icon_url = "https://cdn.discordapp.com/attachments/980807266657792133/1053122406211923968/tumblr_fbaaebf3604af1fb9d5c0ee62b3cb316_8c6cfa87_1280.jpg")
                    await ctx.response.send_message(embed=embed)
                else:
                    for i in r_js['images']:
                        embed_color = '{}'.format(i['dominant_color']).replace('#', '')
                        embed_color_decimal = int(embed_color, 16)
                        embed = discord.Embed(title='Obrazek', color=embed_color_decimal)
                        embed.set_image(url='{}'.format(i['url']))
                        embed.set_footer(text = 'Waifus Paradise', icon_url = "https://cdn.discordapp.com/attachments/980807266657792133/1053122406211923968/tumblr_fbaaebf3604af1fb9d5c0ee62b3cb316_8c6cfa87_1280.jpg")
                        await ctx.response.send_message(embed=embed)
            elif tag == 'kyu':
                await ctx.response.send_message('Nikt jeszcze nie fotografował mędrca.') 
            else:
                await ctx.response.send_message('Nie posiadam takiego tagu!')
        except:
            await Error(ctx)

    @app_commands.command(name = "r34", description = "Daje losowy obrazek z rule34.")
    async def rule34_command(self, ctx: discord.Interaction, tag: str):
        try:
            url = f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags={tag}&json=1&limit=1000"
            try:
                r = requests.get(url).json()
                arts = []
                for i in r:
                    arts.append(i['file_url'])
                embed = discord.Embed(title='Rule34', color=111111)
                embed.set_image(url='{}'.format(random.choice(arts)))
                embed.set_footer(text = 'Waifus Paradise', icon_url = "https://cdn.discordapp.com/attachments/980807266657792133/1053122406211923968/tumblr_fbaaebf3604af1fb9d5c0ee62b3cb316_8c6cfa87_1280.jpg")
                await ctx.response.send_message(embed=embed)
                # print(random.choice(arts))
            except:
                embed = discord.Embed(title='Wybrany tag nie istnieje!', color=111111)
                await ctx.response.send_message(embed=embed)
                # print("Podany tag nie istnieje")
        except:
            await Error(ctx)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(basic_commands(bot), guilds=[Guild_OBJ])