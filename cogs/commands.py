import discord
from TB import AzurLaneTB
from discord import app_commands
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands have been loaded succesfully")

    @app_commands.command(name='info', description='Retrieve the ship\'s information from the database.',)
    async def info(self, ctx: discord.Interaction, name: str):
        ship = AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name}')
        embed = discord.Embed(title=ship.fullname, color=ship.color)
        embed.set_footer(text="Sources:\nAzur Lane English Wiki\nAzur Lane's EN Community Tier List")
        for cat in ship.info['categories']:
            if cat["category"] != 'Full Name' and cat["category"] != "Image":
                embed.add_field(name=cat["category"], value="`" + cat["value"] + "`",inline=False)
        embed.add_field(name="Ranking",value="`"+ ship.tier["rank"] + "`",inline=False)
        if ship.tier["notes"] != []:
            notes = ''
            for note in ship.tier["notes"]:
                notes += f"`{note}`\n"
            embed.add_field(name="Ranking Notes", value=notes.strip(), inline=False)
            
        await ctx.response.send_message("holaaaa", embed=embed)


async def setup(client):
    await client.add_cog(Commands(client))