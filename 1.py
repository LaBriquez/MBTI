@bot.command(name="mbti")
@discord.app_commands.describe(user="first value", nbr="number")
async def mbti(ctx: Context, user: str, nbr: int = 100):
    iduser = 0
    try:
        iduser = int(user.replace("<", "").replace(">", "").replace("@", ""))
    except:
        await ctx.send(f'need a user')
        return

    messages: Messageable.history = ctx.channel.history(limit=nbr)

    res = [line.content async for line in messages if line.author.id == iduser]

    base_values = {'E': 0.0, 'I': 0.0, 'N': 0.0, 'S': 0.0, 'T': 0.0, 'F': 0.0, 'J': 0.0, 'P': 0.0}

    cpt = 0

    for ln in res:
        if ln.startswith("/") or ln.startswith(".") or ln.startswith("!") or ln.startswith("https://tenor.com/view"):
            continue
        cpt += 1
        tester.MBTIadder(base_values, ln)

    for p, v in base_values.items():
        print(p, v)

    ein = (base_values["I"] ** 2 + base_values["E"] ** 2)**0.5
    nsn = (base_values["N"] ** 2 + base_values["S"] ** 2)**0.5
    ftn = (base_values["F"] ** 2 + base_values["T"] ** 2)**0.5
    pjn = (base_values["P"] ** 2 + base_values["J"] ** 2)**0.5

    eival = f"E ({int(base_values['E'] / ein * 100)}%)" if base_values["I"] < base_values["E"] \
        else f"I ({int(base_values['I'] / ein * 100)}%)"

    nsval = f"N ({int(base_values['N'] / nsn * 100)}%)" if base_values["S"] < base_values["N"] \
        else f"S ({int(base_values['S'] / nsn * 100)}%)"

    tfval = f"T ({int(base_values['T'] / ftn * 100)}%)" if base_values["F"] < base_values["T"] \
        else f"F ({int(base_values['F'] / ftn * 100)}%)"

    pjval = f"P ({int(base_values['P'] / pjn * 100)}%)" if base_values["J"] < base_values["P"] \
        else f"J ({int(base_values['J'] / pjn * 100)}%)"

    await ctx.send(f'{eival} {nsval} {tfval} {pjval} for {cpt} messages')