from AzurLane import *

if __name__ == '__main__':
    userInput = sys.argv[1]
    localDB = AzurLaneTB(userInput)
    print(localDB.name + '\n')
    print(json.dumps(localDB.info, indent=4))
    print(json.dumps(localDB.skills, indent=4))
    print(json.dumps(localDB.skins, indent=4))
