#include <stdio.h>
#include <conio.h>

#define WHERE_MARCO1 printf("in file %s , use WHERE_MARCO1 at line %d\n", __FILE__, __LINE__);
#define WHERE_MACRO2 printf("in file %s , use WHERE_MARCO2 at line %d\n", __FILE__, __LINE__);

int main()
{
    //clrscr();
    WHERE_MARCO1;
    WHERE_MACRO2;
    printf("Print this result in %s\n", __DATE__);
    getch();
}
