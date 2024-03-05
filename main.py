from discord.ext.commands import Context
import re
from MBTITest import MBTITest
import discord
from discord.abc import Messageable
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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

    base_values = {'E': 0.0, 'I': 0.0, 'N': 0.0, 'S': 0.0, 'T': 0.0, 'F': 0.0, 'J': 0.0, 'P': 0.0}

    for ln in res:
        tester.MBTIadder(base_values, ln)

    """ein = (base_values["I"] ** 2 + base_values["E"] ** 2) ** 0.5
    nsn = (base_values["N"] ** 2 + base_values["S"] ** 2) ** 0.5
    ftn = (base_values["F"] ** 2 + base_values["T"] ** 2) ** 0.5
    pjn = (base_values["P"] ** 2 + base_values["J"] ** 2) ** 0.5

    eival = f"E ({int(base_values['E'] / ein * 100)}%)" if base_values["I"] < base_values["E"] \
        else f"I ({int(base_values['I'] / ein * 100)}%)"

    nsval = f"N ({int(base_values['N'] / nsn * 100)}%)" if base_values["S"] < base_values["N"] \
        else f"S ({int(base_values['S'] / nsn * 100)}%)"

    tfval = f"T ({int(base_values['T'] / ftn * 100)}%)" if base_values["F"] < base_values["T"] \
        else f"F ({int(base_values['F'] / ftn * 100)}%)"

    pjval = f"P ({int(base_values['P'] / pjn * 100)}%)" if base_values["J"] < base_values["P"] \
        else f"J ({int(base_values['J'] / pjn * 100)}%)"""

    eival = f"E ({int(base_values['E'])}|{int(base_values['I'])})" if base_values["I"] < base_values["E"] \
        else f"I ({int(base_values['I'])}|{int(base_values['E'])})"

    nsval = f"N ({int(base_values['N'])}|{int(base_values['S'])})" if base_values["S"] < base_values["N"] \
        else f"S ({int(base_values['S'])}|{int(base_values['N'])}"

    tfval = f"T ({int(base_values['T'])}|{int(base_values['F'])})" if base_values["F"] < base_values["T"] \
        else f"F ({int(base_values['F'])}|{int(base_values['T'])})"

    pjval = f"P ({int(base_values['P'])}|{int(base_values['J'])})" if base_values["J"] < base_values["P"] \
        else f"J ({int(base_values['J'])}|{int(base_values['P'])})"

    await ctx.send(f'{eival} {nsval} {tfval} {pjval} for {len(res)} messages')


bot.run("MTA3NzMwMDkyNTgxNjkxMzk0MA.G3SR-C.LfWDQ03AlXsI3JkuW189fePlD8iUOihxLyFoB8")
