/*  Author: Will Rodman
    wrodman@tulane.edu

      Running test File
      ---------------------
      Compile terminal line command:
      gcc -o dumps/weak_distance weak_distance.c -lm

      Run terminal line command:
      ./dumps/weak_distance
*/
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "../pyfrechet/weak_distance.c"

char TEST_DATA[] = "sp500";

int main(int argc, char *argv[]) {

  if(TEST_DATA == "sp500") {
    double REACHABLE_EPSILON = 5
    double UNREACHABLE_EPSILON = 0.5
    bool REVERSE_CURVE = false

  } elif(TEST_DATA == "trajectory") {
    double REACHABLE_EPSILON = 70
    double UNREACHABLE_EPSILON = 60
    bool REVERSE_CURVE = true
  }

  char curve1filename[64];
  strcpy(curve1filename, TEST_DATA);
  strcpy(curve1filename, "_data/sample_1.txt");

  char curve2filename[64];
  strcpy(curve2filename, TEST_DATA);
  strcpy(curve2filename, "_data/sample_1.txt");

  printf("TESTING 'weak_distance.c':\n");

  createcurves(curve1filename, curve2filename, true);
  create_freespace_reachabilitytable();

  if(no1 == 1 || no2 == 1) {
    if(computemaxdistances(UNREACHABLE_EPSILON) == false) {
      printf("    TEST -- PASSED: Eplison 60 was un reachable\n");
    } else {
      printf("    TEST -- FAILED: Eplison 60 was reachable\n");
    }

    if(computemaxdistances(REACHABLE_EPSILON) == true) {
      printf("    TEST -- PASSED: Eplison 70 was reachable\n");
    } else {
      printf("    TEST -- FAILED: Eplison 70 was us reachable\n");
    }

    } else {
      setfreespace(UNREACHABLE_EPSILON);
      if(isreachable() == false) {
        printf("    TEST -- PASSED: Eplison 60 was un reachable\n");
      } else {
        printf("    TEST -- FAILED: Eplison 60 was reachable\n");
      }

      setfreespace(REACHABLE_EPSILON);
      if(isreachable() == true) {
        printf("    TEST -- PASSED: Eplison 70 was reachable\n");
      } else {
        printf("    TEST -- FAILED: Eplison 70 was us reachable\n");
      }
  	}
  	return 0;
}
