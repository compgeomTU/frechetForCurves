import math
from decimal import Decimal
from distance import *

class BinarySearch:

    __l: float
    __r: float
    __m: float
    __p: float

    def __init__(self, distance):
        if isinstance(distance, StrongDistance) or \
           isinstance(distance, WeakDistance):
            self.__dis = distance
            self.__l = -1
            self.__r = -1
            self.__p = -1
        else:
            raise TypeError(f"{distance.__name__} is not a valid distance."
                            f"Must be of type {StrongDistance.__name__} or "
                            f"{WeakDistance.__name__}."
                            )

    @staticmethod
    def _vertexlength(c, n):
        l = 0
        for i in range(n-1):
            l += math.dist([c[i].x, c[i].y], [c[i+1].x, c[i+1].y])
        return l

    def setBoundaries(self, left, right):
        self.__l = left
        self.__r = right

    def setPercision(self, precision):
        self.__p = Decimal(str(precision)).as_tuple().exponent

    def search(self):
        #Check if boundieries have been set. if not will take maximum
        #distance across free space diagram
        if self.__l == -1 or self.__r == -1:
            l1 = self._vertexlength(self.__dis.getcurve2(), \
                self.__dis.getcurve2lenght())
            l2 = self._vertexlength(self.__dis.getcurve1(),\
                self.__dis.getcurve1lenght())
            self.__l = 0
            self.__r = int(math.dist([l2, 0], [0, l1]))

        if self.__p = -1: self.__p = 1000

        print("Inital boundieries set:")
        print(f"    | {self.__l} --- {self.__r} |")
        print(f"    precision = {self.__p}\n")

        self.__m = (self.__l + self.__r) / 2
        self.__dis.setfreespace(self.__m)

        print(f"Checking if epsilon is reachable:")
        print(f"    | {self.__l} -- {self.__m} -- {self.__r} |")

        #check if path can be found
        if self.__dis.isreachable():
            #check if mid value is percise enough to exit recurssion
            if Decimal(str(self.__m)).as_tuple().exponent >= self.__p:
                print(f"    Eps {self.__m}: <reachable>\n")
                self.r = self.__m
                return self.search()
            else:
                print(f"    Eps {self.__m}: <reachable> <meets percision>\n")
                return self.__m
        else:
            print(f"    Eps {self.__m}: <unreachable>\n")
            self.__l = self.__m
            return self.search()
