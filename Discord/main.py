import io
import random

import discord
import requests
from discord.ext import commands
from config import settings



def get_my_files(content):
    f = io.BytesIO(content)
    my_file = discord.File(f)
    return my_file


class MyBot(commands.Cog):
    async def send(self, message, text=None, file=None):
        await message.channel.send(text, file=file)

    async def on_message(self, message):
        msg = message.content.lower()
        if "hi" in msg:
            await self.send(message, text="И тебе привет")
        if "кошка" in msg:
            response = requests.get("https://some-random-api.ml/animal/fox")
            data = response.json()
            if response.status_code == 200:
                await self.send(message, file=get_my_files(data["image"]))

    @commands.command(name='randint')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)

bot = commands.Bot(command_prefix='!!')
bot.add_cog(MyBot(bot))
bot.run(settings['token'])
