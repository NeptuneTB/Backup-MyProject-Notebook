#include <stdio.h>

#define PT 3.14
#define TIMES 2
#define ROUNDS 3*TIMES
#define ADD (2 + 1 + a)
#define ADD1 2 + 1 + a

int main()
{
    int a = 3, result, result1;
    printf("Value of Macro PT is %f\n", PT);
    printf("Value of Macro TIMES is %d\n", TIMES);
    printf("Value of Macro ROUNDS is %d\n", ROUNDS);
    printf("Value of Macro ADD (2+1+%d) is %d\n", a, ADD);
    result = 5 * ADD;
    result1 = 5 * ADD1;
    printf("Result is %d\n", result);
    printf("Result1 is %d\n", result1);
}
