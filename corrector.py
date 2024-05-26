import re

import discord

replaced_sent = [
    ("c t", "c'était"),
    ("je c", "je sais"),
    ("tu c", "tu sais"),
    ("il c", "il sait"),
    ("je t", "je t'ai"),
    ("hm hm", "j'en doute"),
    ("mh mh", "j'en doute"),
]

regexW = re.compile(r'[^?!"()\[\]{}\-,:]')
regexO = re.compile(r'[?!"()\[\]{}\-,:]')

replace_word = [
    ("ct", "c'était"),
    ("kel", "quel"),
    ("tema", "regarde"),
    ("impec", "impeccable"),
    ("toutafé", "tout à fait"),
    ("toutafer", "tout à fait"),
    ("toutafez", "tout à fait"),
    ("toutafe", "tout à fait"),
    ("mwa", "moi"),
    ("oim", "moi"),
    ("tj", "toujours"),
    ("ouaip", "ouais"),
    ("reuf", "frère"),
    ("chépa", "je ne sais pas"),
    ("awi", "ah oui"),
    ("tavu", "tu as vu"),
    ("dakor", "d'accord"),
    ("pb", "problème"),
    ("pbs", "problèmes"),
    ("mtn", "maintenant"),
    ("bcp", "beaucoup"),
    ("mek", "mec"),
    ("oe", "oui"),
    ("oé", "oui"),
    ("ui", "oui"),
    ("nn", "non"),
    ("fo", "faut"),
    ("fé", "fait"),
    ("fè", "fait"),
    ("k'on", "qu'on"),
    ("k'un", "qu'un"),
    ("k'1", "qu'un"),
    ("keske", "qu'est ce que"),
    # ("wesh", "salut"),
    ("vazi", "vas y"),
    ("azi", "vas y"),
    ("btw", "d'ailleurs"),
    ("cad", "c'est à dire'"),
    ("càd", "c'est à dire'"),
    ("vénère", "énervé"),
    ("vénere", "énervé"),
    ("venere", "énervé"),
    ("venère", "énervé"),
    ("bo", "beau"),
    ("qq", "quelque"),
    ("osef", "on s'en fou"),
    ("v", "vais"),
    ("kssé", "cassé"),
    ("ksser", "cassé"),
    ("ksse", "cassé"),
    ("att", "attend"),
    ("koi", "quoi"),
    ("kwa", "quoi"),
    ("kan", "quand"),
    ("komment", "comment"),
    ("komen", "comment"),
    ("kommen", "comment"),
    ("koment", "comment"),
    ("coment", "comment"),
    ("C", "c'est"),
    ("c", "c'est"),
    ("c", "c'est"),
    ("G", "J'ai"),
    ("g", "j'ai"),
    ("t", "tu es"),
    ("t'es", "tu es"),
    ("t'as", "tu as"),
    ("ptdr", ":joy:"),
    ("mdr", ":joy:"),
    ("lol", ":joy:"),
    ("XDD", ":joy:"),
    (":joy:", "lol"),
    ("tkt", "ne t'inquiète pas"),
    ("np", "pas de problème"),
    ("awé", "ah oui"),
    ("aba", "ah bah"),
    ("chuis", "je suis"),
    ("chui", "je suis"),
    ("ke", "que"),
    ("pk", "pourquoi"),
    ("pt", "pété"),
    ("tt", "tout"),
    ("ttes", "toutes"),
    ("ts", "tous"),
    ("ki", "qui"),
    ("voc", "vocal"),
    ("bi1", "bien"),
    ("obvious", "évident"),
    ("trad", "traduction"),
    ("kouzin", "cousin"),
    ("kouz", "cousin"),
    ("cous", "cousin"),
    ("kous", "cousin"),
    ("couz", "cousin"),
    ("hmhm", "j'en doute")
]


def manage_text(sentence: str):
    words = sentence.split(' ')

    all_final_words = []

    for w in words:
        words = [s for s in regexO.split(w) if s != ""]
        others = [s for s in regexW.split(w) if s != ""]

        if len(words) == 0:
            all_final_words.append("".join(others))
            continue

        if len(others) == 0:
            new_words = []
            for word in words:
                new_word = word
                for rw in replace_word:
                    if rw[0] == word:
                        new_word = rw[1]
                new_words.append(new_word)

            all_final_words.append("".join(new_words))
            continue

        first_o = "".join(regexO.split(w[0])) == ""

        new_words = []

        for word in words:
            new_word = word
            for rw in replace_word:
                if rw[0] == word:
                    new_word = rw[1]
            new_words.append(new_word)

        final_sentence = []

        while len(new_words) + len(others) != 0:
            wo = new_words.pop(0) if len(new_words) != 0 else ""
            ot = others.pop(0) if len(others) != 0 else ""

            final_sentence.append(ot + wo if first_o else wo + ot)

        all_final_words.append("".join("".join(final_sentence)))

    return " ".join(all_final_words)


def valid_message(line: discord.message.Message):
    backtick_pattern = r'```[^`]+```'

    mention_pattern = r'<@[^>]+>'

    url_pattern = r'https?://\S+'

    combined_pattern = f'({backtick_pattern}|{url_pattern}|{mention_pattern})'

    return not line.content.startswith("/") and not line.content.startswith(".") \
        and not line.content.startswith("!") \
        and not line.author.bot \
        and re.sub(combined_pattern, '', line.content) != ""


def correct(message: str):
    new_message = message.lower()
    for s in replaced_sent:
        last_index = 0
        while s[0] in new_message[last_index:]:
            index = new_message.index(s[0])
            last_index = index + len(s[0])
            if index + len(s[0]) < len(new_message) and new_message[index + len(s[0])] == " ":
                new_message = new_message[:index] + s[1] + new_message[index + len(s[0]):]

            if index + len(s[0]) >= len(new_message):
                new_message = new_message[:index] + s[1]

    return manage_text(new_message)
