import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz

#import logging

#logging.basicConfig(level=logging.INFO)


from dotenv import load_dotenv
import os

load_dotenv()

# Client
client = commands.Bot(command_prefix='clock--', help_command=None)

timezone = None
saved_guild = None
twelve_hour = False

@tasks.loop(seconds=30)
async def update_time():
    if timezone == None or saved_guild == None:
        return
    
    time_string = str(datetime.now(timezone).strftime('%H:%M'))
    
    if int(time_string.split(":")[0]) == 0:
        time_string = "12:" + time_string.split(":")[1]

    # handle twelve hour
    if twelve_hour and int(time_string.split(":")[0]) > 12:
        time_string = str(int(time_string.split(":")[0]) - 12) + ":" + time_string.split(":")[1]

    new_title = 'servertime ' + time_string

    #update previous channel
    channel_exists = False
    for channel in saved_guild.channels:
        first_word = channel.name.split(" ")[0]
        if first_word == 'servertime':
            channel_exists = True
            await channel.edit(name=new_title)
            break

    #create new channel
    if not channel_exists:
        await saved_guild.create_voice_channel(new_title)

@update_time.before_loop
async def before_update_time():
    await client.wait_until_ready()

@update_time.after_loop
async def after_update_time():
    print('loop has stopped')

@client.command(name='set_timezone')
async def set_timezone(context, *args):
    global saved_guild
    global timezone
    global twelve_hour
    global update_time
    try:
        timezone = pytz.timezone(args[0])
    except:
        await context.send('Invalid Timezone. Please visit https://en.wikipedia.org/wiki/List_of_tz_database_time_zones in the "TZ database name" section.')
        return
    
    if len(args) == 2:
        if args[1] == "twelve_hour":
            twelve_hour = True

    if saved_guild != None:
        return

    saved_guild = context.guild

    update_time.start()

@client.command(name='stop')
async def stop(context):
    global timezone
    global twelve_hour
    global saved_guild
    global update_time
    timezone = None
    twelve_hour = None
    
    update_time.cancel()

    for channel in saved_guild.channels:
        first_word = channel.name.split(" ")[0]
        if first_word == 'servertime':
            channel_exists = True
            await channel.delete()
            break

    saved_guild = None

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
client.run(os.getenv("SECRET_CODE"))