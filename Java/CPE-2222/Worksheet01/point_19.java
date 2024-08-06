
import java.util.Scanner;

public class point_19 {

    public static void main(String[] args) {
        Scanner keyborad = new Scanner(System.in);

        int s = 0;
        int i = 0;

        System.out.print("n = ");
        int n = keyborad.nextInt();

        while (i <= n) {
            if (i % 2 == 0) s += i;
            i += 1;
        }
        System.out.println(s);
    }
}
