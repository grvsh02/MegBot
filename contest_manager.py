import json
import os
import discord
from datetime import datetime, timedelta
from dateutil import tz
import dateutil.parser
import requests


def get_contest(ctx, resource, name, image):
    C_API = os.getenv('api_key')
    USER_NAME = os.getenv('username')
    param_query = f"/?username={USER_NAME}&api_key={C_API}"
    nowTime = datetime.now().replace(microsecond=0)
    td = timedelta(10)
    futureTime = (nowTime + td).isoformat()
    embedVar = discord.Embed(title=f"Upcoming {name} Contests",
                             description="These are the list of upcoming contest which are less than 7 days away",
                             color=0x00ff00)
    parameters = {"resource": f"{resource}", "order_by": "-start",
                  "start_gte": f"{nowTime}", "start_lte": f"{futureTime}"}
    response = requests.get(
        f"https://clist.by/api/v2/contest/{param_query}", params=parameters)
    contests = response.json()["objects"]
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc_time = datetime.now()
    flag = 0
    for single in contests:
        event_name = single["event"]
        link = single["href"]
        duration = int(single['duration'])
        duration = round(duration / (60 * 60), 1)
        starts = dateutil.parser.parse(single['start'])
        utc_start_time = starts.replace(tzinfo=from_zone)
        india_start_time = utc_start_time.astimezone(to_zone)
        if 7 > (india_start_time.date() - utc_time.date()).days >= 0:
            flag = 1
            if resource == "codechef.com":
                embedVar.set_thumbnail(
                    url=f"https://clist.by/imagefit/static_resize/64x64/img/resources/codechef_com.ico")
            else:
                embedVar.set_thumbnail(
                    url=f"https://clist.by/imagefit/static_resize/64x64/img/resources/{image}.png")
            embedVar.add_field(name="Contest Name: ",
                               value=f"{event_name}", inline=False)
            embedVar.add_field(
                name="Timings: ",
                value=f"Date: {india_start_time.date()} ({(india_start_time.date() - utc_time.date()).days} day left)\nStart Time: {india_start_time.time()}\nDuration: {duration} hours",
                inline=False)
            embedVar.add_field(name="Registration link: ",
                               value=f"{link}", inline=False)
            embedVar.set_footer(
                text="All timings are in local time zone")
    if flag == 1:
        return embedVar
