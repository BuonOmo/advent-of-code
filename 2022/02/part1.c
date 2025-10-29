#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define streq(a, b) (!(strcmp((a), (b))))

void die(const char * message) {
	fprintf(stderr, "%s\n", message);
	exit(1);
}

int main(void) {
	FILE * fp;
	int buffer_len = 255;
	char buffer[buffer_len];
	unsigned int score = 0;

	fp = fopen("input", "r");
	if (fp == NULL) exit(1);

	while (fgets(buffer, buffer_len, fp)) {

		switch (buffer[2]) {
			case 'X': score += 1; break;
			case 'Y': score += 2; break;
			case 'Z': score += 3; break;
		}

		switch (buffer[2] - buffer[0]) {
			case 23: score += 3; break;
			case 21: case 24: score += 6; break;
			case 22: case 25: score += 0; break;

		}
	}
	// printf("%i %i %i\n", 'X' - 'A', 'Y' - 'B', 'Z' - 'C');
	// printf("%i %i %i\n", 'X' - 'C', 'Y' - 'A', 'Z' - 'B');
	// printf("%i %i %i\n", 'X' - 'B', 'Y' - 'C', 'Z' - 'A');
	printf("%i\n", score);
}

// A X
// B Y
// C Z

// X=1 Y=2 Z=3
// AX=BY=CZ=3
// AY=BZ=CX=6
// AZ=BX=CY=0
