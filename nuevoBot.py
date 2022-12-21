from bs4 import BeautifulSoup
import sys
import requests

def getScrappedInfo(shipURL):
    resp = requests.get(shipURL).text
    doc = BeautifulSoup(resp, "html.parser")
    return doc

def getShipSkins(shipURL):

    resp = requests.get(f'{shipURL}/Gallery').text
    doc = BeautifulSoup(resp, "html.parser")
    mainWindow = doc.find('section', class_='tabber__section').find_all(recursive=False)
    [print(skin['data-title']) for skin in mainWindow]
        #print(skin.find('div', class_='shipskin'))
    for skin in mainWindow:
        print(parseSRCSET(skin.find('div', class_='shipskin-image').find('img')['srcset']))

def parseSRCSET(srcset):
    splitted = srcset.split(' ')
    splitted =splitted[len(splitted)-2].replace('thumb/','')
    fullRes = splitted.split('/')[:-1]
    return '/'.join(fullRes)  if 'px-' in splitted else splitted
    
def getShipInfo(shipDoc):
    mainCard = shipDoc.find('div', class_='ship-card-content')
    shipFullName = mainCard.find('div', class_='card-headline').find('span').text
    mainCardInfo = mainCard.find('div', class_='card-info').find('tbody')
    infoTRs = mainCardInfo.find_all('tr')
    skillsTable = shipDoc.find('table',class_='ship-skills wikitable')
    skillsTR = skillsTable.find_all('tr')[1:]

    for info in infoTRs[0:5]:
        children = info.findChildren()
        print(f'Category {children[0].text.strip()}')
        print(children[-1].text.strip())
    
    print('Category Skills')
    for skill in skillsTR:
        if skill.find('b') != None:
            print(skill.find_all('td')[1].find('b').text)
            print(skill.find_all('td')[2].text)

    
    return 'Done' 



#Main function
if __name__ == '__main__':
    #scrappedDoc = getScrappedInfo(sys.argv[1])
    getShipSkins(sys.argv[1])