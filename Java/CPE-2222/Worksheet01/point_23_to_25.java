import java.util.Scanner;

public class point_23_to_25 {
    public static void main(String[] args) {
        Scanner keyborad = new Scanner(System.in);

        System.out.print("a = ");
        int a = keyborad.nextInt();

        System.out.print("b = ");
        int b = keyborad.nextInt();

        System.out.print("c = ");
        int c = keyborad.nextInt();

        int d = a + b + c;

        if (d >= 80) System.out.println("A"); 
        else if (d >= 75) System.out.println("B+"); 
        else if (d >= 70) System.out.println("B"); 
        else if (d >= 65) System.out.println("C+"); 
        else if (d >= 60) System.out.println("C"); 
        else if (d >= 55) System.out.println("D+"); 
        else if (d >= 50) System.out.println("D"); 
        else System.out.println("F");
    }
}
