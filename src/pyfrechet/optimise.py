import math
from decimal import Decimal
from distance import Distance

class BinarySearch:

    __l: float
    __r: float
    __m: float
    __p: float

    def __init__(self, distance):
        if isinstance(distance, Distance):
            self.__dis = distance
            self.__l = -1
            self.__r = -1
            self.__p = -1
        else:
            raise TypeError(f"{distance.__class__.__name__} is not a valid argument."
                            f"Must be of type StrongDistance or WeakDistance."
                            )

    @staticmethod
    def __vertexLength(c, n):
        l = 0
        for i in range(n-1):
            l += math.dist([c[i].x, c[i].y], [c[i+1].x, c[i+1].y])
        return l

    @staticmethod
    def __percision(p):
        return Decimal(str(p)).as_tuple().exponent

    def setBoundaries(self, left, right):
        self.__l = left
        self.__r = right

    def setPercision(self, precision):
        self.__p = self.__percision(precision)

    def search(self):
        #Check if boundieries have been set. if not will take maximum
        #distance across free space diagram
        if self.__l == -1 and self.__r == -1:
            l1 = self.__vertexLength(self.__dis.getCurve2(), \
                self.__dis.getCurve2Lenght())
            l2 = self.__vertexLength(self.__dis.getCurve1(),\
                self.__dis.getCurve1Lenght())
            self.__l = 0
            self.__r = int(math.dist([l2, 0], [0, l1]))
            print("Inital boundieries set:")
            print(f"    | {self.__l} --- {self.__r} |")

        if self.__p == -1:
            self.__p = -8
            print(f"    precision = {self.__p}\n")

        self.__m = (self.__l + self.__r) / 2
        self.__dis.setFreeSpace(self.__m)

        print(f"Checking if epsilon is reachable:")
        print(f"    | {self.__l} -- {self.__m} -- {self.__r} |")

        #check if path can be found
        if self.__dis.isReachable():
            #check if mid value is percise enough to exit recurssion
            if self.__percision(self.__m) >= self.__p:
                print(f"    Eps {self.__m}: <reachable>\n")
                self.__r = self.__m
                return self.search()
            else:
                print(f"    Eps {self.__m}: <reachable> <meets percision>\n")
                return self.__m
        else:
            print(f"    Eps {self.__m}: <unreachable>\n")
            self.__l = self.__m
            return self.search()
