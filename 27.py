replace_word = [...]

def valid_message(line: discord.message.Message):
    backtick_pattern = r''

    mention_pattern = r'<@[^>]+>'

    url_pattern = r'https?://\S+'

    combined_pattern = f'({backtick_pattern}|{url_pattern}|{mention_pattern})'

    return not line.content.startswith("/") and not line.content.startswith(".") \
        and not line.content.startswith("!") \
        and not line.author.bot \
        and re.sub(combined_pattern, '', line.content) != ""


def correct(message: str):
    splited = message.split(" ")

    new_line = []

    for word in splited:
        new_word = word
        for w in replace_word:
            if w[0] == word:
                new_word = w[1]
        new_line.append(new_word)

    return " ".join(new_line)

if not valid_message(message):
    return

content = correct(message.content)
print(content)