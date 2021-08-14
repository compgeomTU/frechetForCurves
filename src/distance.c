/*! \file distance.c
    \brief
    This program is a derrvied work of "Frechet distance decision
    problem 1.0" and "Weak Frechet distance decision problem 1.0." Defines
    functions used to compute frechet metric, distance and diagrams for two
    polynomial curves.

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
    \include <stdio.h>
    \include <string.h>
    \include <math.h>
    \include <stdbool.h>
    \include <errno.h>
    \include "frechet.h"
*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <errno.h>
#include "distance.h"

/*! \var point *curve1
    \var point *curve2
    \var point *curvetmp
*/
point *curve1;
point *curve2;
point *curvetmp;

/*! \var int no1
    \var int no2
*/
int no1, no2;

/*! \var double **vFSs
    \var double **vFSe
    \var double **hFSs
    \var double **hFSe
*/
double **vFSs;
double **vFSe;
double **hFSs;
double **hFSe;

/*! \var double **vRTs
    \var double **vRTe
    \var double **hRTs
    \var double **hRTe
*/
double **vRTs;
double **vRTe;
double **hRTs;
double **hRTe;

/*! \fn int createcurves(char* curve1filename, char* curve2filename,
    bool reversecurve2)
*/
int createcurves(char* curve1filename, char* curve2filename, \
                  bool reversecurve2) {
  FILE *curve1fp, *curve2fp;
  int i, j;
  double x, y;

  // return errno if file did not open correctly
  curve1fp = fopen(curve1filename, "r");
  if(curve1fp == NULL) return errno;

  // first count vertices
  no1 = 0;
  while(fscanf(curve1fp, "%lf %lf", &x, &y) != EOF) no1++;
  fclose(curve1fp);

  curve1fp = fopen(curve1filename, "r");
  if(curve1fp == NULL) return errno;

  curve1 = (point*)malloc(no1 * sizeof(point));

  // read in curve, and delete duplicate vertices
  for(i = 0, j = 0; i < no1; i++, j++) {
    if(fscanf(curve1fp , "%lf %lf", &x, &y) == 2) {
    curve1[j].x = x;
    curve1[j].y = y;
    if((j > 0) &&
       (curve1[j].x==curve1[j-1].x) &&
       (curve1[j].y == curve1[j-1].y)) j--;
    } else return ECANCELED;
    if(ferror(curve1fp)) return errno;
  }
  fclose(curve1fp);

  if(j < no1) {
    no1 = j;
    curve1 = (point*)realloc(curve1, no1 * sizeof(point));
  }

  // return errno if file did not open correctly
  curve2fp = fopen(curve2filename, "r");
  if(curve2fp == NULL) return errno;

  // first count vertices
  no2 = 0;
  while(fscanf(curve2fp, "%lf %lf", &x, &y) != EOF) no2++;
  fclose(curve2fp);

  curve2fp = fopen(curve2filename, "r");
  if(curve2fp == NULL) return errno;

  curvetmp = (point*)malloc(no2 * sizeof(point));

  // read in curve, and delete duplicate vertices
  // store in temporary array in order to reverse curve later if needed
  for(i = 0, j = 0; i < no2; i++, j++) {
    if(fscanf(curve2fp, "%lf %lf", &x, &y) == 2) {
    curvetmp[j].x = x;
    curvetmp[j].y = y;
    if((j > 0) &&
       (curvetmp[j].x == curvetmp[j-1].x) &&
       (curvetmp[j].y == curvetmp[j-1].y)) j--;
    } else return ECANCELED;
    if(ferror(curve2fp)) return errno;
  }
  fclose(curve2fp);

  if(j < no2) {
    no2 = j;
    curvetmp = (point*)realloc(curvetmp, no2 * sizeof(point));
  }

  curve2 = (point*)malloc(no2 * sizeof(point));

  if(reversecurve2) {
    for(int i = 0; i < no2; i++) curve2[i] = curvetmp[no2-1-i];
  } else {
    for(int i = 0; i < no2; i++) curve2[i] = curvetmp[i];
  }
  return 0;
}

/*! \fn calculatefreespace(double &x1, double &y1, double &x2, double &y2,
    double &xa, double &ya, double &start, double &end, double epsilon)
*/
void calculatefreespace(double x1, double y1, double x2, double y2, \
                        double xa, double ya, double *start, double *end, \
                        double epsilon) {
  double xdiff, ydiff, root, b, divisor, t1, t2, q;

  xdiff = x2 - x1;
  ydiff = y2 - y1;
  divisor = xdiff * xdiff + ydiff * ydiff;

  b = (xa - x1) * xdiff + (ya - y1) * ydiff;
  q = (x1 * x1 + y1 * y1 + xa * xa + ya * ya -
      2 * x1 * xa - 2 * y1 * ya - epsilon * epsilon) * divisor;
  root = b * b - q;

  if(root < 0) {
    *start = -1;
    *end = -1;
    return;
  }

  root = sqrt(root);
  t2 = (b + root) / divisor;
  t1 = (b - root) / divisor;
  if(t1 < 0) t1 = 0;
  if(t2 < 0) t2 = 0;
  if(t1 > 1) t1 = 1;
  if(t2 > 1) t2 = 1;
  *start = t1;
  *end = t2;

  // make sure black intervals are correctly marked black
  if(*start == *end) {
    *start = -1;
    *end = -1;
  }
}

/*! \fn void setfreespace(double epsilon)
*/
void setfreespace(double epsilon) {
  int i, j;

  // calulating free space for horizontal FS
  for(i = 0; i < no1 - 1; i++){
    for(j = 0; j <= no2 - 1; j++){
      calculatefreespace(curve1[i].x, curve1[i].y, curve1[i+1].x, curve1[i+1].y,
                         curve2[j].x, curve2[j].y, &hFSs[j][i], &hFSe[j][i],
                         epsilon);
    }
  }

  // calulating free space for horizontal vertical FS
  for(i = 0; i <= no1 - 1; i++){
    for(j = 0; j < no2 - 1; j++){
      calculatefreespace(curve2[j].x, curve2[j].y, curve2[j+1].x, curve2[j+1].y,
                         curve1[i].x, curve1[i].y, &vFSs[j][i], &vFSe[j][i],
                         epsilon);
    }
  }
}

/*! \fn freespace getfreespace()
*/
freespace getfreespace() {
  return (freespace) {
    .vertical_start = vFSs,
    .vertical_end = vFSe,
    .horizontal_start = hFSs,
    .horizontal_end = hFSe
  };
}

/*! \fn point* getcurve1()
*/
point* getcurve1() {
  return curve1;
}

/*! \fn point* getcurve2()
*/
point* getcurve2() {
  return curve2;
}

/*! \fn int getcurve1lenght()
*/
int getcurve1lenght() {
  return no1;
}

/*! \fn int getcurve2lenght()
*/
int getcurve2lenght() {
  return no2;
}
