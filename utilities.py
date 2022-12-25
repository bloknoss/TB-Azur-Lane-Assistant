import discord
from tb import AzurLaneTB
from discord.ext import commands

# Color headers for the terminal logging.
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

#These are embed generators for the different commands, they function based on the parameters passed on and then return an embed.
#Generates the skin embed.
def generateSkinEmbed(ship, selectedSkin):
    skins_embed = discord.Embed(title=selectedSkin['name'], color=ship.color)
    skins_embed.set_author(name=ship.fullname, icon_url=ship.shipyard)
    if selectedSkin['chibi'] != None:
        skins_embed.set_thumbnail(url=selectedSkin['chibi'])
    skins_embed.set_image(url=selectedSkin['url'])
    for cat in selectedSkin['info']:
        isInline = cat["category"] == "Availability" or 'Client' in cat["category"]
        skins_embed.add_field(name=cat["category"],
                        value=cat["value"], inline=isInline)
        if cat["category"] == "Availability":
            skins_embed.add_field(name='\u200b', value='\u200b')
            
    return skins_embed

#Generates the skills embed
def generateSkillsEmbed(ship: AzurLaneTB, selectedSkill):
    skills_embed = discord.Embed(title=selectedSkill['name'], color=selectedSkill['color'], description=selectedSkill['description'])
    skills_embed.set_author(name=ship.fullname, icon_url=ship.shipyard)
    skills_embed.set_thumbnail(url=ship.skins["skins"][0]['chibi'])
    
    return skills_embed

#Generates the artworks embed
def generateArtworksEmbed(ship:AzurLaneTB,selectedArtwork):
        art_embed = discord.Embed(title=selectedArtwork['artwork'], color=ship.color)
        art_embed.set_author(name=ship.fullname, icon_url=ship.shipyard)
        art_embed.set_thumbnail(url=ship.skins["skins"][0]['chibi'])
        art_embed.set_image(url=selectedArtwork['image'])
        art_embed.set_footer(text=f'{ship.name}\'s artworks')
        
        return art_embed


# This one is only used once in the code but I created it here so it doesn't occupy so much space on the commands cog code.
def generateShipEmbed(ship: AzurLaneTB):
    embed = discord.Embed(color=ship.color)
    embed.set_author(name=ship.fullname, icon_url=ship.shipyard)
    embed.set_thumbnail(url=ship.chibi)
    embed.set_footer(
        text="Sources:\nAzur Lane English Wiki\nAzur Lane's EN Community Tier List")
    for cat in ship.info['categories']:
        if cat["category"] != 'Full Name' and cat["category"] != "Image":
            embed.add_field(
                name=cat["category"], value="`" + cat["value"] + "`", inline=False)
    if ship.drops != None and ship.drops["maps"] != []:
        embed.add_field(name="Drops In", value="`" +
                        ship.drops['maps'][0]+f" and {len(ship.drops['maps'])-1} other(s).`")
    if ship.drops["notes"] != None and ship.drops["notes"] != []:
        notes = ''
        for note in ship.drops["notes"]:
            notes += '`'+note+'`\n'
        embed.add_field(name="Drop Notes", value=notes)
    if ship.tier != None:
        embed.add_field(name="Ranking", value="`" +
                        ship.tier["rank"] + "`", inline=False)
        if ship.tier["notes"] != []:
            notes = ''
            for note in ship.tier["notes"]:
                notes += f"`{note}`\n"
            embed.add_field(name="Ranking Notes",
                            value=notes.strip(), inline=False)
    return embed
