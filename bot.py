import discord
from os import environ
import requests
import json

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('.m'):
        query = message.content[3:]
        response = requests.get(f"https://api.simsimi.net/v2/?text={query}&lc=en&cf=[chatfuel]")
        data = json.loads(response.text)
        reply = data['success']
        await message.channel.send(reply)


client.run(environ.get("bot_token"))
