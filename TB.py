from bs4 import BeautifulSoup
from tierlist.fetch_tl import infoRetrieval
import requests


class AzurLaneTB:
    def __init__(self, shipURL) -> None:
        try:
            self.URL = shipURL
            self.main = self.getScrappedDoc()
            self.name = self.getName()
            self.fullname = self.getFullname()
            self.info = self.getInfo()
            self.image = self.getImage()
            self.skins = self.getSkins()
            self.skills = self.getSkills()
            self.tier = self.getTier()
            self.color = self.getColor()
        except Exception as e:
            print(e.with_traceback())

    def getScrappedDoc(self):
        resp = requests.get(self.URL).text
        doc = BeautifulSoup(resp, "html.parser")
        return doc

    def getTier(self):
        tlInfo = infoRetrieval(self.name, "./tierlist/tierList.json")
        return tlInfo.getTier()

    def getName(self):
        return self.main.find('span', class_='mw-page-title-main').text.strip()

    def getFullname(self):
        return self.main.find('div', class_='ship-card-content').find(
            'div', class_='card-headline').find('span').text.strip()

    def getSkins(self):
        skinsDict = {"skins": []}
        resp = requests.get(f'{self.URL}/Gallery').text
        doc = BeautifulSoup(resp, "html.parser")
        mainWindow = doc.find(
            'section', class_='tabber__section').find_all(recursive=False)
        for skin in mainWindow:
            image = skin.find('div', class_='shipskin-image').find('img')
            if image != None:
                name = skin['data-title']
                link = self.fixSource(src=image['srcset'].strip())
                skinsDict["skins"].append({"name": name, "url": link})

        return skinsDict

    def getImage(self):
        return self.fixSource(self.main.find('div', class_='azl_box_body').find("img")['srcset'])

    def getInfo(self):
        infoDict = {"categories": []}
        mainCard = self.main.find('div', class_='ship-card-content')
        fullName = mainCard.find(
            'div', class_='card-headline').find('span').text
        image = self.fixSource(self.main.find(
            'div', class_='azl_box_body').find("img")['srcset'])
        retrofit = self.main.find(text='Retrofit') != None

        infoDict['categories'].append(
            {"category": "Full Name", "value": fullName})
        infoDict['categories'].append({"category": "Image", "value": image})
        infoDict['categories'].append(
            {"category": "Retrofit", "value": "Available" if retrofit == True else "Unavailable"})
        mainCardInfo = mainCard.find('div', class_='card-info').find('tbody')
        infoElements = mainCardInfo.find_all('tr')

        for info in infoElements[0:5]:
            children = info.findChildren()
            catName = children[0].text.strip()
            catValue = children[-1].text.strip()
            if catName == 'Rarity':
                catValue = catValue.replace('★', '').strip()
                self.rarity = catValue
            infoDict['categories'].append(
                {'category': catName, "value": catValue})

        return infoDict

    def getSkills(self):
        skillsDict = {"skills": []}
        skillsTable = self.main.find('table', class_='ship-skills wikitable')
        skillsElements = skillsTable.find_all('tr')[1:]
        for skill in skillsElements:
            if skill.find('b') != None:
                name = skill.find_all('td')[1].find('b').text.strip()
                description = skill.find_all('td')[2].text.strip()
                link = self.fixSource(skill.find('img')['srcset'])
                skillsDict['skills'].append(
                    {"name": name, "description": description, "image": link})

        return skillsDict

    def getColor(self):
        if self.rarity == "Ultra Rare" or self.rarity == "Decisive":
            return 0xe92063
        elif self.rarity == "Super Rare" or self.rarity == "Priority":
            return 0xffd900
        elif self.rarity == "Elite":
            return 0x800080
        elif self.rarity == "Rare":
            return 0x0000ff
        elif self.rarity == "Common":
            return 0x808080

    def fixSource(self, src):
        splitted = src.split(' ')
        splitted = splitted[len(splitted)-2].replace('thumb/', '')
        fullRes = splitted.split('/')[:-1]
        return '/'.join(fullRes) if 'px-' in splitted else splitted
