from ssl import Options
import discord
from os import environ
import requests
import random
import json
import time
import random

emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
rightwrong = ["✅", "❌"]
correctAnswer = 0
options = []
question = ""


def gethelp():
    cats = """
**Correct way to give trivia command:**
```!trivia <number of questions> <category number>```
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


def showquestions(Outputs):
    global correctAnswer, options, question
    options = []
    category = Outputs['category']
    qtype = Outputs['type']
    question = str(Outputs['question'])
    question = question.replace("&quot;", "\"")
    question = question.replace("&#039;", "\'")
    question = question.replace("&lt;", "<")
    question = question.replace("&gt;", ">")
    question = question.replace("&le;", "≤")
    question = question.replace("&ge;", "≥")
    options.append(Outputs['correct_answer'])
    for j in Outputs['incorrect_answers']:
        options.append(j)
    random.shuffle(options)
    for index, option in enumerate(options):
        if option == Outputs['correct_answer']:
            correctAnswer = index
    inlineop = ""
    for i in range(len(options)):
        inlineop = inlineop + emojis[i] + "**" + options[i] + "**" + "\n"
    trivia = f"**Category:** {category} \n**Type:** {qtype}\n**Question:**\n```{question}```\n**Options:**\n{inlineop}"
    return trivia


def correctanswer():
    global correctAnswer, options, question
    inlineop = ""
    for i in range(4):
        if correctAnswer == i:
            inlineop = inlineop+rightwrong[0]+options[i]+"\n "
        else:
            inlineop = inlineop+rightwrong[1]+options[i]+"\n "
    ans_string = f"**Question:**\n```{question}```\n**Options:**\n{inlineop}"
    return ans_string, correctAnswer


def get_userdata():
    a = []


def checkifcorrect():
    correct = []
