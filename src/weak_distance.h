/*! \file weak_distance.h
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

/*! \def weak_distance_H
    \breif Defines weak distance header if undefined.
*/
#ifndef WEAK_DISTANCE_H
#define WEAK_DISTANCE_H

#include <stdbool.h>

/*! \struct typedef struct DFS
		\brief
		If horizontal
		=============
		0 <= i < totalvertex\n
		0 <= j < noofgpsvertices - 1\n
		If vertical
		===========
		0 <= i < totaledges\n
		0 <= j < noofgpsvertices\n
*/
typedef struct {
	int interval; //!< Interval Value of 0 = horizontal while 1 = vertical.
	int i; //!< Index into vertices, if horizontal interval. Index into edges, if vertical interval.
	int j; //!< Index into vertices[i].FS, if horizontal interval. Index into edges[i].FS, if vertical interval.\n
} DFS;

/*! \var int **vColor
		\brief Vertical interval color.

		\var **hColor
		\brief Horizontal interval color.
*/
extern int **vColor;
extern int **hColor;

/*! \var DFS **vReachedFrom
		\brief Predecessor pointers for vertical intervals.

		\var DFS **hReachedFrom
		\brief Predecessor pointers for horizontal intervals.

		\var bool FSfound
		\brief Global variable that declares if a path for epsilon has been found.
		\sa ispath_visit()
		\sa ispath()
*/
extern DFS **vReachedFrom;
extern DFS **hReachedFrom;
extern bool FSfound;

/*! \var int lastI
		\sa ispath_visit()

		\var int lastJ
		\sa ispath_visit()

		\var int lastInterval
		\sa ispath_visit()
*/
extern int lastI;
extern int lastJ;
extern int lastInterval;

/*! \fn isreachable_visit(int currentI, int currentJ, int currentInterval)
    \brief Recursive function that supports ispath().
		\param currentI
		\param currentJ
		\param currentInterval
		\sa ispath()
*/
void isreachable_visit(int currentI, int currentJ, int currentInterval);

/*! \fn bool computemaxdistances(double epsilon)
    \brief Check if path exists for path epsilon if a curve only contains
		one vertice.
		\param epsilon Maximum distance between both curves. Represented by
    bounderies inside free space diagram.
*/
bool computemaxdistances(double epsilon);

#endif
