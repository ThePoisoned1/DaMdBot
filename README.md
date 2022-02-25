# DaSaoMdBot
Source code of the discord bot made for the SAOMD revival proyect

## Setup
-Check the gitignore to avoid uploading the bot conf and any other sensitive data

1. Create the bot.
    If u need help with this step there is a step by step on [Create a bot](./Templates/Create_a_bot.md).

2. Set up the requirements.
    Execute the commented lines in [requirements](./requirements.txt)

3. Create the conf file.
    Configuration files are not shared in the repo due to privacy and security matters, same goes for the databases.
    you need to create a conf-pro.conf and a conf-dev.pro, paste all the contents in the [configuration templates](./conf/conf-pro-template.conf) and fill that data with your private values.

4. Start the database.
    To start the database u have to run the [database starter](dbStarter.py) from the main folder

5. Start the bot.
    To start the bot just run [main.py](main.py) from the main folder


## Adding new commands
Trying to keep the code structure as clean as possible the bot is stucturated in cogs. Each cog contains a bundle of commands with the same theme. It's cog is created in a separate folder under the [Cogs folder](./cogs/). Each of this folders contains the Cog file and the commands file. 

1. The Cog File
    The [Cog File](./cogs/help/helpcog.py) contains the events and methods that are triggered when the command happens. I there is a [Template](./Templates/CogTemplate.py) for it that u can use to help u make new cogs.

2. Structure for the help command
    The help command is coded to add all the cogs that have any non-owner-only command and all the public commands in them.
    The description and brief will be shown for each of those commands. The brief is used to show the needed parameters for that interaction. It has the following naming < required > (optional) \[alias\]

3. The Command File
    The [Command File](./cogs/help/helpcommands.py) contains the mayority of the logic executed when the commands within the same cog are used. This way it keeps the Cog File as clean as possible

Any questions about the pycord library feel free to contact me or use the [Official documentation](https://docs.pycord.dev/en/master/)
