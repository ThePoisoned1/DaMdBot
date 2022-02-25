from discord.ext import commands
from . import charaSearchCommands
from utils import utils,EmbedPaginatorView

class CharaSearchCog(commands.Cog, name="Character Search"):
    """
    Shows info about md characters
    """

    def __init__(self, bot,con):
        self.bot = bot
        self.con = con

    def getDescriptions():
        descriptions = {}
        descriptions['charaInfo'] = 'Shows info about a certain character'
        return descriptions

    descriptions = getDescriptions()

    @commands.command(name="charaInfo", aliases=['cinfo'], pass_context=True, brief="<Search>", description=descriptions.get('charaInfo'))
    async def charaInfo(self, ctx, *charaName):

        if isinstance(charaName, (list, tuple)):
            charaName = ' '.join(charaName)
        print(charaName)
        matches = charaSearchCommands.character_search(self.con, charaName)
        chara = None
        if len(matches) == 1:
            embed = charaSearchCommands.get_embed_from_chara(matches[0])
            chara = matches[0]
        elif len(matches) < 1:
            embed = [utils.errorEmbed('No character found')]
        elif len(matches) > 20:
            embed = [utils.errorEmbed('Too much results for that bro')]
        else:
            await utils.send_embed(ctx, charaSearchCommands.search_result_embed(matches, charaName))
            msg = await utils.getMsgFromUser(ctx, self.bot)
            if not msg or utils.cancelChecker(msg.content):
                await utils.send_msg(ctx, msg='Operation canceled')
                return
            chara = charaSearchCommands.character_search(self.con, msg.content)
            if chara:
                chara = chara[0]
            else:
                await utils.send_embed(ctx, utils.errorEmbed('No character found'))
                return
            embed = charaSearchCommands.get_embed_from_chara(chara)
        if len(embed)>1:
            view =EmbedPaginatorView.EmbedPaginatorView(ctx, embed, startPage=0)
            print(embed)
            await utils.send_embed(ctx, embed=embed[0], view=view)
        else:
            await utils.send_embed(ctx, embed[0])
        return chara


def setup(bot):
    bot.add_cog(CharaSearchCog(bot))
