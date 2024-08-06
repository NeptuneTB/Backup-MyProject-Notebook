
import java.util.Scanner;

public class point_3 {
   public static void main(String[] args) {
       Scanner keyboard = new Scanner(System.in);

       System.out.print("a = ");
       int a = keyboard.nextInt();

       int b = a * a + 5;

      if (a >= 4) {
         if (b >= 32) System.out.println("large a, large b");
         else System.out.println("large a, small b");
      } else {
         if (b >= 32) System.out.println("small a, large b");
         else System.out.println("small a, small b");
      }

   }
}
