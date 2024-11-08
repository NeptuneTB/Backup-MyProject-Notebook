import java.util.Scanner;

public class point_29 {
    public static void main(String[] args) {
        Scanner keyborad = new Scanner(System.in);

        System.out.print("n = ");
        int n = keyborad.nextInt();

        System.out.print("m = ");
        int m = keyborad.nextInt();

        int s = 0;
        int i = 0;

        while (i <= n) {
            int j = 0;

            while (j <= m) {
                if (i > j) s += j;
                j += 1;
            }
            i += 1;
        }
        System.out.println(s); 
    }
}
