import javax.swing.JOptionPane;

public class AverageScore {

    public static void main(String[] args) {
        double score1;
        double score2;
        double score3;
        double average;
        String input;

        input = JOptionPane.showInputDialog("Enter score #1:");
        score1 = Double.parseDouble(input);

        input = JOptionPane.showInputDialog("Enter score #2:");
        score2 = Double.parseDouble(input);

        input = JOptionPane.showInputDialog("Enter score #3:");
        score3 = Double.parseDouble(input);

        average = (score1 + score2 + score3);

        JOptionPane.showMessageDialog(null, "The average is " + average);

        if (average > 95)
            JOptionPane.showMessageDialog(null, "That's a great score!");
        System.exit(0);

    }

}
