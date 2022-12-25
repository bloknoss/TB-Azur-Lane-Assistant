import discord
from TB import AzurLaneTB
from discord.ext import commands



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def generateSkinEmbed(ship,selectedSkin):
    embed = discord.Embed(title=selectedSkin['name'],color=ship.color)
    embed.set_author(name=ship.fullname, icon_url=ship.shipyard)
    embed.set_thumbnail(url=selectedSkin['chibi'])
    embed.set_image(url=selectedSkin['url'])
    for cat in selectedSkin['info']:
        isInline = cat["category"] == "Availability" or 'Client' in cat["category"]
        embed.add_field(name=cat["category"],value=cat["value"],inline=isInline)
        if cat["category"] == "Availability":
            embed.add_field(name='\u200b', value='\u200b')
    return embed

def generateSkillsEmbed(ship : AzurLaneTB ,selectedSkill):
    embed = discord.Embed(title=selectedSkill['name'],color=selectedSkill['color'],description=selectedSkill['description'])
    embed.set_author(name=ship.fullname, icon_url=ship.shipyard)
    embed.set_thumbnail(url=ship.skins["skins"][0]['chibi'])
    return embed