import discord
from discord import app_commands
from discord.ext import commands, tasks
from cogs.error_msg import Error
import typing;import requests
import random
import re
import datetime
from config import modlog_id, Guild_OBJ

class mod_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    async def timeout_user(self, *, user_id: int, guild_id: int, until: int, reason_mute: str):
        headers = {"Authorization": f"Bot {self.bot.http.token}", "X-Audit-Log-Reason": reason_mute}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        if until is not None:
            timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
        else:
            timeout = None
        json = {'communication_disabled_until': timeout}
        import aiohttp
        self.bot.session = aiohttp.ClientSession()
        async with self.bot.session.patch(url, json=json, headers=headers) as session:
            if session.status in range(200, 299):
                return True
        return False


    @app_commands.command(name = "mute", description = "Wycisza użytkownika.")
    async def mute(self, ctx: discord.Interaction, member: str, until: int, reason: str):
            try:
                if int(until) <= 40320:
                    if reason is not None:
                        member_id = re.findall("[0-9]", member)
                        # print(int(''.join(member_id)))
                        guild = await self.bot.fetch_guild(ctx.guild.id)
                        user = await guild.fetch_member(int(''.join(member_id)))
                        user_mod = await guild.fetch_member(ctx.user.id)
                        handshake = await self.timeout_user(user_id=int(''.join(member_id)), guild_id=ctx.guild.id, until=int(until), reason_mute=reason)
                        if handshake:
                            modlog = self.bot.get_channel(int(modlog_id))
                            embed = discord.Embed(title=f'**{user}**', color=16249435, description=f"**Powód**\n{reason}")
                            embed.add_field(name='User ID:', value=int(''.join(member_id)), inline=True)
                            embed.add_field(name='Mod ID:', value=ctx.user.id, inline=True)
                            embed.add_field(name='Czas trwania:', value=f"{until} min.", inline=True)
                            embed.add_field(name='Kiedy:', value=datetime.datetime.now())
                            embed.add_field(name='Typ:', value='Mute', inline=True)
                            embed.set_footer(text = f'Przez: {user_mod}', icon_url = "https://cdn.discordapp.com/attachments/980807266657792133/1053122406211923968/tumblr_fbaaebf3604af1fb9d5c0ee62b3cb316_8c6cfa87_1280.jpg")
                            await modlog.send(embed=embed)
                            return await ctx.response.send_message(f"Wyciszono {member} na {until} minut. Z powodu \"{reason}\"")
                        await ctx.response.send_message("Coś poszło nie tak.")
                    else:
                        await ctx.response.send_message("Musisz podać powód!")
                else:
                    await ctx.response.send_message("Za duża wartość!")

            except Exception as e:
                print(e)
                print(member)
                await ctx.response.send_message("Podano złego użytkownika bądz czas.")

    @app_commands.command(name = "unmute", description = "Odcisza użytkownika.")
    async def unmute(self, ctx: discord.Interaction, member: str, reason: str):
            try:
                if reason is not None:
                    member_id = re.findall("[0-9]", member)
                    # print(int(''.join(member_id)))
                    guild = await self.bot.fetch_guild(ctx.guild.id)
                    user = await guild.fetch_member(int(''.join(member_id)))
                    user_mod = await guild.fetch_member(ctx.user.id)
                    handshake = await self.timeout_user(user_id=int(''.join(member_id)), guild_id=ctx.guild.id, until=None, reason_mute=reason)
                    if handshake:
                        modlog = self.bot.get_channel(int(modlog_id))
                        embed = discord.Embed(title=f'**{user}**', color=3145631, description=f"**Powód**\n{reason}")
                        embed.add_field(name='User ID:', value=int(''.join(member_id)), inline=True)
                        embed.add_field(name='Mod ID:', value=ctx.user.id, inline=True)
                        embed.add_field(name='Kiedy:', value=datetime.datetime.now())
                        embed.add_field(name='Typ:', value='Unmute', inline=True)
                        embed.set_footer(text = f'Przez: {user_mod}', icon_url = "https://cdn.discordapp.com/attachments/980807266657792133/1053122406211923968/tumblr_fbaaebf3604af1fb9d5c0ee62b3cb316_8c6cfa87_1280.jpg")
                        await modlog.send(embed=embed)
                        return await ctx.response.send_message(f"Odciszono {member}. Z powodu \"{reason}\"")
                    await ctx.response.send_message("Coś poszło nie tak.")
                else:
                    await ctx.response.send_message("Musisz podać powód!")
            except Exception as e:
                print(e)
                # print(member)
                await ctx.response.send_message("Podano złego użytkownika.")

    @app_commands.command(name = "ban", description = "Banuje użytkownika.")
    async def ban(self, ctx: discord.Interaction, member: str, *, reason: str):
        try:
            if reason is not None:
                member_id = re.findall("[0-9]", member)
                guild = await self.bot.fetch_guild(ctx.guild.id)
                user = await guild.fetch_member(''.join(member_id))
                user_mod = await guild.fetch_member(ctx.user.id)
                modlog = self.bot.get_channel(int(modlog_id))
                # print(ConfigLoad['modlog'])
                embed = discord.Embed(title=f'**{user}**', color=16711680, description=f"**Powód**\n{reason}")
                embed.add_field(name='User ID:', value=int(''.join(member_id)), inline=True)
                embed.add_field(name='Mod ID:', value=ctx.user.id, inline=True)
                embed.add_field(name='Kiedy:', value=datetime.datetime.now())
                embed.add_field(name='Typ:', value='Ban', inline=True)
                embed.set_footer(text = f'Przez: {user_mod}', icon_url = "https://cdn.discordapp.com/attachments/980807266657792133/1053122406211923968/tumblr_fbaaebf3604af1fb9d5c0ee62b3cb316_8c6cfa87_1280.jpg")
                await modlog.send(embed=embed)
                await member.ban(reason = reason)
                return await ctx.response.send_message(f'Użytkownik {member} został zbanowany!')
            else:
                await ctx.response.send_message('Nie podano powodu!')
        except:
            await ctx.response.send_message('Nie znaleziono użytkownika.')

    @app_commands.command(name = "unban", description = "Odbanowywuje użytkownika.")
    async def unban(self, ctx: discord.Interaction, id: int, reason: str):
        if reason is not None:
            print(id)
            user = await self.bot.fetch_user(id)
            guild = await self.bot.fetch_guild(ctx.guild.id)
            user_mod = await guild.fetch_member(ctx.user.id)
            modlog = self.bot.get_channel(int(modlog_id))
            # print(ConfigLoad['modlog'])
            embed = discord.Embed(title=f'**{user}**', color=255, description=f"**Powód**\n{reason}")
            embed.add_field(name='User ID:', value=id, inline=True)
            embed.add_field(name='Mod ID:', value=ctx.user.id, inline=True)
            embed.add_field(name='Kiedy:', value=datetime.datetime.now())
            embed.add_field(name='Typ:', value='Unban', inline=True)
            embed.set_footer(text = f'Przez: {user_mod}', icon_url = "https://cdn.discordapp.com/attachments/980807266657792133/1053122406211923968/tumblr_fbaaebf3604af1fb9d5c0ee62b3cb316_8c6cfa87_1280.jpg")
            await modlog.send(embed=embed)
            await ctx.response.send_message('Użytkownik został odbanowany!')
            await ctx.guild.unban(user)
        else:
            await ctx.response.send_message('Nie podano powodu!')

    # KICK COMMAND ##
    @app_commands.command(name = "kick", description = "Wyrzuca użytkownika.")
    async def kick(self, ctx: discord.Interaction, member: str, reason:str):
        if reason is not None:
            member_id = re.findall("[0-9]", member)
            guild = await self.bot.fetch_guild(ctx.guild.id)
            user = await guild.fetch_member(int(''.join(member_id)))
            user_mod = await guild.fetch_member(ctx.user.id)
            modlog = self.bot.get_channel(int(modlog_id))
            # print(ConfigLoad['modlog'])
            embed = discord.Embed(title=f'**{user}**', color=14001047, description=f"**Powód**\n{reason}")
            embed.add_field(name='User ID:', value=int(''.join(member_id)), inline=True)
            embed.add_field(name='Mod ID:', value=ctx.user.id, inline=True)
            embed.add_field(name='Kiedy:', value=datetime.datetime.now())
            embed.add_field(name='Typ:', value='Kick', inline=True)
            embed.set_footer(text = f'Przez: {user_mod}', icon_url = "https://cdn.discordapp.com/attachments/980807266657792133/1053122406211923968/tumblr_fbaaebf3604af1fb9d5c0ee62b3cb316_8c6cfa87_1280.jpg")
            await modlog.send(embed=embed)
            await ctx.response.send_message(f"{member} został wyrzucony z powodu: \"{reason}\"")
            await member.kick(reason=reason)
        else:
            await ctx.response.send_message("Nie podano powodu!")

    @app_commands.command(name = "clear", description = "Czyści wiadomości.")
    async def clear(self, ctx: discord.Interaction, amount: int):
        amount = int(amount)
        if amount != "":
            if amount > 50:
                await ctx.response.send_message('Nie można usunąć więcej niż 50!')
            else:
                await ctx.channel.purge(limit=amount + 1)
        else:
            await ctx.response.send_message('Nie podano ilości!')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(mod_commands(bot), guilds=[Guild_OBJ])
