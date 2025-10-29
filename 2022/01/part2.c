#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define streq(a, b) (!(strcmp((a), (b))))

void die(const char * message) {
	fprintf(stderr, "%s\n", message);
	exit(1);
}

int compare_ints(const void* a, const void* b)
{
    int arg1 = *(const int*)a;
    int arg2 = *(const int*)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

void insert(int sum, int top[3]) {
	top[0] = sum;
	qsort(top, 3, sizeof(int), compare_ints);
}

int main(void) {
	FILE * fp;
	int buffer_len = 255;
	char buffer[buffer_len];
	int sum = 0;
	int top[3] = {0, 0, 0};

	fp = fopen("input", "r");
	if (fp == NULL) exit(1);

	while (fgets(buffer, buffer_len, fp)) {
		if (streq(buffer, "\n")) {
			if (sum >= top[0]) insert(sum, top);
			sum = 0;
		}
		sum += atoi(buffer);
	}
	printf("%i\n", top[0] + top[1] + top[2]);
}
