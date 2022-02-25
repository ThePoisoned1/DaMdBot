from objects.SaoMdObjects import Chara
from utils import databaseUtils
import discord
import os

buffer = {}
def character_search(con, search: str):
    if not buffer.get('charas'):
        update_buffer(con)
    matches = []
    search = search.lower()
    for chara in buffer['charas']:
        if search == str(chara.id) or search == chara.unitName.lower() or search == ' '.join((chara.charaName,chara.unitName)):
            return chara
        if search in chara.unitName.lower() or search in chara.charaName.lower():
            matches.append(chara)
    return matches

def get_character_pic(charaId,imageFolder):
    imgPath = f'{imageFolder}/character{charaId}.png'
    if os.path.isfile(imgPath):
        return

def get_embed_from_chara(chara:Chara):
    embed = discord.Embed(title=f'{chara.charaName} *{chara.unitName}*')
    embed.add_field(name='ID',value=str(chara.id))
    embed.add_field(name='Character',value=chara.charaName)
    embed.add_field(name='Unit',value=chara.unitName)
    embed.add_field(name='Rarity',value=chara.rarity)
    embed.add_field(name='Weapon',value=chara.weapon)
    embed.add_field(name='Element',value=chara.element)
    if len(chara.charaPics)==1:
        embed.set_image(url = chara.charaPics[0])
        return [embed]
    else:
        embeds = []
        for i in range(len(chara.charaPics)):
            aux = embed.copy()
            aux.set_image(url = chara.charaPics[i])
            embeds.append(aux)
        return embeds

def search_result_embed(matches, search):
    seaches = '\n'.join(f'-{chara.charaName} {chara.unitName}'for chara in matches)
    embed = discord.Embed(
        title=f'Search results for {search}', description=seaches, color=discord.Color.dark_blue())
    embed.set_footer(text='Type one of the options above')
    return embed

def update_buffer(con):
    allcharasDb = databaseUtils.select(con, 'chara')
    buffer['charas'] = [Chara.from_db(dbchara) for dbchara in allcharasDb]
