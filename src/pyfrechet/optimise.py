import math

class BinarySearch:

    dis = None
    left_bound = None
    right_bound = None
    mid = None
    precision = 0.001

    def __init__self(distance):
        if type(distance).__name__ == "StrongDistance":
            self.dis = distance
        elif type(distance).__name__ == "WeakDistance":
            self.dis = distance
        else:
            raise TypeError("""binary search must be performed on Frechet
                               StrongDistance or WeakDistance class""")


    def search():
        #Check if boundieries have been set. if not will take maximum
        #distance across free space diagram
        if left_bound == None or right_bound == None:
            def verticelength(c, n):
                lenght = 0
                for i in range(n-1):
                    lenght += math.dist([c[i].x, c[i].y], \
                        [c[i+1].x, c[i+1].y])
                return lenght

            vlenght = verticelength(dis.getverticalcurve(), \
                dis.getverticaledges())

            hlenght = verticelength(dis.gethorizontalcurve(),\
                dis.gethorizontaledges())

            left_bound = 0
            right_bound = math.dist(hlenght, 0, 0, vlenght)

        mid = (left_bound + right_bound) / 2

        self.dis.setfreespace(mid)

        #check if path can be found
        if self.dis.isreachable():
            #check if mid value is percise enough to exit recurssion
            if int(log10(mid))+1 >= int(log10(precision))+1:
                left_bound = mid
                return search()
            else:
                return mid
        else:
            right_bound = mid
            return search()
