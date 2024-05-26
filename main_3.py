from collections import Counter

from discord.ext.commands import Context
import re
from MBTITest import MBTITest
import discord
from discord.abc import Messageable
from discord.ext import commands

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

tester = MBTITest()


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')


@bot.command(name="mbti")
@discord.app_commands.describe(user="first value", nbr="number")
async def mbti(ctx: Context, user: str, nbr: int = 100):
    iduser = 0
    try:
        iduser = int(user.replace("<", "").replace(">", "").replace("@", ""))
    except:
        await ctx.send(f'need a user')

    messages: Messageable.history = ctx.channel.history(limit=nbr)

    backtick_pattern = r'```[^`]+```'

    mention_pattern = r'<@[^>]+>'

    url_pattern = r'https?://\S+'

    combined_pattern = f'({backtick_pattern}|{url_pattern}|{mention_pattern})'

    res = [ln for ln in
           [re.sub(combined_pattern, '', line.content) async for line in messages if line.author.id == iduser
            and not line.content.startswith("/") and not line.content.startswith(".")
            and not line.content.startswith("!")
            ] if len(ln) != 0]

    if len(res) == 0:
        await ctx.send(f'no messages')
        return

    predict1 = tester.predictEI(res)
    predict2 = tester.predictNS(res)
    predict3 = tester.predictTF(res)
    predict4 = tester.predictJP(res)

    occurrences1 = Counter(predict1).most_common()
    occurrences2 = Counter(predict2).most_common()
    occurrences3 = Counter(predict3).most_common()
    occurrences4 = Counter(predict4).most_common()

    await ctx.send(f'{occurrences1}\n{occurrences2}\n{occurrences3}\n{occurrences4}')


bot.run('Token')
