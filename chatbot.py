import telegram
import spacy
import json
from spacy.matcher import Matcher
TOKEN = ""
bot = telegram.Bot(token=TOKEN)
from telegram.ext import Updater, MessageHandler, Filters

data_file = open('data.json')

data = json.load(data_file)
data_file.close()

category_example_1 = [
    {"DEP": "pobj", "POS":"NOUN"},
    {"DEP": "prep"},
    {"DEP": "pobj", "POS": "PROPN"}
]

category_example_1 = [
    {"DEP": "pobj", "POS":"NOUN"},
    {"DEP": "prep"},
    {"DEP": "pobj", "POS": "PROPN"}
]
category_example_2 = [
    {"DEP": "det"},
    {"DEP": "compound"},
    {"POS": "NOUN"}
]
category = [category_example_1 , category_example_2]

location_example_1 = [
    {"DEP": "amod"},
    {"DEP": "prep"},
    {"ENT_TYPE": "GPE"}

]
location_example_2 = [
    {"POS": "AUX"},
    {"DEP": "advmod"},
    {"DEP": "prep"},
    {"DEP": "pobj"}
]
location = [location_example_1 , location_example_2]

company_example_1 = [
    {"DEP": "aux"},
    {"DEP": "nsubj", "ENT_TYPE": "ORG"},
]
company_example_2 = [
    {"POS": "ADP"},
    {"DEP": "pobj", "ENT_TYPE": "ORG"},
]
company = [company_example_1 , company_example_2]

job_type_example_1 = [
    {"POS": "VERB"},
    {"DEP": "amod"},
    {"DEP": "dobj", "OP" : "?"}
]
job_type_example_2 = [
    {"POS": "AUX", "OP": "?"},
    {"DEP": "compound"},
    {"DEP": "attr"},
]
job_type = [job_type_example_1 , job_type_example_2]

experience_example_1 = [
    {"POS": "VERB"},
    {"DEP": "amod", "OP": "?"},
    {"DEP": "dobj"},
]
experience_example_2 = [
    {"POS": "ADV", "OP": "?"},
    {"DEP": "advmod", "OP": "?"},
    {"DEP": "amod"},
    {"POS": "NOUN"}
]
experience_example_3 = [
    {"DEP": "det"},
    {"DEP": "compound"}
]
experience = [experience_example_1 , experience_example_2, experience_example_3]

matchers = {
    "category": category,
    "location": location,
    "company": company,
    "job_type": job_type,
    "experience": experience
}



nlp = spacy.load('en_core_web_sm')
pattern_matchers = {}
matcher = Matcher(nlp.vocab)

for name, patterns in matchers.items():
    matcher = Matcher(nlp.vocab)
    matcher.add(name, patterns)
    pattern_matchers[name] = matcher


def utterance(update, context):
    msg = update.message.text
    doc = nlp(msg)
    matches = matcher(doc)
    for name, matcher in pattern_matchers.items():
        matches = matcher(doc)
        for match_id, start, end in matches:
            if(name == "category"):
                category = match[2]



updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text, utterance))
updater.start_polling()
updater.idle()
