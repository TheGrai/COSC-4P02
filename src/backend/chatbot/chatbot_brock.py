import os
import random
import json
import pickle
import re
from brockU.models import *

import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.python.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('chatbot/intents.json', errors="ignore").read())

words = pickle.load(open('chatbot/words.pkl', 'rb'))
classes = pickle.load(open('chatbot/classes.pkl', 'rb'))
model = load_model('chatbot/chatbot_brock_model.h5')


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
    if len(intents_list) != 0:
        topic = intents_list[0]['intent']
    else:
        topic = 'unknown'
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['topic'] == topic:
            response = random.choice(i['responses'])
            if response == "course":
                course_regex = re.compile(r'[a-zA-Z]{4} *[0-5][a-zA-z][0-9][0-9]')
                courseID = course_regex.search(message)
                if courseID is not None:
                    try:
                        course = Course.objects.get(code__iexact=courseID.group())

                        if re.search("term", message):
                            response.append("term")
                        elif re.search("who", message) or re.search("professor", message) or re.search("prof", message):
                            courseOfferings = CourseOffering.objects.filter(course_id=course.id)
                            for option in courseOfferings:
                                if option.instructor_id is not None:
                                    try:
                                        instructor = Instructor.objects.get(id=option.instructor_id)
                                        response = course.code + ", " + course.name + ", is run by instructor " + instructor.first_name + " " + instructor.last_name
                                    except:
                                        response = "ERROR: Could not grab instructor. "
                                    break
                        elif re.search("lab", message):
                            response.append("lab")
                        elif re.search("prerequisite", message):
                            if course.prerequesites != "":
                                response = course.code + ", " + course.name + ", has prerequisite(s) " + course.prerequesites
                            else:
                                response = course.code + ", " + course.name + ", does not have any prerequisites."

                        else:
                            response.append("about")
                    except Course.DoesNotExist:
                        response = "Hmmm, I can't seem to find information on this course."
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
                    if re.search("requirement", message) or re.search("get into", message):
                        response.append("requirement")
                    else:
                        response.append("about")
                else:
                    response = "∆ Please provide a better question about the program"

            return response


def respond(message):
    ints = predict_class(message)
    response = get_response(ints, intents, message)
    # for response in responses:
    print(message)
    print(response)
    return response


print("BROCK CHATBOT")
while False:
    respond(input(""))

