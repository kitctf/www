#include<stdio.h>

#define SIZE 20

int main(int argc, char* argv[]) {  	
    char buf[SIZE];
    fgets(buf, SIZE, stdin);
    printf(buf);
	return 0;
}
