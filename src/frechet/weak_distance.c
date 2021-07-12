/*! \file weak_distance.c
    \brief
    This program is a derrvied work of "Weak Frechet distance decision problem
		1.0." Defines functions used to compute Weak Frechet metric, distance
    and diagrams for two polynomial curves.

      Author: Carola Wenk
      cwenk@tulane.edu
      http://www.cs.tulane.edu/~carola/research/code.html

      Contributer: Will Rodman
      wrodman@tulane.edu

    Licensed under the Apache License, Version 2.0 (the "License")
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    \author Carola Wenk
    \copyright Copyright 2004 Carola Wenk
*/

/*! \include <stdlib.h>
    \include <stdbool.h>
    \include "weak_distance.h"
    \include "distance.c"
*/
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <float.h>
#include "distance.c"
#include "weak_distance.h"

/*!	\def WHITE 0
		\brief Defines 0 as a reachable interval inside free space.

		\def GRAY 1
		\brief Defines 1 as a unreachable interval inside free space.

		\def NONE 2
		\brief Defines 0 as an interval does not exist inside free space.
*/
#define WHITE 0
#define GRAY 1
#define NONE 2

/*!	\def HORIZONTAL 0
		\def VERTICAL 1
*/
#define HORIZONTAL 0
#define VERTICAL 1

/*! \var int **vColor
		\var **hColor
*/
int **vColor;
int **hColor;

/*! \var DFS **vReachedFrom
		\var DFS **hReachedFrom
		\var bool FSfound
*/
DFS **vReachedFrom;
DFS **hReachedFrom;
bool FSfound;

/*! \var int lastI
		\var int lastJ
		\var int lastInterval
*/
int lastI = 0;
int lastJ = 0;
int lastInterval = -1;

/*! \fn void create_freespace_reachabilitytable()
*/
void create_freespace_reachabilitytable() {
	int i;
	// dimensions: hFS[no2][no1-1]
	hFSs = (double**)malloc(no2 * sizeof(double*)); // rows j
	hFSe = (double**)malloc(no2 * sizeof(double*));
	hColor = (int**)malloc(no2 * sizeof(int*));
	hReachedFrom = (DFS**)malloc(no2 * sizeof(DFS*));

	for(i = 0; i < no2; i++){
		hFSs[i] = (double*)malloc((no1 - 1) * sizeof(double)); // columns i
		hFSe[i] = (double*)malloc((no1 - 1) * sizeof(double));
		hColor[i] = (int*)malloc((no1 - 1) * sizeof(int));
		hReachedFrom[i] = (DFS*)malloc((no1 - 1) * sizeof(DFS));
	}

	// dimensions: vFS[no2-1][no1]
	vFSs = (double**)malloc((no2 - 1) * sizeof(double*));
	vFSe = (double**)malloc((no2 - 1) * sizeof(double*));
	vColor = (int**)malloc((no2 - 1) * sizeof(int*));
	vReachedFrom = (DFS**)malloc((no2-1) * sizeof(DFS*));

	for(i = 0; i < no2-1; i++){
		vFSs[i] = (double*)malloc(no1 * sizeof(double));
		vFSe[i] = (double*)malloc(no1 * sizeof(double));
		vColor[i] = (int*)malloc(no1 * sizeof(int));
		vReachedFrom[i] = (DFS*)malloc(no1 * sizeof(DFS));
	}
}

