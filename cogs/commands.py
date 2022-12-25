import discord
import json
from TB import AzurLaneTB
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from controls import skinsMenuView, Buttons,skillsMenuView
from utilities import bcolors, generateSkinEmbed, generateSkillsEmbed

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f"{bcolors.OKBLUE}[{time_now}] The commands module has loaded succesfully.")
    
    @app_commands.command(name='shipgirl', description='Retrieve the ship\'s information from the database.')
    async def info(self, ctx: discord.Interaction, name: str):
        ship = AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name.replace(" ","_")}')
        view = Buttons(ship=ship)
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Fetched {name}\'s information at "{ctx.guild.name}/{ctx.channel.name}" for user "{ctx.user.name}/{ctx.user.id}"')
        embed = discord.Embed(color=ship.color)
        embed.set_author(name=ship.fullname, icon_url=ship.shipyard)
        embed.set_thumbnail(url=ship.chibi)
        embed.set_footer(
            text="Sources:\nAzur Lane English Wiki\nAzur Lane's EN Community Tier List")
        for cat in ship.info['categories']:
            if cat["category"] != 'Full Name' and cat["category"] != "Image":
                embed.add_field(
                    name=cat["category"], value="`" + cat["value"] + "`", inline=False)
        if  ship.drops != None and ship.drops["maps"] != []:
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

        await ctx.response.send_message(embed=embed,view=view)
        view.response = await ctx.original_response()
    
    
    @app_commands.command(name='skins', description='Retrieve the ship\'s information from the database.')
    async def skins(self,ctx:discord.Interaction,name:str):
        ship = AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name.replace(" ","_")}')
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Fetched {name}\'s skins at "{ctx.guild.name}/{ctx.channel.name}" for user "{ctx.user.name}/{ctx.user.id}"')
        selectedSkin = ship.skins["skins"][0]
        skinEmbed = generateSkinEmbed(ship=ship,selectedSkin=selectedSkin)
        skinsView = skinsMenuView(ship=ship) 
        await ctx.response.send_message(embed=skinEmbed, view=skinsView)
        skinsView.response = await ctx.original_response()

    @app_commands.command(name='skills',description='Retrieve the ship\'s skills from the database.')
    async def skills(self,ctx:discord.Interaction,name:str):
        ship=AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name.replace(" ","_")}')
        selectedSkill = ship.skills[0]
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Fetched {name}\'s skills at "{ctx.guild.name}/{ctx.channel.name}" for user "{ctx.user.name}/{ctx.user.id}"')
        skillsView = skillsMenuView(ship=ship)
        embed = generateSkillsEmbed(ship=ship,selectedSkill=selectedSkill)
        await ctx.response.send_message(embed=embed,view=skillsView)
        skillsView.response = await ctx.original_response()
        
async def setup(client):
    await client.add_cog(Commands(client))






