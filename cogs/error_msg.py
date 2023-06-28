import discord

async def Error(ctx):
    embed = discord.Embed(title='Nastąpił error!', color=111111)
    await ctx.response.send_message(embed=embed)