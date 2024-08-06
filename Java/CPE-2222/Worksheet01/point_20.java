import java.util.Scanner;

public class point_20 {
    public static void main(String[] args) {
        Scanner keyborad = new Scanner(System.in);

        int s = 0;
        int i = 1;

        System.out.print("n = ");
        int n = keyborad.nextInt();

        while (i <= n) {
            if (i % 3 == 0) s += i;
            i += 1;
        }
        System.out.println(s);
    }
}
