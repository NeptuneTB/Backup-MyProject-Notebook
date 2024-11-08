#include <stdio.h>

#define MAX(x, y) ((x) > (y) ? (x) : (y))
#define MAX_MIN(x, y) {                        \
    if (x > y)                                 \
        printf("MAX : %d , MIN : %d\n", x, y); \
    else                                       \
        printf("MAX : %d , MIN : %d\n", y ,x); \
}

int main()
{
    int x = 5, y = 8, max;
    max = MAX(x, y);
    printf("max value from macro MAX is %d\n", max);
    MAX_MIN(x, y);
}
