#include <stdio.h>

#define TEST1 2
#define TEST2 3*TEST1
int times = 11, result;

int main()
{
    #if TEST1
        result = TEST1*times;
        printf("Value of Macro TEST1 is %d ===> %d x %d times\n", TEST1, TEST1, times);
    #elif TEST2
        result = TEST2*times;
        printf("Value of Macro TEST2 is %d ===> %d x %d times\n", TEST2, TEST2, times);
    #else
        result = 0;
    #endif

    if(result == 0) {
        printf("NOT DEFINE MACRO TEST1 & TEST2\n");
    }
    else {
        printf("Result in %d\n", result);
    }
    return 0;
}
