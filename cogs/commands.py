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
    async def test(self, ctx: discord.Interaction, name: str):
        ship = AzurLaneTB(f'https://azurlane.koumakan.jp/wiki/{name}')
        embed = discord.Embed(title=ship.fullname)
        embed.set_image(url=ship.image)
        for cat in ship.info['categories']:
            if cat["category"] != 'Full Name' and cat["category"] != "Image":
                embed.add_field(name=cat["category"], value=cat["value"],inline=False)
                
        await ctx.response.send_message("holaaaa", embed=embed)


async def setup(client):
    await client.add_cog(Commands(client))