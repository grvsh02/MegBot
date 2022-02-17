import discord
from os import environ
import requests
import random
import json
import time

emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
rightwrong = ["✅", "❌", "❌", "❌"]


def gethelp():
    cats = """
        Correct way to give trivia command:
        "$trivia <number of questions> <category number>"
        
        Categories:
        1. General Knowledge
        2. Entertainment: Books
        3. Entertainment: Film
        4. Entertainment: Music
        5. Entertainment: Musicals & Theatres
        6. Entertainment: Television
        7. Entertainment: Video Games
        8. Entertainment: Board Games
        9. Science & Nature
        10. Science: Computers
        11. Science: Mathematics
        12. Science: Mythology
        13. Sports
        14. Geography
        15. History
        16. Politics
        17. Art
        18. Celebrities
        19. Animals
        20. Vehicles
        21. Entertainment: comics
        22. Science: Gadgets
        23. Entertainment: Japanese Anime & Manga
        24. Entertainment: Cartoons & Animations"""
    return cats


def getdata(numberofquestions, cat):
    trivia_url = f"https://opentdb.com/api.php?amount={numberofquestions}&category={cat}&type=multiple"
    qinput = "$trivia"
    a = requests.request('POST', trivia_url, json={"query": qinput[1:]})
    data = json.loads(a.text)
    return data


def showquestions(data):
    Outputs = []
    results = data['results']
    for i in results:
        Outputs.append(i)
    print(Outputs)
    for i in range(len(Outputs)):
        options = []
        category = Outputs[i]['category']
        qtype = Outputs[i]['type']
        question = str(Outputs[i]['question'])
        question = question.replace("&quot;", "\"")
        question = question.replace("&#039;", "\'")
        question = question.replace("&lt;", "<")
        question = question.replace("&gt;", ">")
        question = question.replace("&le;", "≤")
        question = question.replace("&ge;", "≥")
        options.append(Outputs[i]['correct_answer'])
        for j in Outputs[i]['incorrect_answers']:
            options.append(j)
        options.sort()
        options.reverse()
        c = []
        d = []
        for k in range(len(options)):
            d.append(emojis[k])
            c.append(options[k])
        inlineop = ""
        for i in range(len(c)):
            inlineop = inlineop + d[i] + c[i] + "\n "
        trivia = f"Category:{category} \n Type: {qtype}\n Question:\n {question} \n\n Options:\n {inlineop}"
        return trivia


def correctanswer(data):
    Outputs = []
    results = data['results']
    for i in results:
        Outputs.append(i)
    for i in range(len(Outputs)):
        options = []
        question = str(Outputs[i]['question'])
        question = question.replace("&quot;", "\"")
        question = question.replace("&#039;", "\'")
        question = question.replace("&lt;", "<")
        question = question.replace("&gt;", ">")
        question = question.replace("&le;", "≤")
        question = question.replace("&ge;", "≥")
        question = question.replace("&rsquo;", "\'")
        question = question.replace("&lsquo;", "\'")
        options.append(Outputs[i]['correct_answer'])
        for j in Outputs[i]['incorrect_answers']:
            options.append(j)
        c = []
        d = []
        for j in range(len(options)):
            c.append(rightwrong[j])
            d.append(options[j])
        inlineop = ""
        for i in range(len(c)):
            inlineop = inlineop+c[i]+d[i]+"\n "
        Correct_Ans = f"Question:\n {question} \n\n Options: \n {inlineop}"
        return Correct_Ans


def get_userdata():
    a = []


def checkifcorrect():
    correct = []
