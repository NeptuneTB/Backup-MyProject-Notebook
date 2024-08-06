
public class IncrementDecrement {

    public static void main(String[] args) {
        int number = 4;

        System.out.println("number is " + number);
        System.out.println("I will increment number.");

        int x = number++ + 100;
        System.out.println("x = " + x);

        System.out.println("Now, number is " + number);
        System.out.println("I will decrement number.");

        int y = 100 + number--;
        System.out.println("y = " + y);
        System.out.println("Now, number is " + number);
    }
}
