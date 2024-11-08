
import java.util.Scanner;

public class point_22 {
    public static void main(String[] args) {
        Scanner keyborad = new Scanner(System.in);

        System.out.print("n = ");
        int n = keyborad.nextInt();

        int s = 0;
        int i = 0;

        while (i <= n) {
            int j = 0;

            while (j <= n) {
                s += 1;
                j += 1;
            }
            i += 1;
        }
        System.out.println(s);
    }
}
