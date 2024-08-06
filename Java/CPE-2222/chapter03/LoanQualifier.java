
import javax.swing.JOptionPane;

public class LoanQualifier {

    public static void main(String[] args) {
        double salary;
        double yearsOnJob;
        String input;

        input = JOptionPane.showInputDialog("Enter your " + "annual salary.");
        salary = Double.parseDouble(input);

        input = JOptionPane.showInputDialog("Enter the number of " + "years at your curreant job.");
        yearsOnJob = Double.parseDouble(input);

        if (salary >= 30000 && yearsOnJob >= 2) {
            JOptionPane.showMessageDialog(null, "You qualify " + "for the loan");
        } else {
            JOptionPane.showMessageDialog(null, "You must loan " + "at least $30,000 per year to qualify.");
        }
        System.exit(0);
    }
}
