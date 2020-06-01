from os import sep
from math import ceil
import codecs
import csv


__dbFolderPath = sep.join(("..", "dbFiles"))
__xpTableFilePath = sep.join((__dbFolderPath, "EXPTable.csv"))
__ingrTableFilePath = sep.join((__dbFolderPath, "skyItemsIngredientsTable.csv"))
__rewardsTableFilePath = sep.join((__dbFolderPath, "rewardsTable.csv"))
__ishgardCraftingInputsFilePath = sep.join((__dbFolderPath, "jobsInput.csv"))
__itemLocationTableFilePath = sep.join((__dbFolderPath, "itemLocationTable.csv"))
__recipeLevelTableFilePath = sep.join((__dbFolderPath, "RecipeLevelTable.csv"))
__recipesFilePath = sep.join((__dbFolderPath, "Recipes.csv"))
__itemsFilePath = sep.join((__dbFolderPath, "Items.csv"))

wikiURLbase = "https://ffxiv.gamerescape.com/wiki/{}"
# print("{:>2} {}".format(self.itemDict[rid].recLvl, wikiURLbase.format(self.inameDict[rid].replace(" ", "_").replace("'", "%27"))))

__xpTable = {}
__ingrTable = {}
__rewardsTable = {}
__recipesTable = {}
__ishgardCraftingInputs = {}
__itemLocationTable = {}


def canIntConvert(x):
    try:
        int(x)
        return True
    except:
        return False


def repairQuotes(x):
    indices = []
    for i in range(len(x)):
        if x[i].count("\"")%2:
            indices.append(i)
    melds = [[indices[i*2], indices[i*2 + 1]] for i in range(int(len(indices)/2))]
    for pair in list(reversed(melds)):
        y = x.pop(pair[1])
        x[pair[0]] += "," + y
    return x


def addDicts(updDict, withDict):
    for k in withDict:
        if k in updDict:
            updDict[k] += withDict[k]
        else:
            updDict[k] = withDict[k]


def getXPTable():
    return __xpTable


def getIngrTable():
    return __ingrTable


def getRewardsTable():
    return __rewardsTable


def getRecipesTable():
    return __recipesTable


def getIshgardCraftingInputs():
    return __ishgardCraftingInputs


def getItemLocationTable():
    return __itemLocationTable


class craftItem:
    def __init__(self, i, ct, count, rlt):
        self.id = i
        # self.name = n
        self.ctype = ct
        self.output = count
        self.recLvl = rlt
        self.reqs = []

    def addIngr(self, i, q=1):
        self.reqs.append([q, i])
        return self

    def __str__(self):
        return "{}, {}, {}, {}".format(self.id, self.ctype, self.output, self.recLvl)


