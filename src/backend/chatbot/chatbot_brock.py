import random
import json
import pickle
import re
from brockU.models import *
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.python.keras.models import load_model
from difflib import SequenceMatcher

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
            if i['context_set'] == "course":
                course_regex = re.compile(r'[a-zA-Z]{4} *[0-5][a-zA-z][0-9][0-9]')
                courseID = course_regex.search(message)
                if courseID is not None:
                    try:
                        course = Course.objects.get(code__iexact=courseID.group())
                        if topic == "about":
                            if course.description != "":
                                response = course.code + ", " + course.name + ", is a course that can be described as " + course.description
                            else:
                                response = course.code + ", " + course.name + ", does not have a description."
                        if topic == "when":
                            courseOfferings = CourseOffering.objects.filter(course_id=course.id)
                            response = course.code + ", " + course.name + ", runs from " + courseOfferings[0].start_date.strftime("%B %d %Y") + " to " + courseOfferings[0].end_date.strftime("%B %d %Y")
                        elif topic == "instructor":
                            courseOfferings = CourseOffering.objects.filter(course_id=course.id)
                            for option in courseOfferings:
                                try:
                                    instructor = option.instructor_id
                                    if instructor is not None:
                                        response = course.code + ", " + course.name + ", is run by instructor " + instructor.first_name + " " + instructor.last_name
                                        break
                                except Instructor.DoesNotExist:
                                    response = "ERROR: Could not grab instructor."
                            if response == "course":
                                response = course.code + ", " + course.name + ", does not have an instructor."
                        elif topic == "lab":
                            labOfferings = CourseOffering.objects.filter(delivery_type=CourseOffering.DeliveryType.LABORATORY)
                            courseOfferings = labOfferings.filter(course_id=course.id)
                            gen = False
                            response = course.code + " - " + course.name + " has "
                            for option in courseOfferings:
                                    gen = True
                                    schedule = option.schedule
                                    response += " Lab " + str(option.section)
                                    if schedule.items():
                                        response += " that runs "
                                        for key, value in schedule.items():
                                            print(key + " " + value)
                                            response += (key + " " + value)
                                    if option.location != '':
                                        response += " located at " + option.location
                                    response += "."
                            if not gen:
                                response = "There are no labs for the requested course " + course.code
                        elif topic == "seminar":
                            labOfferings = CourseOffering.objects.filter(delivery_type=CourseOffering.DeliveryType.SEMINAR)
                            courseOfferings = labOfferings.filter(course_id=course.id)
                            gen = False
                            response = course.code + " - " + course.name + " has "
                            for option in courseOfferings:
                                    gen = True
                                    schedule = option.schedule
                                    response += " Seminar " + str(option.section)
                                    if schedule.items():
                                        response += " that runs "
                                        for key, value in schedule.items():
                                            print(key + " " + value)
                                            response += (key + " " + value)
                                    if option.location != '':
                                        response += " located at " + option.location
                                    response += "."
                            if not gen:
                                response = "There are no seminars for the requested course " + course.code
                        elif topic == "prerequisite":
                            if course.prerequesites != "":
                                response = course.code + ", " + course.name + ", has prerequisite(s) " + course.prerequesites
                            else:
                                response = course.code + ", " + course.name + ", does not have any prerequisites."
                    except Course.DoesNotExist:
                        response = "Hmmm, I can't seem to find information on this course."
                else:
                    response = "∆ Please provide a valid course code"

            elif i['context_set'] == "exam":
                try:
                    course = Course.objects.get(code__iexact=courseID.group())
                    exams = Exam.object.filter(course_id=course.id)
                    if topic == "about":
                        response = ""
                        for exam in exams:
                            response += exam.code + " section " + exam.section +"'s exam will be taking place at " + exam.location + " on " + exam.date.strftime("%B %d %Y") + " at " + exam.start_time + "."
                    elif topic == "where":
                        response = ""
                        for exam in exams:
                            response += exam.code + " section " + exam.section + "'s exam will be taking place at " + exam.location
                    elif topic == "when":
                        response = ""
                        for exam in exams:
                            response += exam.code + " section " + exam.section + "'s exam will be taking place on " + exam.date.strftime("%B %d %Y") + " at " + exam.start_time + "."
                except Exam.DoesNotExist:
                    response = "Hmmm, I can't seem to find information on this course exam. You can access the exam timetable here: https://www.brocku.ca/guides-and-timetables/exams/"

            elif topic == "program":
                subjectOfferings = Subject.objects.all()
                possibleSubjects = []
                bestSub = ""
                for subject in subjectOfferings:
                    lowerName = subject.name.lower()
                    substrings = lowerName.split()
                    lowerMessage = message.lower()
                    if any(substring in lowerMessage for substring in substrings):
                        possibleSubjects.append(subject)
                        bestSub = subject
                        #response = "The " + subject.name + " program at Brock University was found. It can be described as: " + subject.description + " More information about the program can be found here: " + subject.url
                    else:
                        response = "The program you were asking about at Brock University was not found. Perhaps it is under a different name. You can try to find it here: https://brocku.ca/webcal/"

                if bestSub is not "":
                    for pSub in possibleSubjects:
                            if SequenceMatcher(None, pSub.name, message).ratio() > SequenceMatcher(None, bestSub.name, message).ratio():
                                bestSub = pSub
                    response = "The " + bestSub.name + " program at Brock University was found. It can be described as: " + bestSub.description + " More information about the program can be found here: " + bestSub.url
                else:
                    response = "Hmmm. I could not find anything about the program you are asking for. Perhaps it is under a different name. You can try to find it here: https://brocku.ca/webcal/"

            else:
                response = random.choice(i['responses'])
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

