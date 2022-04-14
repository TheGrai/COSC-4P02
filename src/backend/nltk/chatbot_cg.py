import random
import json
import pickle
import re

import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.python.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intentsCG.json', errors="ignore").read())

words = pickle.load(open('wordsCG.pkl', 'rb'))
classes = pickle.load(open('classesCG.pkl', 'rb'))
model = load_model('chatbot_CG_model.h5')


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
            if response == "course":
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

            elif response == "exam":
                course_regex = re.compile(r'[a-z]{4} *[0-5][a-z][0-9][0-9]')
                course = course_regex.search(message)
                if course is not None:
                    response = ["exam", course.group()]
                    if re.search("when", message) or re.search("time", message):
                        response.append("time")
                    elif re.search("where", message) or re.search("location", message):
                        response.append("location")
                    else:
                        response.append("about")
                else:
                    response = "∆ Please provide a valid course code"

            elif response == "program":
                program_regex = re.compile(r'[a-z]* program')
                program = program_regex.search(message)
                if program is not None:
                    response = ["program", program.group()]
                    if re.search("requirement", message):
                        response.append("requirement")
                    else:
                        response.append("about")
                else:
                    response = "∆ idk"

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