/*! \fn void isreachable_visit(int currentI, int currentJ, int currentInterval)
*/
void isreachable_visit(int currentI, int currentJ, int currentInterval) {

	if(FSfound) return;

	// VERTICAL
	if(currentInterval == VERTICAL && vColor[currentJ][currentI] == WHITE) {
	vColor[currentJ][currentI] = GRAY;

		if(currentI == no1 - 1 && currentJ == no2 - 2) {
			// path to upper right corner found.
			lastI = currentI;
			lastJ = currentJ;
			lastInterval = VERTICAL;
			FSfound = true;
			return;
		} else {

			if(currentI > 0) {
				// left vertical
				if(vColor[currentJ][currentI-1] == WHITE) {
					// save predecessor
					vReachedFrom[currentJ][currentI-1].interval = currentInterval;
					vReachedFrom[currentJ][currentI-1].i = currentI;
					vReachedFrom[currentJ][currentI-1].j = currentJ;
					isreachable_visit(currentI - 1, currentJ, VERTICAL);
				}
			}

			if(currentI < no1 - 1) {
				// right vertical
				if(vColor[currentJ][currentI+1] == WHITE) {
					// save predecessor
					vReachedFrom[currentJ][currentI+1].interval = currentInterval;
					vReachedFrom[currentJ][currentI+1].i = currentI;
					vReachedFrom[currentJ][currentI+1].j = currentJ;
					isreachable_visit(currentI + 1, currentJ, VERTICAL);
				}
			}

			if(currentI > 0) {
				// lower left horizontal
				if(hColor[currentJ][currentI-1] == WHITE) {
					// save predecessor
					hReachedFrom[currentJ][currentI-1].interval = currentInterval;
					hReachedFrom[currentJ][currentI-1].i = currentI;
					hReachedFrom[currentJ][currentI-1].j = currentJ;
					isreachable_visit(currentI - 1, currentJ, HORIZONTAL);
				}
			}

			if(currentI < no1 - 1) {
				// lower right horizontal
				if(hColor[currentJ][currentI] == WHITE) {
					// save predecessor
					hReachedFrom[currentJ][currentI].interval = currentInterval;
					hReachedFrom[currentJ][currentI].i = currentI;
					hReachedFrom[currentJ][currentI].j = currentJ;
					isreachable_visit(currentI, currentJ, HORIZONTAL);
				}
			}

			if(currentI > 0) {
				// upper left horizontal
				if(hColor[currentJ+1][currentI-1] == WHITE) {
					// save predecessor
					hReachedFrom[currentJ+1][currentI-1].interval = currentInterval;
					hReachedFrom[currentJ+1][currentI-1].i = currentI;
					hReachedFrom[currentJ+1][currentI-1].j = currentJ;
					isreachable_visit(currentI - 1, currentJ + 1, HORIZONTAL);
				}
			}

			if(currentI < no1 - 1) {
				// lower right horizontal
				if(hColor[currentJ+1][currentI] == WHITE) {
					// save predecessor
					hReachedFrom[currentJ+1][currentI].interval = currentInterval;
					hReachedFrom[currentJ+1][currentI].i = currentI;
					hReachedFrom[currentJ+1][currentI].j = currentJ;
					isreachable_visit(currentI ,currentJ + 1, HORIZONTAL);
				}
			}
		}
	}

	// HORIZONTAL
	if(currentInterval == HORIZONTAL && hColor[currentJ][currentI] == WHITE) {
	hColor[currentJ][currentI] = GRAY;

		if(currentI == no1 - 2 && currentJ == no2 - 1) {
			// Path to upper right corner found.
			lastI = currentI;
			lastJ = currentJ;
			lastInterval = HORIZONTAL;
			FSfound = true;
			return;
		} else {

			if(currentJ < no2 - 1) {
				// upper left vertical
				if(vColor[currentJ][currentI] == WHITE) {
					// save predecessor
					vReachedFrom[currentJ][currentI].interval = currentInterval;
					vReachedFrom[currentJ][currentI].i = currentI;
					vReachedFrom[currentJ][currentI].j = currentJ;
					isreachable_visit(currentI, currentJ, VERTICAL);
				}

				// upper right vertical
				if(vColor[currentJ][currentI+1] == WHITE) {
					// save predecessor
					vReachedFrom[currentJ][currentI+1].interval = currentInterval;
					vReachedFrom[currentJ][currentI+1].i = currentI;
					vReachedFrom[currentJ][currentI+1].j = currentJ;
					isreachable_visit(currentI + 1, currentJ, VERTICAL);
				}

				// upper horizontal
				if(hColor[currentJ+1][currentI] == WHITE) {
					// save predecessor
					hReachedFrom[currentJ+1][currentI].interval = currentInterval;
					hReachedFrom[currentJ+1][currentI].i = currentI;
					hReachedFrom[currentJ+1][currentI].j = currentJ;
					isreachable_visit(currentI, currentJ + 1, HORIZONTAL);
				}
			}

			if(currentJ > 0) {
				// lower left vertical
				if(vColor[currentJ-1][currentI] == WHITE) {
					// save predecessor
					vReachedFrom[currentJ-1][currentI].interval = currentInterval;
					vReachedFrom[currentJ-1][currentI].i = currentI;
					vReachedFrom[currentJ-1][currentI].j = currentJ;
					isreachable_visit(currentI, currentJ - 1, VERTICAL);
				}

				// lower right vertical
				if(vColor[currentJ-1][currentI+1] == WHITE) {
					// save predecessor
					vReachedFrom[currentJ-1][currentI+1].interval = currentInterval;
					vReachedFrom[currentJ-1][currentI+1].i = currentI;
					vReachedFrom[currentJ-1][currentI+1].j = currentJ;
					isreachable_visit(currentI + 1, currentJ - 1, VERTICAL);
				}

				// lower horizontal
				if(hColor[currentJ-1][currentI] == WHITE) {
					// save predecessor
					hReachedFrom[currentJ-1][currentI].interval = currentInterval;
					hReachedFrom[currentJ-1][currentI].i = currentI;
					hReachedFrom[currentJ-1][currentI].j = currentJ;
					isreachable_visit(currentI, currentJ - 1, HORIZONTAL);
				}
			}
		}
	}
}

