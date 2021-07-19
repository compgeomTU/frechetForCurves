import math
from decimal import Decimal

class BinarySearch:

    dis = None
    l = None
    r = None
    m = None
    prsn = 10

    def __init__(self, distance):
        if type(distance).__name__ == "StrongDistance" or \
            type(distance).__name__ == "WeakDistance":
            self.dis = distance
        else:
            raise TypeError(type(distance).__name__)

    def setBoundaries(self, left, right):
        self.l = left
        self.r = right

    def setPercision(self, precision):
        self.prsn = Decimal(str(precision)).as_tuple().exponent

    def search(self):

        def verticelength(c, n):
            l = 0
            for i in range(n-1):
                l += math.dist([c[i].x, c[i].y], [c[i+1].x, c[i+1].y])
            return l

        #Check if boundieries have been set. if not will take maximum
        #distance across free space diagram
        if self.l == None or self.r == None:
            vl = verticelength(self.dis.getverticalcurve(), \
                self.dis.getverticaledges())
            hl = verticelength(self.dis.gethorizontalcurve(),\
                self.dis.gethorizontaledges())
            self.l = 0
            self.r = int(math.dist([hl, 0], [0, vl]))

            print("Configued starting boundieries as:")
            print(f"    | {self.l} --- {self.r} |\n")

        self.m = (self.l + self.r) / 2
        self.dis.setfreespace(self.m)

        print(f"Checking if epsilon is reachable:")
        print(f"    | {self.l} -- {self.m} -- {self.r} |")

        #check if path can be found
        if self.dis.isreachable():
            #check if mid value is percise enough to exit recurssion
            if Decimal(str(self.m)).as_tuple().exponent >= self.prsn:
                print(f"    Eps {self.m}: <reachable>\n")
                self.r = self.m
                return self.search()
            else:
                print(f"    Eps {self.m}: <reachable> <meets percision>\n")
                return self.m
        else:
            print(f"    Eps {self.m}: <unreachable>\n")
            self.l = self.m
            return self.search()
