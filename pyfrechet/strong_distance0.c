/*! \file strong_distance.c
    \brief
    This program is a derrvied work of "Frechet distance decision
    problem 1.0." Defines functions used to compute Strong Frechet metric,
    distance and diagrams for two polynomial curves.

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
    \include "strong_distance.h"
    \include "distance.c"
*/
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <float.h>
#include "distance.c"
#include "strong_distance.h"

/*! \def maxdouble(a, b)
    \breif defines greatest value of two double types
    \param a
    \param b
*/
#define maxdouble(a, b) \
  ({ double _a = (a), _b = (b); _a > _b ? _a : _b; })

/*! \fn void create_freespace_reachabilitytable()
*/
void create_freespace_reachabilitytable() {
  int i;

  // dimensions: hFS[no2][no1-1]
  hFSs = (double**)malloc(no2 * sizeof(double*)); // rows j
  hFSe = (double**)malloc(no2 * sizeof(double*));
  hRTs = (double**)malloc(no2 * sizeof(double*));
  hRTe = (double**)malloc(no2 * sizeof(double*));

  for(i = 0; i < no2; i++) {
    hFSs[i] = (double*)malloc((no1 - 1) * sizeof(double)); // columns i
    hFSe[i] = (double*)malloc((no1 - 1) * sizeof(double));
    hRTs[i] = (double*)malloc((no1 - 1) * sizeof(double));
    hRTe[i] = (double*)malloc((no1 - 1) * sizeof(double));
  }

  // dimensions: vFS[no2-1][no1]
  vFSs = (double**)malloc((no2 - 1) * sizeof(double*));
  vFSe = (double**)malloc((no2 - 1) * sizeof(double*));
  vRTs = (double**)malloc((no2 - 1) * sizeof(double*));
  vRTe = (double**)malloc((no2 - 1) * sizeof(double*));

  for(i = 0; i < no2-1; i++) {
    vFSs[i] = (double*)malloc(no1 * sizeof(double));
    vFSe[i] = (double*)malloc(no1 * sizeof(double));
    vRTs[i] = (double*)malloc(no1 * sizeof(double));
    vRTe[i] = (double*)malloc(no1 * sizeof(double));
  }
}

/*! \fn void setreachabilitytable()
*/
void setreachabilitytable() {
  int i, j;

  for(i = 0; i < no1; i++) {
    vRTs[0][i] = vFSs[0][i];
    vRTe[0][i] = vFSe[0][i];

    for(j = 1; j < no2-1; j++) {
      vRTs[j][i] = -5;
      vRTe[j][i] = -5;
    }
  }

  for(j = 0; j < no2; j++) {
    hRTs[j][0]=hFSs[j][0];
    hRTe[j][0]=hFSe[j][0];

    for(i = 1; i < no1 - 1; i++) {
      hRTs[j][i] = -5;
      hRTe[j][i] = -5;
    }
  }

  for(i = 0; i < no1 - 1; i++) {
    for(j = 0; j < no2 - 1; j++) {
      if(vRTs[j][i] >= 0 && vRTe[j][i] > vRTs[j][i]) {
        // left boundary is white
        // TOP hRT = TOP hFS
        // only if not at topmost cell
        hRTs[j+1][i] = hFSs[j+1][i];
        hRTe[j+1][i] = hFSe[j+1][i];
      } else {
        // left boundary is black
        if(hRTs[j][i] >= 0 && hRTe[j][i] > hRTs[j][i]) {
          // bottom boundary is white
          hRTs[j+1][i] = maxdouble(hFSs[j+1][i], hRTs[j][i]);
          hRTe[j+1][i] = hFSe[j+1][i];

          if(hRTe[j+1][i] <= hRTs[j+1][i]) {
            // interval black
            hRTs[j+1][i] = -1;
            hRTe[j+1][i] = -1;
          }
        } else {
          // bottom boundary is black
          hRTs[j+1][i] = -1;
          hRTe[j+1][i] = -1;
        }
      }
      if(hRTs[j][i] >= 0 && hRTe[j][i] > hRTs[j][i]) {
        // bottom boundary is white
        // RIGHT vRT = RIGHT vFS
        // only if not at rightmost cell
        vRTs[j][i+1] = vFSs[j][i+1];
        vRTe[j][i+1] = vFSe[j][i+1];
      } else {
        // bottom boundary is black
        if(vRTs[j][i] >= 0 && vRTe[j][i] > vRTs[j][i]) {
          // left boundary is white
          vRTs[j][i+1] = maxdouble(vFSs[j][i+1], vRTs[j][i+1]);
          vRTe[j][i+1]=vFSe[j][i+1];

          if(vRTe[j][i+1] <= vRTs[j][i+1]) {
            // interval black
            vRTe[j][i+1] = -1;
            vRTs[j][i+1] = -1;
          }
        } else {
          // left boundary is black
          vRTe[j][i+1] = -1;
          vRTs[j][i+1] = -1;
        }
      }
    }
  }
}

/*! \fn bool isreachable)
*/
bool isreachable() {
  int vlast = 0;
  int i, j;

  // Upper right RT corner is white.
  if((vRTe[no2-2][no1-1] == 1) &&
     (hRTe[no2-1][no1-2] == 1) &&
     ((vRTs[no2-2][no1-1] < vRTe[no2-2][no1-1]) ||
     (hRTs[no2-1][no1-2] < hRTe[no2-1][no1-2]))) {
    // Lower left RT corner is white
    if((vRTs[0][0] == 0) &&
       (hRTs[0][0] == 0) &&
       ((vRTs[0][0] < vRTe[0][0]) ||
       (hRTs[0][0] < hRTe[0][0]))) {

      // Start traceback.
      vlast = 1;
      i = no1 - 1;
      j = no2 - 2;

      while(i > 0 || j > 0) {
        if(vlast) {
          if(vRTs[j][i-1] >= 0 && vRTe[j][i-1] > vRTs[j][i-1]) {
            // left boundary is white
            i--;
          } else if(hRTs[j][i-1] >= 0 && hRTe[j][i-1] > hRTs[j][i-1]) {
            // lower boundary is white
            vlast = 0;
            i--;
          } else {
            // NO path found.
            return false;
          }
        } else {
          if(vRTs[j-1][i] >= 0 && vRTe[j-1][i] > vRTs[j-1][i]) {
            // left boundary is white
            j--;
            vlast = 1;
          } else if(hRTs[j-1][i] >= 0 && hRTe[j-1][i] > hRTs[j-1][i]) {
            // lower boundary is white
            j--;
          } else {
            // NO path found.
            return false;
          }
        }
      }
      // Path found.
      return true;
    }
  }
  // NO path found. Upper/lower corners not white.
  return false;
}
