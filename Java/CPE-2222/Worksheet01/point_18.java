import java.util.Scanner;

public class point_18 {
    public static void main(String[] args) {
        Scanner keyborad = new Scanner(System.in);

        int s = 0;

        System.out.print("n = ");
        int n = keyborad.nextInt();

        int i = n;

        while (i >= 0) {
            s += i;
            i -= 2;
        }
        System.out.println(s);
    }
}
