from googletrans import Translator

def traduire_phrase(phrase, langue_source='fr', langue_destination='en'):
    translator = Translator()
    traduction = translator.translate(phrase, src=langue_source, dest=langue_destination)
    return traduction.text

phrase_a_traduire = "Bonjour, comment ça va ?"
langue_source = "fr"
langue_destination = "en"

traduction = traduire_phrase(phrase_a_traduire, langue_source, langue_destination)
return traduction