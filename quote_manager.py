import requests
import json
from os import environ


def quote_time():
    quote_key = environ.get('qoute_token')
    while True:
        quote_json = requests.get(
            f"https://zenquotes.io/api/quotes/{quote_key}")
        quote_data = json.loads(quote_json.text)
        quote = quote_data[0]["q"]
        author = quote_data[0]["a"]
        post = f"Good Morning folks !! \nHere is a beautiful quote to start your day ;-) \n \n{quote} \n\n~{author} \n"
        return post
