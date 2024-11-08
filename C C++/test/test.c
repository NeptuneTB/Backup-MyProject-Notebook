#include <stdio.h>

#define WHERE_MARCO1 printf("in file %s , use WHERE_MARCO1 at line %d\n", __FILE_NAME__, __LINE__);
#define WHERE_MACRO2 printf("in file %s , use WHERE_MACRO2 at line %d\n", __FILE_NAME__, __LINE__);

int main()
{
    WHERE_MARCO1;
    WHERE_MACRO2;
    printf("Print this result in %s\n", __DATE__);
    return 0;
}