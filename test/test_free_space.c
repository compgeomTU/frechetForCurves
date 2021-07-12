/*

      Running test File
      ---------------------
      Compile terminal line command:
      gcc -o test_free_space test_free_space.c -lm

      Run terminal line command:
      ./test_free_space

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

  printf("TESTING -- Free Space\n\n");

  createcurves(curve1filename, curve2filename, true);
  create_freespace_reachabilitytable();
  setfreespace(100);

  int v1 = gethorizontaledges();
  int v2 = getverticaledges();
  freespace fs = getfreespace();

  printf("  Horizontal verticies: %d\n", v1);
  printf("  Vertical verticies: %d\n", v2);
  printf("--------------------------\n\n");

  for(int i = 1; i < v1; i++) {
    for(int j = 1; j < v2; j++) {
      printf("\n\n  Cell at (%d , %d):\n\n", i, j);

      printf(
        "       %.2lf       %.2lf       \n"
        "\n"
        "%.2lf                     %.2lf\n"
        "\n"
        "%.2lf                     %.2lf\n"
        "\n"
        "       %.2lf       %.2lf       \n",
        fs.vertical_start[i+1][j+1],
        fs.vertical_end[i+1][j+1],
        fs.horizontal_end[i][j],
        fs.horizontal_end[i+1][j+1],
        fs.horizontal_start[i][j],
        fs.horizontal_start[i+1][j+1],
        fs.vertical_start[i][j],
        fs.vertical_end[i][j]);
    }
  }
  return 0;
}
