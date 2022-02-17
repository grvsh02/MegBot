
import discord
from os import environ
import requests
import json
import time
import scrap
import asyncio

client = discord.Client()
trivia_url = "https://opentdb.com/api.php?amount=10"
a = requests.request('POST', trivia_url)
temojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
quiz_api = environ.get("api_token")
solving_time = 15


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! ')

    if message.content.startswith('.m'):
        query = message.content[3:]
        response = requests.get(
            f"https://api.simsimi.net/v2/?text={query}&lc=en&cf=[chatfuel]")
        data = json.loads(response.text)
        reply = data['success']
        await message.channel.send(reply)

    if message.content.startswith("$trivia help"):
        a = scrap.gethelp()
        await message.channel.send(a)

    elif message.content.startswith('$trivia'):
        n = int(message.content[8:10])
        if int(message.content[10:]) == '':
            c = 8
        else:
            c = int(message.content[10:]) + 8
        for i in range(n):
            b = scrap.getdata(n, c)
            a = scrap.showquestions(b)
            rmsg = f"""```{a}```"""
            z = await message.channel.send(rmsg)
            await z.add_reaction("1️⃣")
            await z.add_reaction("2️⃣")
            await z.add_reaction("3️⃣")
            await z.add_reaction("4️⃣")
            id_of_z = await message.channel.fetch_message(z.id)
            users = []
            await asyncio.sleep(5)
            reactions = id_of_z.reactions.flatten
            print(reactions)
            print(type(reactions[0]))
            for reaction in reactions:
                print(reaction.count)
                async for user in reaction.users():
                    users.append(user)
                    print(reaction.emoji)
            print(users)
            for i in users:
                print(i)
            await z.delete()
            remsg = scrap.correctanswer(b)
            sendcrt = f"""```{remsg}```"""
            await message.channel.send(sendcrt)

    if (message.content.lower() == "!yell2"):
        msg = await message.channel.send("whoa")
        await msg.add_reaction("😮")


client.run("OTM1ODM5NDQyODMxMjkwNDQ4.YfEeZg.fkOLnpHRF15s0H6L5TD1Y8IHy3I")
