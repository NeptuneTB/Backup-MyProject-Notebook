#include <stdio.h>

int main()
{
    float g = 3.5;
    float a = 3.7;
    float point;
    char name1[30];
    char ch = 'A', str[] = "Computer";
    char name[20] = "tapanan";
    putchar(ch);
    putchar(' ');
    putchar(str[7]);
    putchar('\n');
    puts(str);
    printf("GPA = %.2f\n", g);
    printf("GPA = %.2f\n", g);
    printf("GPA = %.2f\n", a);
    printf("%s\n", name);
    printf("%s\n", name);
    printf("%s\n%s\n", name, name);
    printf("Enter name = ");
    scanf("%s", name1);
    printf("Enter point = ");
    scanf("%f", &point);
    printf("\nYour name = %s\nYour point = %.2f\n", name1, point);

}
