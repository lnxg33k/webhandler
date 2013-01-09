import math, sys



class Tablize(object):

    def __init__(self, l, sql):
        self.dataList = l
        if len(l[0].keys()) == 1:
            self.columns = 1
            self.title = l[0].keys()[0]
            tmpList = []
            for i in self.dataList:
                tmpList.append(i.values()[0])
            self.tup = tuple(tmpList)
        else:
            self.columns = 2
            self.title = sql
            tmpHeader = []
            for i in l[0].keys():
                tmpHeader.append(i)
            self.headerTup = tuple(tmpHeader)
            tmpList = []
            for i in l:
                tmpT = []
                for j in i.values():
                    tmpT.append(j)
                tmpList.append(tuple(tmpT))
                self.tup = tuple(tmpList)
        self.lengths = {}
        if self.columns == 2:
            for i in self.tup:
                for j in range(len(i)):
                    try:
                        if(self.lengths[j] < len(i[j])):
                            self.lengths[j] = len(i[j])
                    except:
                        self.lengths[j] = len(i[j])
        else:
            for i in range(len(self.tup)):
                self.lengths[i] = len(self.tup[i])

    def hr(self):
        print "+",
        if self.columns == 1:
            if len(self.title) > max(self.lengths.values()):
                maxx = len(self.title)
            else:
                maxx = max(self.lengths.values())
            for i in range(maxx+2):
                sys.stdout.write("-")

        else:
            for i in range(sum(self.lengths.values())+(3*len(self.lengths))-1):
                sys.stdout.write("-")
        print "+"


    def tablize(self, data):

        if(type(data) == str):
            self.hr()
            print "|", self.centerize(data, sum(self.lengths.values()) + len(self.lengths.values()) + 1),
            print "|"
            self.hr()
        else:
            if self.columns == 1:
                self.hr()
                if len(self.title) > max(self.lengths.values()):
                    maxx = len(self.title)
                else:
                    maxx = max(self.lengths.values())
                for row in data:
                    print "|", self.centerize(row, maxx),
                    print "|"
                self.hr()
            else:
                self.hr()
                for row in data:
                    for n in range(len(row)):
                        print "|", self.centerize(row[n], self.lengths[n]),
                    print "|"
                self.hr()

    def centerize(self, word, count):
        try:
            diff = count - len(word)
        except TypeError:
            diff = count - 4
        half = int(math.floor(diff / float(2)))
        op = ""
        for i in range(half):
            op += " "
        op += str(word)
        for i in range(half):
            op += " "
        if len(op) < count:
            op += " "
        return op



