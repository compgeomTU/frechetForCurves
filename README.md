# pyfrechet
## Frechet Distance Python Library

pyfrechet is a Python 3 library intended to visualize free space, discover
paths and manage information for the Frechet distance. This library derives
its work from [Frechet distance decision problem 1.0](http://www.cs.tulane.edu/~carola/research/code.html)
and [Weak Frechet distance decision problem 1.0](http://www.cs.tulane.edu/~carola/research/code.html),
two programs written by [Dr. Carola Wenk](cs.tulane.edu/~carola/). The library
open source design allows for new programs to be added and build upon existing
ones.

### Installation
Download from Python Package Index using the command line below.
```
pip install pyfrechet
```

### Documentation
A GUI version of the source code documentation can be viewed by opening
[documentation.html](documentation.html). The GUI is generated by Doxygen and
supporting packages can be found in [/docs](/docs).

### Dependencies
- [CFFI](cffi.readthedocs.io) allows source code written in C to be compiled as .so files.
- [NumPy](numpy.org) is used to calculate dimentions of free space diagrams.
- Free space diagrams are stored using [Shapleys](shapely.readthedocs.io) Polygon and Multipolygon classes.
- The GUI of the free space diagram is built using [matplotlib](matplotlib.org).

## Examples
Below are several examples how the library can be used.

### Creating empty Frechet and Weak Frechet distance objects:
**example .py**
```
from pyfrechet.distance import StrongDistance, WeakDistance

strong_distance = StrongDistance()
print(strong_distance)

weak_distance = WeakDistance()
print(weak_distance)
```
**output**
```
                Frechet Distance       |  StrongDistance
                ========================================
                Curve 1 File           |  N/A
                Curve 2 File           |  N/A


                Frechet Distance       |  WeakDistance
                ========================================
                Curve 1 File           |  N/A
                Curve 2 File           |  N/A
```

### Creating Frechet and Weak Frechet distance objects with two curves:
**sample_1.txt**
```
484472 4.21292e+006
484183 4.21293e+006
484166 4.21314e+006
484140 4.21347e+006

... ...

483379 4.21391e+006
483389 4.21385e+006
483349 4.21362e+006
483280 4.21325e+006
```
**sample_2.txt**
```
483282.000000 4213251.000000
483281.000000 4213333.000000
483279.000000 4213347.000000
483278.000000 4213393.000000

... ...

484152.172363 4212991.013613
484137.000000 4212937.000000
484326.000000 4212933.000000
484462.000000 4212918.000000
```
**example .py**
```
from pyfrechet.distance import StrongDistance, WeakDistance

strong_distance = StrongDistance.setCurves(curve_1_file="sample_1.txt", \
                                           curve_2_file="sample_2.txt", \
                                           reverse_curve_2=True)
print(strong_distance)

weak_distance = WeakDistance.setCurves(curve_1_file="sample_1.txt", \
                                       curve_2_file="sample_2.txt", \
                                       reverse_curve_2=True)
print(weak_distance)
```
**output**
```
                Frechet Distance       |  StrongDistance
                ========================================
                Curve 1 File           |  curve_1_file.txt
                Curve 2 File           |  curve_2_file.txt


                Frechet Distance       |  WeakDistance
                ========================================
                Curve 1 File           |  curve_1_file.txt
                Curve 2 File           |  curve_2_file.txt
```

### Accessing curve file data:
**example .py**
```
from pyfrechet.distance import StrongDistance

strong_distance = StrongDistance.setCurves("sample_1.txt", "sample_2.txt", True)
curve_1_lenght = strong_distance.getCurve1Lenght()
curve_1 = strong_distance.getCurve1()

print(f"Curve 1 lenght: {curve_1_lenght}")
print(f"First coordinates of curve 1: ({curve_1[0].x}, {curve_1[0].y})")
```
**output**
```
Curve 1 lenght: 59
First coordinates of curve 1: (483282.000000,  4213251.000000)
```

### Checking if path exists inside free space:
**example .py**
```
from pyfrechet.distance import StrongDistance

strong_distance = StrongDistance.setCurves("sample_1.txt", "sample_2.txt", True)

strong_distance.setFreeSpace(epsilon=50)
is_path = strong_distance.isReachable()
print(f"Path exists for epsilon 50: {is_path}")

strong_distance.setFreeSpace(epsilon=100)
is_path = strong_distance.isReachable()
print(f"Path exists for epsilon 100: {is_path}")
```
**output**
```
Path exists for epsilon 50: False
Path exists for epsilon 100: True
```

### Finding minimum epsilon for path using default binary search:
**example .py**
```
from pyfrechet.distance import StrongDistance
from pyfrechet.optimise import BinarySearch

strong_distance = StrongDistance.setCurves("sample_1.txt", "sample_2.txt", True)

binary_search = BinarySearch(strong_distance)
epsilon = binary_search.search()

print(f"Epsilon found using binary search: {epsilon}")
```
**output**
```
Checking if epsilon is reachable:
    | 0 -- 6986.0 -- 13972 |
    Eps 6986.0: <reachable>

Checking if epsilon is reachable:
    | 0 -- 3493.0 -- 6986.0 |
    Eps 3493.0: <reachable>

... ...

Checking if epsilon is reachable:
    | 67.7962646484375 -- 68.00946044921875 -- 68.22265625 |
    Eps 68.00946044921875: <unreachable>

Checking if epsilon is reachable:
    | 68.00946044921875 -- 68.11605834960938 -- 68.22265625 |
    Eps 68.11605834960938: <reachable> <meets percision>

Epsilon found using binary search: 68.11605834960938
```

### Finding minimum epsilon for path using custom binary search:
```
from pyfrechet.distance import StrongDistance
from pyfrechet.optimise import BinarySearch

strong_distance = StrongDistance.setCurves("sample_1.txt", "sample_2.txt", True)

binary_search = BinarySearch(strong_distance)
binary_search.setBoundaries(left=50, right=100)
binary_search.setPercision(0.0001)
epsilon = binary_search.search()

print(f"Epsilon found using binary search: {epsilon}")
```
**output**
```
Checking if epsilon is reachable:
    | 50 -- 75.0 -- 100 |
    Eps 75.0: <reachable>

Checking if epsilon is reachable:
    | 50 -- 62.5 -- 75.0 |
    Eps 62.5: <unreachable>

... ...

Checking if epsilon is reachable:
    | 67.1875 -- 67.96875 -- 68.75 |
    Eps 67.96875: <unreachable>

Checking if epsilon is reachable:
    | 67.96875 -- 68.359375 -- 68.75 |
    Eps 68.359375: <reachable> <meets percision>

Epsilon found using binary search: 68.359375
```

### Visualizing free space diagram for epsilon:
**example .py**
```
from pyfrechet.distance import StrongDistance
from pyfrechet.visualize import FreeSpaceDiagram

strong_distance = StrongDistance.setCurves("sample_1.txt", "sample_2.txt", True)
strong_distance.setFreeSpace(100)

free_space_diagram = FreeSpaceDiagram(strong_distance)
free_space_diagram.plot()
```
**output**
![Image](/docs/figure_1.png?raw=true)

### Visualizing free space diagram for epsilon with cell gird lines and weighted cells:
**example .py**
```
from pyfrechet.distance import StrongDistance
from pyfrechet.visualize import FreeSpaceDiagram

strong_distance = StrongDistance.setCurves("sample_1.txt", "sample_2.txt", True)
strong_distance.setFreeSpace(100)

free_space_diagram = FreeSpaceDiagram(strong_distance)
free_space_diagram.plot(cell_gridlines=True, weighted_cells=True)
```
**output**
![Image](/docs/figure_2.png?raw=true)

### Visualizing free space diagram with sliding bar for epsilon:
**example .py**
```
from pyfrechet.distance import StrongDistance
from pyfrechet.visualize import FreeSpaceDiagram

strong_distance = StrongDistance.setCurves("sample_1.txt", "sample_2.txt", True)

free_space_diagram = FreeSpaceDiagram(strong_distance)
free_space_diagram.addEpsilonSlider(min=50, max=500, step=50)
free_space_diagram.plot(cell_gridlines=True, weighted_cells=True)
```
**output**
![Image](/docs/figure_3.gif?raw=true)

### Visualizing trajectories:
**example .py**
```
from pyfrechet.distance import StrongDistance
from pyfrechet.visualize import Trajectories

strong_distance = StrongDistance.setCurves("sample_1.txt", "sample_2.txt", True)

trajectories = Trajectories(strong_distance)
trajectories.plot()
```
**output**
![Image](/docs/figure_4.png?raw=true)

## Author
- **Will Rodman** wrodman@tulane.edu

### Version History
- **0.1.13** 9-2-2021
- **0.2.0** 10-3-2021 Added Trajectory class to visualize curves.

### Lisence
MIT License • Copyright (c) 2021 Computational Geometry @ Tulane
