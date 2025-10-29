#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define streq(a, b) (!(strcmp((a), (b))))

void die(const char * message) {
	fprintf(stderr, "%s\n", message);
	exit(1);
}

int count_score(const char * buffer) {
	int score = 0;
	switch (buffer[2]) {
		case 'X': score += 0; score += 1 + ((3 + buffer[0] - 'A' - 1) % 3); break;
		case 'Y': score += 3; score += 1 + ((3 + buffer[0] - 'A' - 0) % 3); break;
		case 'Z': score += 6; score += 1 + ((3 + buffer[0] - 'A' - 2) % 3); break;
	}
	return score;
}

int main(void) {
	FILE * fp;
	int buffer_len = 255;
	char buffer[buffer_len];
	unsigned int score = 0;

	fp = fopen("input", "r");
	if (fp == NULL) exit(1);

	while (fgets(buffer, buffer_len, fp)) {
		score += count_score(buffer);
	}
	// printf("%i %i %i\n", 'X' - 'A', 'Y' - 'B', 'Z' - 'C');
	// printf("%i %i %i\n", 'X' - 'C', 'Y' - 'A', 'Z' - 'B');
	// printf("%i %i %i\n", 'X' - 'B', 'Y' - 'C', 'Z' - 'A');
	// printf("%s: %i\n", "A X", count_score("A X"));
	// printf("%s: %i\n", "A Y", count_score("A Y"));
	// printf("%s: %i\n", "A Z", count_score("A Z"));
	// printf("%s: %i\n", "B X", count_score("B X"));
	// printf("%s: %i\n", "B Y", count_score("B Y"));
	// printf("%s: %i\n", "B Z", count_score("B Z"));
	// printf("%s: %i\n", "C X", count_score("C X"));
	// printf("%s: %i\n", "C Y", count_score("C Y"));
	// printf("%s: %i\n", "C Z", count_score("C Z"));
	printf("%i\n", score);
}

// 17570 too high

// A X
// B Y
// C Z

// X=0 Y=3 Z=6
// AX=3
// AY=1
// AZ=2

// BX=1
// BY=2
// BZ=3

// CX=2
// CY=3
// CZ=1



// AY=BZ=CX=6
// AZ=BX=CY=0
