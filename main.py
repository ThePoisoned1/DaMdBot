import os

# discord
import discord
from discord.ext import commands

# utils
from utils import utils,databaseUtils

# conf
import configparser

#cogs
from cogs.errorhandler import errorhandlercog
from cogs.help import helpcog
from cogs.dastuff import dastuffcog
from cogs.charaSearch import charaSearchCog



def addCogs(bot,conf,con):
    bot.add_cog(errorhandlercog.CommandErrorHandler(bot,conf['log']['path']))
    bot.add_cog(helpcog.HelpCog(bot,conf['bot']))
    bot.add_cog(dastuffcog.DaStuffCog(bot,con,conf))
    bot.add_cog(charaSearchCog.CharaSearchCog(bot,con))
    pass


def startBot(conf,updateCharas):
    intents = discord.Intents.default()
    intents.members = True
    activity = utils.getBotActivity(
        conf['bot']['activity_type'], conf['bot']['avtivity_msg'], url=conf['bot']['streaming_url'])
    status = utils.getBotStatus(conf['bot']['status'])
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or(conf['bot']['prefix']), activity=activity, status=status, help_command=None, intents=intents,case_insensitive=True)

    @ bot.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(bot.user.name + "#" + bot.user.discriminator)
        print(bot.user.id)
        print('------')

    @ bot.check
    def check_commands(ctx):
        infor = f"{ctx.message.created_at} -> {ctx.message.author} <{ctx.message.author.id}> in '{ctx.guild} <{ctx.guild.id}>': {ctx.message.content}"
        # utils.addToLog(ctx.message.created_at, ctx.message.author,
        # ctx.message.author.id, ctx.guild, ctx.guild.id, ctx.message.content)
        return ';' not in ctx.message.content
    con = databaseUtils.connectToDb(conf['database']['path'])
    addCogs(bot,conf,con)
    # start the bot
    bot.run(conf['bot']['token'])


def getConf(profile):
    conf = configparser.ConfigParser()
    pyProfile = os.environ.get('PYTHON_PROFILE', profile)
    conf.read(os.path.join('conf', f'conf-{pyProfile}.conf'))
    return conf


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Starts the discord bot')
    parser.add_argument('--update', '-u', action='store_true',
                        help='Runs a character update in the database')
    parser.add_argument('-dev', action='store_true',
                        help='Runs the bot with the development conf')
    args = parser.parse_args()
    profile = 'dev' if args.dev else 'pro'

    updateCharas = args.update
    conf = getConf(profile)
    startBot(conf, updateCharas)

