#include <stdio.h>

int convert(int x[]);

int main()
{
   int i = 0, num;
   int b[8] = {0};

   printf("\n\tEnter your number: ");
   scanf("%d", &num);

   while (num != 0)
   {
      b[i] = num % 8;
      num /= 8;
      i++;
   }
   convert(num);

   printf("\n\tEnter your number: ");
   scanf("%d", &num);

   return 0;
}

int convert(int x[]){
   int i = 0;
   for (i = 7; i >= 0; i--)
      printf("\t%d", x[i]);
}