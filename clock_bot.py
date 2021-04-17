import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz

import logging

logging.basicConfig(level=logging.INFO)


from dotenv import load_dotenv
import os

load_dotenv()

# Client
client = commands.Bot(command_prefix='clock--', help_command=None)

saved_guilds = []

def get_time(timezone, twelve_hour):
    time_string = str(datetime.now(timezone).strftime('%H:%M'))
    
    if int(time_string.split(":")[0]) == 0:
        time_string = "12:" + time_string.split(":")[1]

    is_pm = False
    if int(time_string.split(":")[0]) == 12:
        is_pm = True

    # handle twelve hour
    if twelve_hour and int(time_string.split(":")[0]) > 12:
        is_pm = True
        time_string = str(int(time_string.split(":")[0]) - 12) + ":" + time_string.split(":")[1]

    am_pm = ""
    if twelve_hour == True:
        am_pm = "pm" if is_pm else "am"

    time_string = 'servertime ' + time_string + am_pm
    return time_string

@tasks.loop(minutes=1)
async def update_time():
    global saved_guilds

    #update previous channel
    for saved_guild in saved_guilds:
        new_title = get_time(saved_guild["timezone"], saved_guild["twelve_hour"])
        channel_exists = False
        for channel in saved_guild["guild"].channels:
            first_word = channel.name.split(" ")[0]
            if first_word == 'servertime':
                await channel.delete()
                #channel_exists = True
                #await channel.edit(name=new_title)
                #break

        #create new channel
        if not channel_exists:
            await saved_guild["guild"].create_voice_channel(new_title)

async def initialize_timekeeper(context, timezone, twelve_hour):
    new_title = get_time(timezone, twelve_hour)
    channel_exists = False
    for channel in context.guild.channels:
        first_word = channel.name.split(" ")[0]
        if first_word == 'servertime':
            await channel.delete()
            #channel_exists = True
            #await channel.edit(name=new_title)
            #break

    #create new channel
    if not channel_exists:
        await context.guild.create_voice_channel(new_title)

@update_time.before_loop
async def before_update_time():
    await client.wait_until_ready()

@update_time.after_loop
async def after_update_time():
    print("loop unexpectedly ended")

@client.command(name='set_timezone')
async def set_timezone(context, *args):
    global saved_guilds
    twelve_hour = False

    try:
        timezone = pytz.timezone(args[0])
    except:
        await context.send('Invalid Timezone. Please visit https://en.wikipedia.org/wiki/List_of_tz_database_time_zones in the "TZ database name" section.')
        return

    if len(args) == 2:
        if args[1] == "twelve_hour":
            twelve_hour = True

    #check if we are just changing the timezone of this guild
    for saved_guild in saved_guilds:
        if context.guild.id == saved_guild["guild"].id:
            saved_guild["timezone"] = timezone
            saved_guild["twelve_hour"] = twelve_hour
            return

    saved_guilds.append({"guild": context.guild, "timezone": timezone, "twelve_hour": twelve_hour})

    await initialize_timekeeper(context, timezone, twelve_hour)

@client.command(name='stop')
async def stop(context):
    # remove channel
    for channel in context.guild.channels:
        first_word = channel.name.split(" ")[0]
        if first_word == 'servertime':
            await channel.delete()
            break

    await context.send("Server Clock has been deactivated")

@client.command(name='help')
async def help_funct(context):
    em = discord.Embed(title = "Help", color=context.author.color)
    em.add_field(name="clock--set_timezone (timezone name) [twelve_hour]",
        value="""Starts the server clock given a valid timezone name as \
            shown at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones \
            in the "TZ database name" section and can optionally show time in 12 \
            hour clock.""")
    em.add_field(name="clock--stop", value="Stops the server clock and deletes the associated voice channel")

    await context.send(embed=em)

# run the client on server
update_time.start()
client.run(os.getenv("SECRET_CODE"))
