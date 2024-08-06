#include <stdio.h>
#include <stdlib.h>

int i;

int main()
{
    printf("Sum = %d\n", 10+20+30);
    printf("GPA = %f\n", 3.78);
    printf("Grade = %c\n", 'A');
    printf("My name = %s\n", "tapanan");
    printf("Sum = %d\nGPA = %f\nGrade = %c\nMy name = %s\n", 10+20+30, 3.78, 'A', "tapanan");
    printf("%10d*\n", 46);
    printf("%-10d*\n", 46);
    printf("%20c*\n", 'A');
    printf("%-20c*\n", 'A');
    printf("%20s*\n", "tapanan");
    printf("%-20s*\n", "tapanan");
    printf("%.3s\n", "Google");
    printf("%20.3s*\n", "Google");
    printf("%-20.3s*\n", "Google");
    printf("%.3f\n", 12.3456789);
    printf("%20.3f*\n", 12.3456789);
    printf("%-20.3f*\n", 12.3456789);
}
