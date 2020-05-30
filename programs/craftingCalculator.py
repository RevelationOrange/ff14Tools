from programs.ffxivToolsLib import craftItemManager, wikiURLbase, setup as ff14libSetup


def main():
    ff14libSetup()
    ciMngr = craftItemManager()
    arbInputList = []

    with open("..\\dbFiles\\arbitraryInput.txt") as arbInFile:
        for line in arbInFile:
            arbInputList.append(line.split("\n")[0])

    # ciMngr.setJobLevel('carpenter', 75)
    # ciMngr.setJobLevel('Blacksmith', 75)
    # ciMngr.setJobLevel('armorer', 75)
    # ciMngr.setJobLevel('goldsmith', 75)
    # ciMngr.setJobLevel('leatherworker', 75)
    # ciMngr.setJobLevel('weaver', 75)
    # ciMngr.setJobLevel('alchemist', 75)
    # ciMngr.setJobLevel('culinarian', 75)
    ciMngr.setAllJobLevels(75)

    #'''
    ciMngr.shopAdd('atrociraptorskin boots of crafting', 1)
    ciMngr.shopAdd('pixie cotton apron of crafting', 1)
    ciMngr.shopAdd('pixie cotton breeches of crafting', 1)
    ciMngr.shopAdd('pixie cotton hat of crafting', 1)
    ciMngr.shopAdd('pixie cotton sleeves of crafting', 1)
    #'''

    cim2 = craftItemManager(ciMngr)
    # print(cim2.inameDict)
    use = cim2
    z = cim2.findItemID('faded')
    fcSet = set()
    # for _ in z:
    #     print(cim2.inameDict[_])
    # arbInputList = ['effervescent water']
    # arbInputList = z[2:]
    # print(len(z), len(arbInputList))
    # checkAllRecs(cim2)
    # for x in (cim2.findItemID("effervescent water")):
    #     print(cim2.inameDict[x], x)
    do = True
    if do:
        for x in arbInputList:
            iid = cim2.idPicker(x)
            # iid = x
            rlist = cim2.findRecsByIngr(x, 50-1)
            # rlist = cim2.findRecsByIngr(iid, 50-1, True)
            print(x, len(rlist))
            for rid in rlist:
                fcSet.add(rid)
                rlvl = cim2.itemDict[rid].recLvl
                __cimtmp = craftItemManager(cim2)
                __cimtmp.shopAddByID(rid)
                sl = __cimtmp.getShoppingList()
                url = wikiURLbase.format(cim2.inameDict[rid].replace(" ", "_").replace("'", "%27"))
                # print(iid)
                if iid in sl:
                    nreq = sl[iid]['ct']
                else:
                    nreq = "intermediate item"
                ostr = "{:>2}, {:>1}, {}".format(rlvl, nreq, url)
                print(ostr)
    # cim2.findRecsByIngr("enchanted iron ink")
    # cim2.shopReset()
    do0 = False
    if do0:
        x = use.getShoppingList()
        delim = "|"
        for iid in x:
            if not ciMngr.shardTypeCheck[iid]:
                print("{},{},{},{}".format(ciMngr.inameDict[iid], x[iid]['ct'],
                                           delim.join([ciMngr.jobIDReverse[z] for z in x[iid]['jobs']]),
                                           delim.join([ciMngr.inameDict[z] for z in x[iid]['items']])))


def checkAllRecs(someCIM):
    print(len(someCIM.itemDict.keys()))
    outputfname = "recInvolvedStats.csv"
    with open(outputfname, 'w') as opf:
        opf.write("itemName,nRecs\n")
        for iid in someCIM.inameDict.keys():
            x = someCIM.findRecsByIngr(iid, 0, True)
            if len(x) > 0:
                print("{},{}".format(someCIM.inameDict[iid], len(x)))
                opf.write("{},{}\n".format(someCIM.inameDict[iid], len(x)))


if __name__ == '__main__':
    main()
