import discord
from discord import Interaction
from discord.ext import commands

from MBTI import analize_side_content, force_side, mbti_values, analize_NS, analize_TF, get_doc, get_blob, get_sia, \
    ego_size
from corrector import valid_message, correct

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')


@bot.tree.command(name="mbti", description="send mbti")
@discord.app_commands.describe(user="user")
async def mbti(ctx: Interaction, user: str = ""):
    try:
        id = int(user.replace("<@", "").replace(">", "")) \
            if user != "" else ctx.user.id
    except Exception as e:
        await ctx.response.send_message(f"need a valid user")
        return

    if id not in force_side.keys():
        await ctx.response.send_message(f"there is no <@{id}> on the holocrons")
        return

    await ctx.response.send_message(
        f"<@{id}> : N {mbti_values[id]["N"]:.2f} / S {mbti_values[id]["S"]:.2f}"
        f", T {mbti_values[id]["T"]:.2f} / F {mbti_values[id]["F"]:.2f}"
        f", Ego {mbti_values[id]["Ego"]:.2f}")


@bot.tree.command(name="side", description="send side")
@discord.app_commands.describe(user="user")
async def side(ctx: Interaction, user: str = ""):
    try:
        id = int(user.replace("<@", "").replace(">", "")) \
            if user != "" else ctx.user.id
    except Exception as e:
        await ctx.response.send_message(f"need a valid user")
        return

    if id not in force_side.keys():
        await ctx.response.send_message(f"there is no <@{id}> on the holocrons")
        return

    side = force_side[id]
    print(side)

    compound = side['compound'] / side['total']

    img = ("images/Jedi.jpg", "is a great and powerful jedi") if compound > 0.55 \
        else ("images/Sith.jpg", "has fallen to the dark side") if compound < 0.45 \
        else ("images/GreyJedi.jpg", "is a grey jedi balanced in the force")

    print(f"<@{id}> ({int(compound * 100)}%)")

    await ctx.response.send_message(f"<@{id}> {img[1]}", file=discord.File(open(img[0], 'rb')))


@bot.event
async def on_message(message: discord.message.Message):
    if not valid_message(message):
        return

    content = correct(message.content)
    print(content)

    analize_side_content(message, content)

    if message.author.id not in mbti_values.keys():
        mbti_values[message.author.id] = {
            "N": 0.0,
            "S": 0.0,
            "T": 0.0,
            "F": 0.0,
            "Ego": 0.0
        }

    doc = get_doc(content)
    blob = get_blob(content)
    sia = get_sia(content)

    s, n = analize_NS(doc)
    f, t = analize_TF(doc, blob, sia)

    ego_moment = ego_size(doc)

    mbti_values[message.author.id]["Ego"] += ego_moment

    mbti_values[message.author.id]["N"] += n
    mbti_values[message.author.id]["S"] += s

    mbti_values[message.author.id]["F"] += f
    mbti_values[message.author.id]["T"] += t


bot.run("Token")
