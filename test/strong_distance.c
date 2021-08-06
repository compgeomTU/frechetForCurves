/*  Author: Will Rodman
    wrodman@tulane.edu

      Running test File
      ---------------------
      Compile terminal line command:
      gcc -o dumps/strong_distance strong_distance.c -lm

      Run terminal line command:
      ./dumps/strong_distance
*/
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "../src/frechet/strong_distance.c"

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

  printf("TESTING 'strong_distance.c':\n");

  createcurves(curve1filename, curve2filename, REVERSE_CURVE);
  create_freespace_reachabilitytable();

  setfreespace(UNREACHABLE_EPSILON);
  setreachabilitytable();
  if(isreachable() == false) {
    printf("    TEST -- PASSED: Eplison 60 was un reachable\n");
  } else {
    printf("    TEST -- FAILED: Eplison 60 was reachable\n");
  }

  setfreespace(REACHABLE_EPSILON);
  setreachabilitytable();
  if(isreachable() == true) {
    printf("    TEST -- PASSED: Eplison 70 was reachable\n");
  } else {
    printf("    TEST -- FAILED: Eplison 70 was us reachable\n");
  }
  return 0;
}
