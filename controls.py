import discord
from TB import AzurLaneTB as TB
from datetime import datetime
from utilities import generateSkinEmbed, generateSkillsEmbed
from discord.ext import commands
from utilities import bcolors


class skinsMenu(discord.ui.Select):
    def __init__(self, ship: TB):
        super().__init__()
        self.ship = ship
        self.skins = self.ship.skins["skins"]
        options = [discord.SelectOption(
            label=self.skins[i]["name"], value=i) for i in range(len(self.skins))]
        super().__init__(placeholder="Select an option",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selectedSkin = self.skins[int(self.values[0])]
        skinEmbed = generateSkinEmbed(
            ship=self.ship, selectedSkin=selectedSkin)
        await interaction.response.edit_message(embed=skinEmbed)


class skinsMenuView(discord.ui.View):
    def __init__(self, *, timeout=180, ship):
        super().__init__(timeout=timeout)
        self.response = None
        self.add_item(skinsMenu(ship=ship))

    async def on_timeout(self):
        await self.response.edit(view=None)
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Timed out menu interaction. ')


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180, ship):
        super().__init__(timeout=timeout)
        self.ship = ship
        self.response = discord.InteractionMessage
        
    async def on_timeout(self):
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        await self.response.edit(view=None)
        print(f'{bcolors.OKGREEN}[{time_now}] Timed out button interaction. ')
        
    @discord.ui.button(label='Skins', style=discord.ButtonStyle.red)
    async def skillsButton(self, interaction : discord.Interaction, button:discord.ui.Button,):
        skinsView = skinsMenuView(ship=self.ship)
        selectedSkin = self.ship.skins["skins"][0]
        await interaction.response.send_message(embed=generateSkinEmbed(ship=self.ship, selectedSkin=selectedSkin), view=skinsView)
        skinsView.response = await interaction.original_response()

class skillsMenu(discord.ui.Select):
    def __init__(self, ship: TB):
        super().__init__()
        self.ship = ship
        self.skills = self.ship.skills
        options = [discord.SelectOption(
            label=self.skills[i]["name"], value=i) for i in range(len(self.skills))]
        super().__init__(placeholder="Select an option",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selectedSkill = self.skills[int(self.values[0])]
        skillEmbed = generateSkillsEmbed(
            ship=self.ship, selectedSkill=selectedSkill)
        await interaction.response.edit_message(embed=skillEmbed)


class skillsMenuView(discord.ui.View):
    def __init__(self, *, timeout=180, ship):
        super().__init__(timeout=timeout)
        self.response = None
        self.add_item(skillsMenu(ship=ship))

    async def on_timeout(self):
        await self.response.edit(view=None)
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Timed out menu interaction. ')
