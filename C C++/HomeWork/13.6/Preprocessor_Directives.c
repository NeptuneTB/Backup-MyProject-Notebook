#include <stdio.h>
#include <string.h>

#define A 5

int main()
{
    #ifdef A
        #undef A
        #define A printf("This is Macro A\n");
        A;
    #endif
    #ifndef B
        #define B "HELLO!!!"
        char greeting[9];
        strcpy(greeting, B);
    #else
        #define A printf("This is Macro A\n")
        A;
        #define B printf("This is Macro B\n")
        B;
    #endif

    printf("%s\n", greeting);
    printf("End processing Macro\n");
    return 0;
}
