import codecs


with codecs.open("..\\dbFiles\\ItemFood.csv", encoding='utf8') as foodItemCSV:
    print(foodItemCSV.__next__()[:-1])
    print(foodItemCSV.__next__()[:-1])
    print(foodItemCSV.__next__()[:-1])
    print(foodItemCSV.__next__()[:-1])
    print(foodItemCSV.__next__()[:-1])
