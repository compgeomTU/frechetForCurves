import sys,os

sys.path.insert(0, "../src/pyfrechet/")

from distance import StrongDistance, WeakDistance

print("TESTING -- 'pyfrechet.distance.StrongDistance'\n\n")

sd = StrongDistance.setcurves("test_curve_1.txt", "test_curve_2.txt", True)

sd.setfreespace(70)

vc = sd.getverticalcurve()
print(f"    First point on vertical curve: ({vc[0].x}, {vc[0].y})\n")

hc = sd.getverticalcurve()
print(f"    First point on horizonal curve: ({hc[0].x}, {hc[0].y})\n")

ve = sd.getverticaledges()
print(f"    Number of edges on vertical curve: {ve}\n")

he = sd.gethorizontaledges()
print(f"    Number of edges on vertical curve: {he}\n")

fs = sd.getfreespace()
print(f"""    First wall and floor or freespace cell:

              {fs.horizontal_end[0][0]}

              {fs.horizontal_start[0][0]}
                    {fs.vertical_start[0][0]}     {fs.vertical_end[0][0]}\n""")

ir =  sd.isreachable()
print(f"    Test passed if free space is reachable: {ir}\n")

print("TESTING -- 'pyfrechet.distance.WeakDistance'\n\n")

wd = WeakDistance.setcurves("test_curve1.txt", "test_curve2.txt", True)

wd.setfreespace(70)

vc = wd.getverticalcurve()
print(f"    First point on vertical curve: ({vc[0].x}, {vc[0].y})\n")

hc = wd.getverticalcurve()
print(f"    First point on horizonal curve: ({hc[0].x}, {vhc[0].y})\n")

ve = wd.getverticaledges()
print(f"    Number of edges on vertical curve: {ve}\n")

he = wd.gethorizontaledges()
print(f"    Number of edges on vertical curve: {he}\n")

fs = wd.getfreespace()
print(f"""    First wall and floor or freespace cell:

              {fs.horizontal_end}

              {fs.horizontal_start}
                    {fs.vertical_start}     {fs.vertical_end}\n""")

ir =  wd.isreachable()
print(f"    Test passed if free space is reachable: {ir}\n")
