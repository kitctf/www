#include<stdio.h>
void getBuffer() {
    char buf[80];
    gets(buf);
    //register int i asm("esp");
    //printf("$esp = %#010x\n", i);
}
int main(int argc, char* argv[]) {  	
    getBuffer();
	return 0;
}
/*#include <stdio.h>
void main() {
        register int i asm("esp");
        printf("$esp = %#010x\n", i);
}*/
