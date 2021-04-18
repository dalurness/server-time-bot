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
