# CURRENTLY DOWN AND WAITING FOR SUPPORT 
I have taken the bot down and not updated it due to a flaw in the discord API. I have contacted their support for help but have not been able to solve the issue up to this point. The base function of the bot is deleting and then re-creating a channel with the proper time displayed. Over time as the bot runs on the server, the discord API will fail to delete the channel it created at a seemingly random time. That channel then goes into a sort of corrupted state, where it will not allow you to delete it through the api or through any of the GUI interfaces (mobile, pc, or web). This has caused me and others some frustration, as it clogs up your server with channels that cannot be deleted (it will continue to happen. The most I have had at one time is 5). Until this problem is resolved, I do not plan on allowing the bot to run. Sorry for the inconvenience and I hope as much as you do that I can display a consistent time in my servers in the near future.

# Server Time Bot
### Get started

------------

To add the bot to your server, make sure you have administrative permissions and go to [https://discord.com/oauth2/authorize?client_id=832760856302845984&scope=bot&permissions=3088](https://discord.com/oauth2/authorize?client_id=832760856302845984&scope=bot&permissions=3088)

Once the bot has been added, enter this command to start the clock (replacing "America/Denver" with your desired timezone):
`clock--set_timezone America/Denver`

Valid timezones can be found at [https://en.wikipedia.org/wiki/List_of_tz_database_time_zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) in the "TZ database name" section.

------------


### Commands
##### prefix="clock--"
------------

##### clock--set_timezone (timezone name) [twelve_hour]
Starts the server clock given a valid timezone name as shown at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones in the "TZ database name" section and can optionally show time in 12 hour clock.

##### clock--stop
Stops the server clock and deletes the associated voice channel

##### clock--help
Displays help message showing available commands.

# Due to Discord Rate Limits, the clock will always be slightly off.
