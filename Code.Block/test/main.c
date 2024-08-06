#include <stdio.h>
#include <conio.h>
#define A 5

#ifndef A
    #undef A
    #define A printf("This is Macro A\n");
    int main(){
        clrscr();
        A;
#else
    #ifndef B
    #define B printf("This is Macro B\n");
    int main(){
        clrscr();
        B;
#endif
printf("End processing Macro\n");
getch();
}
