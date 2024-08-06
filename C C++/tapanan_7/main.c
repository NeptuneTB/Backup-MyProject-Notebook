#include <stdio.h>
#include <conio.h>

int main()
{
    /* int count = 0;
    printf("Show even 0-100\n\n");   
    while (count <= 100)
    {
        if (count%2 != 0)
        {
            printf("%d\t", count);
        }
        count++;
    } */
    
    /* int vowel = 0, alphabet = 0, count;
    char letter;
    for (count = 0; count < 10; count++)
    {
        printf("\nEnter letter a-z = ");
        letter = getche();

        if ((letter == 'a') || (letter == 'e') || (letter == 'i') || (letter == 'o') || (letter == 'u'))
            vowel++;
        else
            alphabet++;

    }
    printf("\n*****************Result*****************\n");
    printf("Vowel (a,e,i,o,u) = %d\n", vowel);
    printf("Other letter = %d", alphabet); */

    int num, i, j;
    char space = ' ';
    printf("Enter number = ");
    scanf("%d", &num);
    for (i = 1; i <= num; i++)
    {
        printf("\n");

        for (j = 1; j <= num; j++)
        {
            if (i == 1 || i == num || j == 1 || j == num)
                printf("*");
            else
                printf("%c", space);            
        }
        
    }
    

}