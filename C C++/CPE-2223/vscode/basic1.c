#include <stdio.h>

int main()
{
   int i = 0, num;
   int b[8] = {0};

   printf("\n\tEnter your number: ");
   scanf("%d", &num);

   while (num != 0) {
      b[i] = num % 16;
      num /= 16;
      i++;
   }

   for (i = 7; i >= 0; i--)
      if (b[i] == 10)
         printf("A");
      else if (b[i] == 11)
         printf("B");
      else if (b[i] == 12)
         printf("C");
      else if (b[i] == 13)
         printf("D");
      else if (b[i] == 14)
         printf("E");
      else if (b[i] == 15)
         printf("F");
      else
         printf("\t%d", b[i]);

   printf("\n\tEnter your number: ");
   scanf("%d", &num);

   return 0;
}
