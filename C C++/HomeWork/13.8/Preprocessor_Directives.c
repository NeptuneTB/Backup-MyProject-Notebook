#include <stdio.h>

#define A 1

int main()
{
    #if A == 0
        char language[4] = "THA";
    #else
        char language[4] = "ENG";
    #endif

    printf("Flag A is %d , Language is %s\n", A, language);
    return 0;
}
