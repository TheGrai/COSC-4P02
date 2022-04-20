import random
import json
import pickle
import re
import datetime

import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.python.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intentsCG.json', errors="ignore").read())

words = pickle.load(open('wordsCG.pkl', 'rb'))
classes = pickle.load(open('classesCG.pkl', 'rb'))
model = load_model('chatbot_CG_model.h5')

listOfSports = ["Athletics", "Baseball", "Basketball", "Box Lacrosse", "Canoe Cayak", "Cycling", "Diving", "Golf", "Rowing", "Rugby Sevens", "Sailing", "Soccer", "Softball", "Swimming", "Tennis", "Triathon", "Volleyball", "Wrestling"]

listOfProvTerCodes = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
listOfProvTerNames = [["Newfoundland", "labrador"],["prince", "edward", "island"],["nova", "scotia"],["new", "brunswick"],["Quebec"],["Ontario"],["Manitoba"],
                      ["saskatchewan"],["alberta"],["british", "columbia", " bc "],["yukon"],["northwest", "territories"],["nunavut"]]

medalType = ["bronze", "silver", "gold"]
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    error_threshold = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > error_threshold]

    results.sort(key=lambda x: x[1], reverse=True)
    # results.reverse()
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json, message):
    topic = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['topic'] == topic:
            response = random.choice(i['responses'])
            if response == "athlete":
                course_regex = re.compile(r'[a-z]{4} *[0-5][a-z][0-9][0-9]')
                course = course_regex.search(message)
                if course is not None:
                    response = ["course", course.group()]
                    if re.search("term", message):
                        response.append("term")
                    elif re.search("who", message):
                        response.append("teacher")
                    elif re.search("lab", message):
                        response.append("lab")
                    elif re.search("prerequisite", message):
                        response.append("prerequisite")
                    else:
                        response.append("about")
                else:
                    response = "∆ Please provide a valid course code"

            elif response == "score":
                provter = None
                ind = 0
                for prv in listOfProvTerNames:
                    for nm in prv:
                        if re.search(nm, message, re.IGNORECASE):
                            provter = listOfProvTerCodes[ind]
                            break
                    ind = ind + 1
                    if provter is not None:
                        break
                if provter is not None:
                    response = ["score", provter]
                    mt = None
                    for tp in medalType:
                        if re.search(tp, message, re.IGNORECASE):
                            mt = tp
                            break
                    if mt is not None:
                        response.append(mt)
                else:
                    response = "∆ Please provide a valid Province/Territory"

            elif response == "schedule":
                response = ["schedule"]
                sport = None
                for sp in listOfSports:
                    if re.search(sp, message, re.IGNORECASE):
                            sport = sp
                            break
                if sport is not None:
                    response = ["schedule", sport]
                    provter = None
                    ind = 0
                    for prv in listOfProvTerNames:
                        for nm in prv:
                            if re.search(nm, message, re.IGNORECASE):
                                provter = listOfProvTerCodes[ind]
                                break
                        ind = ind + 1
                        if provter is not None:
                            break
                    if provter is not None:
                        response.append(provter)
                else:
                    response = "∆ Please provide a valid sport"
            elif response == "when":
                today = datetime.date.today()
                start = datetime.date(2022, 8, 6)
                timeTil = start - today

                response = "The Canada Website says the event starts in " + str(timeTil.days) + " days"

            return response


def respond(message):
    ints = predict_class(message)
    response = get_response(ints, intents, message)
    # for response in responses:
    #     print(response)
    print(response)


print("CANADA GAMES CHATBOT")
while True:
    respond(input(""))