class craftItemManager:
    __allCIsDict = {}
    __allINameDict = {}
    __allShardTypeCheckDict = {}
    __isSetup = False

    def __init__(self, copyfrom=None):
        self.jobIDDict = {"carpenter": 0, "blacksmith": 1, "armorer": 2, "goldsmith": 3, "leatherworker": 4,
                          "weaver": 5, "alchemist": 6, "culinarian": 7}
        self.jobIDReverse = {v: k for k, v in self.jobIDDict.items()}
        self.shoppingList = {}
        self.inventory = {}
        if copyfrom:
            self.itemDict = copyfrom.itemDict.copy()
            self.inameDict = copyfrom.inameDict.copy()
            self.shardTypeCheck = copyfrom.shardTypeCheck.copy()
            self.jobLevels = copyfrom.jobLevels.copy()
        else:
            self.itemDict = craftItemManager.__allCIsDict.copy()
            self.inameDict = craftItemManager.__allINameDict.copy()
            self.shardTypeCheck = craftItemManager.__allShardTypeCheckDict.copy()
            self.jobLevels = dict.fromkeys(self.jobIDDict.values(), 0)

    def addItem(self, i):
        tmp = craftItem(i)
        self.itemDict[i] = tmp
        return tmp

    def addCI(self, ci):
        self.itemDict[ci.id] = ci

    def setJobLevel(self, j, l):
        self.jobLevels[self.jobIDDict[j.lower()]] = l

    def setAllJobLevels(self, l):
        for j in self.jobLevels:
            self.jobLevels[j] = l

    def getJobLevels(self):
        return self.jobLevels

    def getItemsList(self):
        return self.itemDict.keys()

    def calcMats(self, i, q=1):
        matsDict = {}
        reqs = self.itemDict[i].reqs
        for r in reqs:
            # print(r[1] in self.itemDict)
            if r[1] in self.itemDict and self.jobLevels[self.itemDict[r[1]].ctype] >= self.itemDict[r[1]].recLvl:
                # print(self.inameDict[r[1]], '\ttype:', self.itemDict[r[1]].ctype)
                # print(self.inameDict[i], self.itemDict[i].output, "({})".format(i))
                tmpMats = self.calcMats(r[1], ceil(r[0]*q/self.itemDict[r[1]].output))
                for k in tmpMats:
                    if k in matsDict:
                        matsDict[k] += tmpMats[k]
                    else:
                        matsDict[k] = tmpMats[k]
            else:
                if r[1] in matsDict:
                    matsDict[r[1]] += q*r[0]
                else:
                    matsDict[r[1]] = q*r[0]
        return matsDict

    def shopAddByID(self, i, q=1):
        if i in self.shoppingList:
            self.shoppingList[i] += q
        else:
            self.shoppingList[i] = q

    def idPicker(self, n):
        i = 0
        iids = self.findItemID(n)
        for iid in iids:
            if self.inameDict[iid].lower() == n.lower():
                i = iid
        if not i:
            z = 0
            print(n)
            for iid in iids:
                print("{}. {}".format(z, self.inameDict[iid]))
                z += 1
            c = input(">> ")
            i = iids[int(c)]
        return i

    def shopAdd(self, name, q=1):
        self.shopAddByID(self.idPicker(name), q)

    def shopReset(self):
        self.shoppingList = {}

    def getShoppingList(self):
        tmp = {}
        for i in self.shoppingList:
            # print(self.inameDict[i], self.itemDict[i].output)
            mats = self.calcMats(i, ceil(self.shoppingList[i]/self.itemDict[i].output))
            for k in mats:
                if k in tmp:
                    tmp[k]['ct'] += mats[k]
                    if self.itemDict[i].ctype not in tmp[k]['jobs']:
                        tmp[k]['jobs'].append(self.itemDict[i].ctype)
                    if self.itemDict[i].id not in tmp[k]['items']:
                        tmp[k]['items'].append(self.itemDict[i].id)
                else:
                    tmp[k] = {'ct': mats[k], 'jobs': [self.itemDict[i].ctype], 'items': [self.itemDict[i].id]}
        for k in tmp:
            if k in self.inventory:
                tmp[k]['ct'] = max(tmp[k]['ct'] - self.inventory[k], 0)
        return tmp

    def setInvy(self, invyDict):
        if type(invyDict) is dict:
            self.inventory = invyDict
        else:
            print("setInvy received a non-dict argument")

    def addToInvy(self, iname):
        pass

    def clearInvy(self):
        self.inventory = {}

    def findItemID(self, name):
        foundids = []
        for i in self.inameDict:
            if name.lower() in self.inameDict[i].lower():
                foundids.append(i)
        return foundids

    def findRecsByIngrOld(self, ingrName, overLvl=0, isID=False):
        if isID:
            ingrID = ingrName
        else:
            ingrID = self.idPicker(ingrName)

        ridSet = set()
        retRidSet = set()
        for rid in self.itemDict:
            for reqQ, reqID in self.itemDict[rid].reqs:
                if reqID == ingrID:
                    ridSet.add(rid)
                    ridSet = ridSet.union(self.findRecsByIngrOld(rid, 0, True))
        for rid in ridSet:
            if self.itemDict[rid].recLvl > overLvl:
                retRidSet.add(rid)
        return retRidSet

    def findRecsByIngr(self, ingrName, overLvl=0, isID=False):
        if isID:
            ingrID = ingrName
        else:
            ingrID = self.idPicker(ingrName)

        ridDict = {}
        retRidDict = {}
        for rid in self.itemDict:
            for reqQ, reqID in self.itemDict[rid].reqs:
                if reqID == ingrID:
                    addDicts(ridDict, {rid: reqQ})
                    addDicts(ridDict, self.findRecsByIngr(rid, 0, True))
        for rid in ridDict:
            if self.itemDict[rid].recLvl > overLvl:
                retRidDict[rid] = ridDict[rid]
        return retRidDict

    def setup(self, rltFilePath, recsFilePath, itemsFilePath):
        rltDict = {}

        with open(rltFilePath) as rltCSV:
            for _ in range(3): rltCSV.__next__()
            for line in rltCSV:
                z = line.split(',')
                rltDict[int(z[0])] = int(z[1])

        with open(recsFilePath) as recipeCSV:
            i = 0
            ingrOffset = 6
            indexlist = recipeCSV.__next__().split('\n')[0].split(',')
            colList = recipeCSV.__next__().split('\n')[0].split(',')
            # print(colList[4], colList[2], colList[3])
            typeList = recipeCSV.__next__().split('\n')[0].split(',')
            for line in recipeCSV:
                y = line.split(',')
                ci = craftItem(int(y[4]), int(y[2]), int(y[5]), rltDict[int(y[3])])
                for ind in range(10):
                    if int(y[ingrOffset + 1 + ind * 2]):
                        ci.addIngr(int(y[ingrOffset + ind * 2]), int(y[ingrOffset + 1 + ind * 2]))
                craftItemManager.__allCIsDict[ci.id] = ci

        with codecs.open(itemsFilePath, encoding='utf8') as itemCSV:
            x = itemCSV.__next__()
            y = itemCSV.__next__()
            z = itemCSV.__next__()
            prevData = ""
            for line in itemCSV:
                test = line.split(",")[0]
                if canIntConvert(test):
                    if prevData:
                        csvItem = csv.reader(prevData[:-1].splitlines(), quotechar='"', delimiter=',',
                                             quoting=csv.QUOTE_ALL, skipinitialspace=True)
                        item = [x for x in csvItem][0]
                        craftItemManager.__allShardTypeCheckDict[int(item[0])] = item[16] == '59'
                        craftItemManager.__allINameDict[int(item[0])] = item[10]
                    prevData = line
                else:
                    prevData += line

        craftItemManager.__isSetup = True


