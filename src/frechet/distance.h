/*! \file distance.h
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

/*! \def DISTANCE_H
    \breif Defines distance header if undefined.
*/
#ifndef DISTANCE_H
#define DISTANCE_H

/*! \include <stdbool.h>
*/
#include <stdbool.h>

/*! \struct typedef struct point
    \breif Structure of (long, lat) coordinates for curves.
*/
typedef struct point point;

struct point {
  double x, y;
};

/*! \struct typedef struct freespace
*/
typedef struct freespace freespace;

struct freespace {
  double **vertical_start;
  double **vertical_end;
  double **horizontal_start;
  double **horizontal_end;
};

/*! \var point *curve1
    \brief Array of coordinates for first curve.

    \var point *curve2
    \brief Array of coordinates for second curve.

    \var point *curvetmp
    \brief Array of coordinates temorarily used if second curve
    must be reversed.
*/
extern point *curve1;
extern point *curve2;
extern point *curvetmp;

/*! \var int no1
    \brief Number of vertices for first curve.

    \var int no2
    \brief Number of vertices for second curve.
*/
extern int no1, no2;

/*! \var double **vFSs
    \brief Vertical free space diagram start.

    \var double **vFSe
    \brief Vertical free space diagram end.

    \var double **hFSs
    \brief Horizontal free space diagram start.

    \var double **hFSe
    \brief Horizontal free space diagram end.
*/
extern double **vFSs;
extern double **vFSe;
extern double **hFSs;
extern double **hFSe;

/*! \var double **vRTs
    \brief Vertical reachability table start.

    \var double **vRTe
    \brief Vertical reachability table end.

    \var double **hRTs
    \brief Horizontal reachability table start.

    \var double **hRTe
    \brief Horizontal reachability table end.
*/
extern double **vRTs;
extern double **vRTe;
extern double **hRTs;
extern double **hRTe;

/*! \fn int createcurves(char* curve1filename, char* curve2filename,
    bool reversecurve2)
    \brief
    Reads data from the two input files and stores it to curve point arrays.
    \param curve1filename Filename of first curve.
    \param curve2filename Filename of second curve.
    \param reversecurve2 true agurment if second curve must be reversed.
    \return 0 if fopen() and fscanf() succeed
    \return errno if fopen() or fscanf() fail
*/
int createcurves(char* curve1filename, char* curve2filename, \
                  bool reversecurve2);

/*! \fn void create_freespace_reachabilitytable()
    \brief Allocates memory for free space diagram and reachability table.
*/
void create_freespace_reachabilitytable();

/*! \fn void calculatefreespace(double &x1, double &y1, double &x2, double &y2,
    double &xa, double &ya, double &start, double &end, double epsilon)
    \brief
    Input: A line segment starting in (x1, y1) and ending in (x2,y2) for a
    point (xa, ya).

    Output: The two points on the boundary of the free space diagram: start,
    end. Hopefully start and end lie between 0 and 1. This should be checked!
    \param &x1
    \param &y1
    \param &x2
    \param &y2
    \param &xa
    \param &ya
    \param &start
    \param &end
    \param epsilon Maximum distance between both curves. Represented by
    bounderies inside free space diagram.
*/
void calculatefreespace(double x1, double y1, double x2, double y2, \
                        double xa, double ya, double *start, double *end, \
                        double epsilon);

/*! \fn void setfreespace(double epsilon)
    \brief Calculates the the bounderies of free space diagram.
    \param epsilon Maximum distance between both curves. Represented by
    bounderies inside free space diagram (this arument will be only be used
    as an arugment to calculate free space)
    \sa calculatefreespace()
*/
void setfreespace(double epsilon);

/*! \fn freespace getfreespace()
*/
freespace getfreespace();

/*! \fn point* getcurve1()
*/
point* getcurve1();

/*! \fn point* getcurve2()
*/
point* getcurve2();

/*! \fn int getcurve1lenght()
*/
int getcurve1lenght();

/*! \fn int getcurve2lenght()
*/
int getcurve2lenght();

/*! \fn bool isreachable()
    \brief
    Checks to see if a path exists from bottom left to top right of free space
    diagram. Strong Frechet metric only checks for a monotone path. Weak
    Frechet metric checks for any non-monotone path.
    \return true A path exists for epsilon.
    \return flase No path was found for epsilon.
*/
bool isreachable();

#endif
