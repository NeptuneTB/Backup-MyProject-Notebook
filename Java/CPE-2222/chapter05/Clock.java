
import java.text.DecimalFormat;

public class Clock {
    public static void main(String[] args) {
        DecimalFormat fmt = new DecimalFormat("00");

        for (int hours = 1; hours <= 12; hours++) {
            for (int minutes = 0; minutes <= 59; minutes++) {
                for (int seconds = 0; seconds <= 59; seconds++) {
                    try {
                        if (System.getProperty("os.name").contains("Windows")) {
                            new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
                        } else {
                            new ProcessBuilder("clear").inheritIO().start().waitFor();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }

                    System.out.print(fmt.format(hours) + ":");
                    System.out.print(fmt.format(minutes) + ":");
                    System.out.println(fmt.format(seconds));

                    // try {
                    //     Thread.sleep(1000);
                    // } catch (InterruptedException e) {
                    //     e.printStackTrace();
                    // }
                }
            }
        }
    }
}
