import discord
import json
from tb import AzurLaneTB
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from controls import skinsMenuView, skillsMenuView, artworksMenuView, Buttons
from utilities import bcolors, generateSkinEmbed, generateSkillsEmbed, generateShipEmbed,generateArtworksEmbed

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f"{bcolors.OKBLUE}[{time_now}] The commands module has loaded succesfully.")
    
    #Command with the general information of a shipgirl.
    @app_commands.command(name='shipgirl', description='Displays the shipgirl\'s information ')
    async def info(self, ctx: discord.Interaction, name: str):
        ship = AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name.replace(" ","_")}')
        view = Buttons(ship=ship)
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Fetched {name}\'s information at "{ctx.guild.name}/{ctx.channel.name}" for user "{ctx.user.name}/{ctx.user.id}"')
        embed = generateShipEmbed(ship=ship)
        await ctx.response.send_message(embed=embed,view=view)
        view.response = await ctx.original_response()
    
    #Command that displays the shipgirl's skins
    @app_commands.command(name='skins', description='Shows the given shipgirl\'s skills.')
    async def skins(self,ctx:discord.Interaction,name:str):
        ship = AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name.replace(" ","_")}')
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Fetched {name}\'s skins at "{ctx.guild.name}/{ctx.channel.name}" for user "{ctx.user.name}/{ctx.user.id}"')
        selectedSkin = ship.skins["skins"][0]
        skinEmbed = generateSkinEmbed(ship=ship,selectedSkin=selectedSkin)
        skinsView = skinsMenuView(ship=ship) 
        await ctx.response.send_message(embed=skinEmbed, view=skinsView)
        skinsView.response = await ctx.original_response()

    #Command to display the shipgirl's skills.
    @app_commands.command(name='skills',description='Shows the given shipgirl\'s skills')
    async def skills(self,ctx:discord.Interaction,name:str):
        ship=AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name.replace(" ","_")}')
        selectedSkill = ship.skills[0]
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Fetched {name}\'s skills at "{ctx.guild.name}/{ctx.channel.name}" for user "{ctx.user.name}/{ctx.user.id}"')
        skillsView = skillsMenuView(ship=ship)
        embed = generateSkillsEmbed(ship=ship,selectedSkill=selectedSkill)
        await ctx.response.send_message(embed=embed,view=skillsView)
        skillsView.response = await ctx.original_response()
        
    #Command that displays every artwork/loading screen in which this shipgirl appears.
    @app_commands.command(name='artworks',description='Show the given shipgirl\'s artworks shown on loading screens.')
    async def artworks(self,ctx:discord.Interaction, name:str):
        ship=AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name.replace(" ","_")}')
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Fetched {name}\'s artworks at "{ctx.guild.name}/{ctx.channel.name}" for user "{ctx.user.name}/{ctx.user.id}"')
        if ship.artworks != None:
            selectedArtwork = ship.artworks[0]
            artworksView = artworksMenuView(ship=ship)
            artworkEmbed = generateArtworksEmbed(ship=ship,selectedArtwork=selectedArtwork)
            await ctx.response.send_message(embed=artworkEmbed,view=artworksView)
            artworksView.response = await ctx.original_response()
        else:
            errorEmbed = discord.Embed(color=ship.color, description=f'The shipgirl {ship.name} has no available artworks to show.\nSearch for another shipgirl\'s artworks if you desire.')
            errorEmbed.set_author(name=ship.fullname, icon_url=ship.shipyard)
            errorEmbed.set_thumbnail(url=ship.chibi)
            errorEmbed.set_footer(text=f'{ship.name}\'s artworks')
            await ctx.response.send_message(embed=errorEmbed, ephemeral=True)



#Adds the commands class to the cog to be loaded.
async def setup(client):
    await client.add_cog(Commands(client))