#include <stdio.h>

int main()
{
    int num, main;
    // int i = 1, final;
    // int count, sum = 0;
    // char letter;
    /* printf("Show 0-100\n");

    while (count <= 100)
    {
        printf("%d\t", count);
        count++;
        
    }
    
    printf("Enter final = ");
    scanf("%d", &final);

    while (i <= final)
    {
        sum = sum + i;
        i++;
    }
    printf("Sum = %d", sum); */

    /* do
    {
        sum = sum + count;
        count++;
    } while (count <= 100);
    printf("Sum 1-100 = %d", sum); */

    /* for (count = 0; count <= 100; count++)
    {
        sum = sum + count;
    }
    printf("Sum = %d", sum); */
    
    /* for (letter = 'a'; letter <= 'z'; letter++)
    {
        printf("%c\t", letter);

        if (letter == 'p')
        {
            printf("\n");
        }
        
    } */

    printf("Multiplication table = ");
    scanf("%d", &main);    
    for (num = 1; num <= 12; num++)
    {
        printf("%5d * %-2d = %-3d\n", main, num, main*num);
    }
    printf("\n");
    printf("Multiplication table = ");
    scanf("%d", &main);
    for (num = 1; num <= 12; num++)
    {
        printf("%5d * %-2d = %-3d\n", main, num, main * num);
    }
}