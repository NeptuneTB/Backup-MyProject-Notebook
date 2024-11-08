#include <string.h>
#include <stdio.h>

int main()
{
   int i = 0, n;
   char x[50];
   printf("Enter your message: ");
   getc(x);

   printf("Your message is: %s", x);
   
   while (x[i] != '\0')
   {
      i++;
      n=i;
   }
   
   printf("Length of string is: %d", n);

   return 0;
}
