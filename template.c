///usr/bin/env gcc ${0} -o ${0%%.c} -O3 && ./${0%%.c} && exit 0
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

	fp = fopen("input", "r");
	if (fp == NULL) exit(1);

	while (fgets(buffer, buffer_len, fp)) {

	}
}
