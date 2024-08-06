#include <stdio.h>

int main()
{
    /* float num1, num2;
    printf("Enter num1 = ");
    scanf("%f", &num1);
    printf("Enter num2 = ");
    scanf("%f", &num2);

    if (num2 != 0)
    {
        printf("%.2f/%.2f = %.2f", num1, num2, num1 / num2);
    }
    else
    {
        printf("Error\n");
    } */

    /* float score;
    printf("Enter score = ");
    scanf("%f", &score);

    if (score < 50)
        printf("Grade = F");
    else if (score < 60)
        printf("Grade = D");
    else if (score < 70)
        printf("Grade = C");
    else if (score < 80)
        printf("Grade = B");
    else
        printf("Grade = A"); */

    int d;
    printf("Enter 1-9 = ");
    scanf("%d", &d);

    switch (d)
    {
        case 1:
            puts("Hi RMUTR");
            break;
        case 2:
            puts("HI CPE");
            break;
        case 3:
        case 5:
        case 6:
            puts("Hi CVE");
            break;
        default:
            puts("Try again");
            break;
    }


    return(0);
}