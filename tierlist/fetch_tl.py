import json
from requests_html import HTMLSession
import sys
from bs4 import BeautifulSoup


class tlDatabase:
    def __init__(self) -> None:
        self.shipClassifications = [
            "bb", "cv", "ca", "cl", "dd", "ss", "other"]
        self.tierList = {"BB": [], "CV": [], "CA": [],
                         "CL": [], "DD": [], "SS": [], "OTHER": []}

    def update_localdb(self):
        print("Updating local database from https://slaimuda.github.io/ectl/#/home.\nThis could take up to a few minutes.\n")
        for classif in self.shipClassifications:
            session = HTMLSession()

            resp = session.get(
                f'https://slaimuda.github.io/ectl/#/main/{classif}')
            resp.html.render()
            soup = BeautifulSoup(resp.html.html, 'html.parser')

            tiers = soup.find(
                'div', class_='tab-pane active').find_all('div', class_=None)
            for tier in tiers:
                if tier.find('h3') != None:
                    ships = tier.find_all('div', class_='col-4')
                    rank = tier.find('h3').text.strip()
                    currentRank = {"ships": []}
                    for ship in ships:
                        additionalNotes = ship.find_all('img', class_=None)
                        name = ship.text
                        if additionalNotes != None:
                            additionalNotes = [
                                additionalNote["data-tip"].strip() for additionalNote in additionalNotes]
                        else:
                            additionalNotes = None

                        currentRank["ships"].append(
                            {"name": name, "notes": additionalNotes})
                    self.tierList[classif.upper()].append({rank: currentRank})
                    print(
                        f"Tier for {classif.upper()}'s {rank} fetched succesfully.")
            print("")

        self.save()

    def save(self):
        with open("tierList.json", "w") as fp:
            json.dump(self.tierList, fp, indent=4)
        print("\nUpdating has finished succesfully.\nSaved on tierList.json")


class infoRetrieval():
    def __init__(self, ship: str, db:str):
        self.name = ship
        f = open(db)
        self.tl = json.load(f)
        f.close()
        self.shipClassifications = [
            "bb", "cv", "ca", "cl", "dd", "ss", "other"]

    def getTier(self):
        for classif in self.shipClassifications:
            tierAmount = len(self.tl[classif.upper()])
            for i in range(tierAmount):
                for tier in self.tl[classif.upper()][i]:
                    for ship in self.tl[classif.upper()][i][tier]["ships"]:
                        if ship["name"] == self.name:
                            return {"rank": tier, "notes": ship["notes"]}


