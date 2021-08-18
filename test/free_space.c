/*  Author: Will Rodman
    wrodman@tulane.edu

      Running test File:
      ==================
      Compile terminal line command:
      gcc -o dumps/free_space free_space.c -lm

      Run terminal line command:
      ./dumbs/free_space
*/

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "../pyfrechet/strong_distance.c"

char TEST_DATA[] = "sp500";
bool REVERSE_CURVE = false
unsigned int SAMPLE_SIZE = 5;

int main(int argc, char *argv[]) {

  char curve1filename[64];
  strcpy(curve1filename, TEST_DATA);
  strcpy(curve1filename, "_data/sample_1.txt");

  char curve2filename[64];
  strcpy(curve2filename, TEST_DATA);
  strcpy(curve2filename, "_data/sample_1.txt");

  printf("Testing Free Space Data Structure:\n");
  printf("==================================\n");

  createcurves(curve1filename, curve2filename, REVERSE_CURVE);
  create_freespace_reachabilitytable();
  setfreespace(100);

  int v1 = gethorizontaledges();
  int v2 = getverticaledges();
  freespace fs = getfreespace();

  printf("  Horizontal verticies: %d\n", v1);
  printf("  Vertical verticies: %d\n", v2);
  printf("--------------------------\n\n");

  for(int i = SAMPLE_SIZE; i < v1; i++) {
    for(int j = SAMPLE_SIZE; j < v2; j++) {
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
