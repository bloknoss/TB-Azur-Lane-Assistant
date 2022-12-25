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
            self.shipyard = self.getShipyardIcon()
            self.image = self.getImage()
            self.skins = self.getSkins()
            self.drops = self.getDrops()
            self.skills = self.getSkills()
            self.tier = self.getTier()
            self.color = self.getColor()
        except Exception as e:
            print(e.with_traceback())

    def getScrappedDoc(self):
        resp = requests.get(self.URL).text
        doc = BeautifulSoup(resp, "html.parser")
        return doc

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

    def getShipyardIcon(self):
        return self.main.find('img')['src']

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
        self.chibi = mainWindow[0].find('img', alt='Chibi')['src']

        for skin in mainWindow:
            image = skin.find('div', class_='shipskin-image').find('img')
            if image != None:
                name = skin['data-title']
                chibi = skin.find('img', alt='Chibi')['src']
                link = self.fixSource(src=image['srcset'].strip())
                info_table = skin.find("table", class_='wikitable shipskin-table').find('tbody').find_all('tr')
                skin_info = []

                for tr in info_table:
                    tds = tr.find_all("td")
                    if len(tds) > 1:
                        skin_info.append({"category":tr.find('th').text.strip(),"value":tr.find('td').text.strip()})
                        skin_info.append({"category":"Availability","value":tr.find_all('td')[1].text.strip()})        
                    else:                      
                        skin_info.append({"category":tr.find('th').text.strip(),"value":tr.find('td').text.strip()})

                skinsDict["skins"].append(
                    {"name": name, "url": link, "chibi": chibi,"info":skin_info})

        return skinsDict

    def getImage(self):
        return self.fixSource(self.main.find('div', class_='azl_box_body').find("img")['srcset'])

    def getSkills(self):
        skillsDict =  []
        skillsTable = self.main.find('table', class_='ship-skills wikitable')
        skillsElements = skillsTable.find_all('tr')[1:]
        for skill in skillsElements:
            if skill.find('b') != None:
                name = skill.find_all('td')[1].find('b').text.strip()
                description = skill.find_all('td')[2].text.strip()
                color = self.getSkillColor(skill.find('td')['style'])
                link = self.fixSource(skill.find('img')['srcset'])
                skillsDict.append(
                    {"name": name, "description": description, "image": link,"color":color})

        return skillsDict

    def getDrops(self):
        maps = {"maps": [], "notes": []}
        construct_table = self.main.find(
            'table', class_='ship-construction wikitable')
        if construct_table != None:
            rows = construct_table.find_all("tr")[1:5]
            dropNotes = construct_table.find_all(
                "tr")[-1] if len(construct_table.find_all("tr")) > 5 else None
            for i in range(len(rows)):
                cols = rows[i].find_all('td', colspan=None, rowspan=None)
                for j in range(len(cols)):
                    colValue = cols[j].text.strip()
                    if colValue != '-':
                        maps["maps"].append(f'{j+1}-{i+1}')

            if dropNotes != None:
                [maps['notes'].append(note.text.strip())
                 for note in dropNotes.find_all('td')]

        return maps

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

    def getSkillColor(self,color:str):
        if 'Pink' in color:
            return 0xfa2953
        elif 'Gold' in color:
            return 0xffd900
        elif 'DeepSkyBlue' in color:
            return 0x85ceea
    
    def fixSource(self, src):
        splitted = src.split(' ')
        splitted = splitted[len(splitted)-2].replace('thumb/', '')
        fullRes = splitted.split('/')[:-1]
        return '/'.join(fullRes) if 'px-' in splitted else splitted
