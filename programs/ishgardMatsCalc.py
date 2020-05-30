from programs import ffxivToolsLib
from math import ceil


def main(targetLvl, skyLvl, rewardTier):
    # getMatsList(targetLvl, skyLvl, rewardTier)
    ffxivToolsLib.setup()
    jobInputs = ffxivToolsLib.getIshgardCraftingInputs()
    itemLocations = ffxivToolsLib.getItemLocationTable()
    totalItems = {}
    grindLocations = {}
    inclJobs = ['blacksmith', 'armorer']

    for x in jobInputs.items():
        print(x)
        if x[0] in inclJobs:
            addDicts(totalItems, getMatsList(targetLvl, skyLvl, rewardTier, x))
    if 'maple sap' in totalItems:
        totalItems['maple sap'] = ceil(totalItems['maple sap']/3)

    for k in totalItems:
        # print(k, totalItems[k])
        loc = itemLocations[k]
        z, a, n = loc.values()
        if z in grindLocations:
            if a in grindLocations[z]:
                grindLocations[z][a].append([totalItems[k], k, n])
            else:
                grindLocations[z][a] = [[totalItems[k], k, n]]
        else:
            grindLocations[z] = {a: [[totalItems[k], k, n]]}

    print(len(totalItems))
    for zone in grindLocations:
        if zone == 'diadem':
            print(zone)
            for node in grindLocations[zone]['diadem']:
                print("\t" + "{} {}, {}".format(*node))
        else:
            # print(zone, len(grindLocations[zone].keys()), grindLocations[zone])
            print(zone)
            for area in grindLocations[zone]:
                print("\t" + area)
                for node in grindLocations[zone][area]:
                    # print(node)
                    print("\t\t" + "{} {}, {}".format(*node))


def addDicts(updDict, withDict):
    for k in withDict:
        if k in updDict:
            updDict[k] += withDict[k]
        else:
            updDict[k] = withDict[k]


def getMatsList(targetLvl, skyLvl, rewardTier, jobInfo):
    xpTable = ffxivToolsLib.getXPTable()
    ingredients = ffxivToolsLib.getIngrTable()
    rewards = ffxivToolsLib.getRewardsTable()
    recipes = ffxivToolsLib.getRecipesTable()
    totalItems = {}

    jname,[jlvl, jxp] = jobInfo

    remXP = xpTable[targetLvl] - xpTable[jlvl] - jxp
    xpPerCraft, scripsPerCraft = rewards[skyLvl][rewardTier]
    totalCrafts = ceil(remXP/xpPerCraft)
    for recID in recipes[jname]:
        if ingredients[recID]['recipeLvl'] == skyLvl:
            for i in ingredients[recID]['ingrs']:
                n = i[0]*totalCrafts
                name = i[1]
                if name in totalItems:
                    totalItems[name] += n
                else:
                    totalItems[name] = n
    return totalItems


if __name__ == '__main__':
    tlvl = 75
    skyItemLevel = 60
    useTier = 't3'
    main(tlvl, skyItemLevel, useTier)
