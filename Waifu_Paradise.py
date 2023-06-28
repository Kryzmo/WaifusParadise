import discord
from discord.ext import commands
from config import token, app_id, intents, Guild_OBJ, Guild_ID
DEBUG = True


class Waifus(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            application_id=app_id)

    async def on_ready(self):
        print(f"hey {self.user}")
    
    async def setup_hook(self):
        await self.load_extension(f"cogs.basic_commands")
        await self.load_extension(f"cogs.music_commands")
        await self.load_extension(f"cogs.mod_commands")
        await bot.tree.sync(guild=Guild_OBJ)

if DEBUG == False:
    async def main():
        bot = Waifus()
        await bot.start(token)
    if __name__ == '__main__':
        import asyncio
        asyncio.get_event_loop().run_until_complete(main())
if DEBUG == True:
    bot = Waifus()
    bot.run(token)