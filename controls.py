import discord
from tb import AzurLaneTB as TB
from datetime import datetime
from utilities import generateSkinEmbed, generateSkillsEmbed, generateArtworksEmbed
from discord.ext import commands
from utilities import bcolors

# Defined view classes up here, uses the view components below to display them in the discord message.
class skinsMenuView(discord.ui.View):
    def __init__(self, *, timeout=180, ship: TB, destroy: bool = False):
        super().__init__(timeout=timeout)
        self.destroy = destroy
        self.response = None
        self.add_item(skinsMenu(ship=ship))

    async def on_timeout(self):
        if self.destroy == True:
            await self.response.delete()
        else:
            await self.response.edit(view=None)

        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Timed out menu interaction. ')


class skillsMenuView(discord.ui.View):
    def __init__(self, *, timeout=180, ship: TB, destroy: bool = False):
        super().__init__(timeout=timeout)
        self.response = None
        self.destroy = destroy
        self.add_item(skillsMenu(ship=ship))

    async def on_timeout(self):
        if self.destroy == True:
            await self.response.delete()
        else:
            await self.response.edit(view=None)
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Timed out menu interaction. ')
        
        
class artworksMenuView(discord.ui.View):
    def __init__(self, *, timeout=180, ship: TB, destroy: bool = False):
        super().__init__(timeout=timeout)
        self.response = None
        self.destroy = destroy
        self.add_item(artworksMenu(ship=ship))

    async def on_timeout(self):
        if self.destroy == True:
            await self.response.delete()
        else:
            await self.response.edit(view=None)

        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f'{bcolors.OKGREEN}[{time_now}] Timed out menu interaction. ')

# Here are the menu components defined, these are the ones that appear in the discord message
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

class artworksMenu(discord.ui.Select):
    def __init__(self, ship: TB):
        super().__init__()
        self.ship = ship
        self.artworks = self.ship.artworks
        options = [discord.SelectOption(
            label=self.artworks[i]["artwork"][:100], value=i) for i in range(len(self.artworks))]
        super().__init__(placeholder="Select an option",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selectedArtwork = self.artworks[int(self.values[0])]
        artworkEmbed = generateArtworksEmbed(self.ship,selectedArtwork=selectedArtwork)
        await interaction.response.edit_message(embed=artworkEmbed)

# This is the view with also the buttons in them.
class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180, ship: TB):
        super().__init__(timeout=timeout)
        self.ship = ship
        self.response = discord.InteractionMessage

    #Timeout, when the set timeout passes it'll disable the view.
    async def on_timeout(self):
        time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        await self.response.edit(view=None)
        print(f'{bcolors.OKGREEN}[{time_now}] Timed out button interaction. ')

    #Skins button
    @discord.ui.button(label='Skins', style=discord.ButtonStyle.red)
    async def skinsButton(self, interaction: discord.Interaction, button: discord.ui.Button,):
        skinsView = skinsMenuView(timeout=60, ship=self.ship, destroy=True)
        selectedSkin = self.ship.skins["skins"][0]
        await interaction.response.send_message(embed=generateSkinEmbed(ship=self.ship, selectedSkin=selectedSkin), view=skinsView)
        skinsView.response = await interaction.original_response()

    #Skills button
    @discord.ui.button(label='Skills', style=discord.ButtonStyle.red)
    async def skillsButton(self, interaction: discord.Interaction, button: discord.ui.Button,):
        skillsView = skillsMenuView(timeout=60, ship=self.ship, destroy=True)
        selectedSkill = self.ship.skills[0]
        await interaction.response.send_message(embed=generateSkillsEmbed(ship=self.ship, selectedSkill=selectedSkill), view=skillsView)
        skillsView.response = await interaction.original_response()
        
    #Artworks button
    @discord.ui.button(label='Artworks', style=discord.ButtonStyle.red)
    async def artworksButton(self, interaction: discord.Interaction, button: discord.ui.Button,):
        if self.ship.artworks != None:
            selectedArtwork = self.ship.artworks[0]
            artworksView = artworksMenuView(ship=self.ship,timeout=60,destroy=True)
            artworkEmbed = generateArtworksEmbed(ship=self.ship,selectedArtwork=selectedArtwork)
            await interaction.response.send_message(embed=artworkEmbed,view=artworksView)
            artworksView.response = await interaction.original_response()
        else:
            errorEmbed = discord.Embed(color=self.ship.color, description=f'The shipgirl {self.ship.name} has no available artworks to show.\nSearch for another shipgirl\'s artworks if you desire.')
            errorEmbed.set_author(name=self.ship.fullname, icon_url=self.ship.shipyard)
            errorEmbed.set_thumbnail(url=self.ship.chibi)
            errorEmbed.set_footer(text=f'{self.ship.name}\'s artworks')
            await interaction.response.send_message(embed=errorEmbed, ephemeral=True)