def setup():
    __protoCIM = craftItemManager()
    __protoCIM.setup(__recipeLevelTableFilePath, __recipesFilePath, __itemsFilePath)

    with open(__xpTableFilePath) as xpTableFile:
        xpTableFile.__next__()
        for line in xpTableFile:
            l = line[:-1].split(',')
            __xpTable[int(l[0])] = int(l[2])

    with open(__ingrTableFilePath) as ingrTableFile:
        ingrTableFile.__next__()
        for line in ingrTableFile:
            l = line[:-1].split(',')
            ingrCols = [x for x in l[4:] if x]
            ingrList = [y for y in zip(map(int, ingrCols[::2]), ingrCols[1::2])]
            __ingrTable[int(l[0])] = {'id': int(l[0]), 'name': l[1], 'recipeLvl': int(l[2]), 'job': l[3], 'ingrs': ingrList}
            if l[3] in __recipesTable:
                __recipesTable[l[3]].append(int(l[0]))
            else:
                __recipesTable[l[3]] = [int(l[0])]

    with open(__rewardsTableFilePath) as rewardsTableFile:
        rewardsTableFile.__next__()
        for line in rewardsTableFile:
            l = line[:-1].split(',')
            __rewardsTable[int(l[0])] = {'t{}'.format(x+1): [int(y), int(z)] for x, y, z in zip(range(3), l[1:][::2], l[1:][1::2])}

    with open(__ishgardCraftingInputsFilePath) as ishgardInputsFile:
        ishgardInputsFile.__next__()
        for line in ishgardInputsFile:
            l = line[:-1].split(',')
            __ishgardCraftingInputs[l[0]] = [x for x in map(int, l[1:])]

    with open(__itemLocationTableFilePath) as itemLocationTableFile:
        itemLocationTableFile.__next__()
        for line in itemLocationTableFile:
            l = line[:-1].split(',')
            __itemLocationTable[l[0]] = {'zone': l[1], 'area': l[2], 'node': l[3]}
