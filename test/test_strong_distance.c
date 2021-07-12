/*  This programs tests the functionality of the strong frechet c source code.

      Running test File
      ---------------------
      Compile terminal line command:
      gcc -o test_strong_distance test_strong_distance.c -lm

      Run terminal line command:
      ./test_strong_distance

    Author: Will Rodman
    wrodman@tulane.edu
*/
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "../src/frechet/strong_distance.c"

int main(int argc, char *argv[]) {
  char *curve2filename = "test_curve_1.txt";
  char *curve1filename = "test_curve_2.txt";

  // tests if weak frechet distance functions can find path inside free space
  // the minimum epsilon for the test curves is ~67.5
  printf("TESTING 'strong_distance.c':\n");

  createcurves(curve1filename, curve2filename, true);
  create_freespace_reachabilitytable();

  setfreespace(60);
  setreachabilitytable();
  if(isreachable() == false) {
    printf("    TEST -- PASSED: Eplison 60 was un reachable\n");
  } else {
    printf("    TEST -- FAILED: Eplison 60 was reachable\n");
  }

  setfreespace(70);
  setreachabilitytable();
  if(isreachable() == true) {
    printf("    TEST -- PASSED: Eplison 70 was reachable\n");
  } else {
    printf("    TEST -- FAILED: Eplison 70 was us reachable\n");
  }
  return 0;
}
