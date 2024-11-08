#include <stdio.h>
#include <string.h>

#define WHERE_MACRO1 printf("in file %s , use WHERE_MACRO1 at line %d\n", __FILE__, __LINE__);
#define WHERE_MACRO2 printf("in file %s , use WHERE_MACRO2 at line %d\n", __FILE__, __LINE__);

int main()
{
    WHERE_MACRO1;
    WHERE_MACRO2;
    printf("Print this result in %s\n", __DATE__);
    return 0;
}
