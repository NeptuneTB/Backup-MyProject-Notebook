import java.util.Scanner;

public class point_4 {
   public static void main(String[] args) {
       Scanner keyboard = new Scanner(System.in);

       System.out.print("a = ");
       int a = keyboard.nextInt();

       int b = a * a + 16;

       if (a >= 5) {
           if (b >= 15) {
               System.out.println("large a, large b"); 
           }else {
               System.out.println("large a, small b");
           }
       } else {
           if (b >= 15) {
               System.out.println("small a, large b"); 
           }else {
               System.out.println("small a, small b");
           }
       }
   }
}