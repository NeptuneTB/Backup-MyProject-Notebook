#include <stdio.h>

void reverse(char *value, char *reversed)
{
   int k = 0;

   while (value[k] != '\0')
   {
      k++;
   }

   int m, n;
   for (m = k - 1, n = 0; m >= 0; n++, m--)
   {
      reversed[n] = value[m];
   }
   reversed[n] = '\n';
}

void Convert_Base_Number(int number, int base)
{
   char answer[100];
   int index = 0;

   while (number > 0)
   {
      int result = number % base;

      if (result < 10)
         answer[index++] = 48 + result;
      else
         answer[index++] = 55 + result;
      number /= base;
   }
   answer[index] = '\0';

   char reversed[100];
   reverse(answer, reversed);

   printf("Converted Number: %s\n", reversed);
}

int main()
{
   int number, base;

   printf("Enter Number: ");
   scanf("%d", &number);

   printf("Enter Base Number: ");
   scanf("%d", &base);

   Convert_Base_Number(number, base);

   return 0;
}