/*! \fn bool isreachable()
*/
bool isreachable() {
	int i, j;

	// horizontal
	for(i = 0; i < no1 - 1; i++) {
		for(j = 0; j <= no2 - 1; j++) {
			if(hFSs[j][i] < hFSe[j][i]) {
				hColor[j][i] = WHITE;
			} else {
				hColor[j][i] = NONE;
			}
			hReachedFrom[j][i].interval = -1;
			hReachedFrom[j][i].i = -1;
			hReachedFrom[j][i].j = -1;
		}
	}

	// vertical
	for(i = 0; i <= no1 - 1; i++) {
		for(j = 0; j< no2 - 1; j++) {
			if(vFSs[j][i] < vFSe[j][i]) {
				vColor[j][i] = WHITE;
			} else {
				vColor[j][i] = NONE;
			}
			vReachedFrom[j][i].interval = -1;
			vReachedFrom[j][i].i = -1;
			vReachedFrom[j][i].j = -1;
		}
	}

	// lower left corner
	if(hFSs[0][0] == 0) {
		hColor[0][0] = WHITE;
	} else {
		hColor[0][0] = NONE;
	}

	if(vFSs[0][0] == 0) {
		vColor[0][0] = WHITE;
	} else {
		vColor[0][0] = NONE;
	}

	// upper right corner
	if(hFSe[no2-1][no1-2] == 1) {
		hColor[no2-1][no1-2] = WHITE;
	} else {
		hColor[no2-1][no1-2] = NONE;
	}

	if(vFSe[no2-2][no1-1] == 1) {
		vColor[no2-2][no1-1] = WHITE;
	} else {
		vColor[no2-2][no1-1] = NONE;
	}
	FSfound = false;
	isreachable_visit( 0, 0, HORIZONTAL);
	return FSfound;
}

/*! \fn bool computemaxdistances(double epsilon)
*/
bool computemaxdistances(double epsilon) {
	int i;
	int maxi = -1;
	double maxDistance = 0;
	double distance;

	if(no1 == 1) {
		for(i = 0; i < no2; i++) {
			distance = (curve1[0].x - curve2[i].x) * (curve1[0].x - curve2[i].x) +
			           (curve1[0].y - curve2[i].y) * (curve1[0].y - curve2[i].y);

			if(distance > maxDistance) {
				maxDistance = distance;
				maxi = i;
			}
		}
	} else {
		for(i = 0; i < no1; i++){
			distance = (curve2[0].x - curve1[i].x) * (curve2[0].x - curve1[i].x) +
			           (curve2[0].y - curve1[i].y) * (curve2[0].y - curve1[i].y);
			if(distance > maxDistance) {
				maxDistance = distance;
				maxi = i;
			}
		}
	}

	if(maxDistance <= epsilon * epsilon) {
		return true;
	} else {
		return false;
	}
}
