
import java.util.Scanner;

public class point_14_to_17 {
    public static void main(String[] args) {
        Scanner keyborad = new Scanner(System.in);

        System.out.print("a = ");
        int a = keyborad.nextInt();

        System.out.print("b = ");
        int b = keyborad.nextInt();

        System.out.print("c = ");
        int c = keyborad.nextInt();

        System.out.print("d = ");
        int d = keyborad.nextInt();

        if (a <= b) {
            if (c >= d) System.out.println("Bird");
            else System.out.println("Ant");
        } else {
            if (c <= d) System.out.println("Dog");
            else System.out.println("Cat");
        }
    }
}
