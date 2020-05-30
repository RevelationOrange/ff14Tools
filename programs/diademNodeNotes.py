

class Node:
    def __init__(self, contents, designation, n=-1):
        self.contents = contents
        self.designation = designation
        self.n = n

    def setSpot(self, n):
        self.n = n


class Diadem:
    def __init__(self):
        self.btnRedNodeList = []
        self.btnBlueNodeList = []
        self.minRedNodeList = []
        self.minBlueNodeList = []

    def addNode(self, n, nType, nColor):
        if nType == 'min':
            if nColor == 'r':
                n.setSpot(len(self.minRedNodeList))
                self.minRedNodeList.append(n)
            elif nColor == 'b':
                n.setSpot(len(self.minBlueNodeList))
                self.minBlueNodeList.append(n)
            else:
                print('wrong node color')
        elif nType == 'btn':
            if nColor == 'r':
                n.setSpot(len(self.btnRedNodeList))
                self.btnRedNodeList.append(n)
            elif nColor == 'b':
                n.setSpot(len(self.btnBlueNodeList))
                self.btnBlueNodeList.append(n)
            else:
                print('wrong node color')
        else:
            print('wrong node type')


def main():
    x = 1
    D = Diadem()
    D.addNode(Node({x: 'beehive', 0: 'maple sap', 2: 'feather', 3: 'resin', 4: 'hardened sap'}, 'c', 0), 'btn', 'r')
    D.addNode(Node({x: 'beehive'}, 'r'), 'btn', 'r')


if __name__ == '__main__':
    main()
