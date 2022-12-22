from bs4 import BeautifulSoup
import json
import sys
import requests


class AzurLaneTB:
    def __init__(self, shipURL) -> None:
        self.URL = shipURL
        self.main = self.getScrappedInfo()
        self.skins = self.getShipSkins()
        self.skills = self.getSkills()

    def getScrappedInfo(self):
        resp = requests.get(self.URL).text
        doc = BeautifulSoup(resp, "html.parser")
        return doc

    def getShipSkins(self):
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
                skinsDict["skins"].append({"name": name , "url": link})
                # print(self.fixSource(src=skin.find('div', class_='shipskin-image').find('img')['srcset'].strip())+'\n')

        return skinsDict

    def getInfo(self):
        mainCard = self.main.find('div', class_='ship-card-content')
        shipFullName = mainCard.find(
            'div', class_='card-headline').find('span').text
        mainCardInfo = mainCard.find('div', class_='card-info').find('tbody')
        infoTRs = mainCardInfo.find_all('tr')

        for info in infoTRs[0:5]:
            children = info.findChildren()
            print(f'Category {children[0].text.strip()}')
            print(children[-1].text.strip() + '\n')

        return 'Done'

    def getSkills(self):
        skillsTable = self.main.find('table', class_='ship-skills wikitable')
        skillsTR = skillsTable.find_all('tr')[1:]
        for skill in skillsTR:
            if skill.find('b') != None:
                print(self.fixSource(skill.find('img')['srcset']))
                print(skill.find_all('td')[1].find('b').text)
                print(skill.find_all('td')[2].text.strip() + '\n')

    def fixSource(self, src):
        splitted = src.split(' ')
        splitted = splitted[len(splitted)-2].replace('thumb/', '')
        fullRes = splitted.split('/')[:-1]
        return '/'.join(fullRes) if 'px-' in splitted else splitted


# Main function
if __name__ == '__main__':
    # scrappedDoc = getScrappedInfo(sys.argv[1])
    input = sys.argv[1]
    tb = AzurLaneTB(shipURL=input)
    print(json.dumps(tb.skins,indent=4))
