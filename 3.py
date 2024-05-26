def traduire(message):
    return translator.translate(message, "en", "fr").text


@bot.tree.command(name="traduction", description="traduit un message")
@discord.app_commands.describe(sentence="la phrase a traduire")
async def traduction(ctx: discord.interactions.Interaction, sentence: str):
    await ctx.response.send_message(traduire(sentence))