
import java.io.*;
import java.util.Scanner;

public class FileWriteDemo {
    public static void main(String[] args) throws IOException {
        String filename;
        String friendName;
        int numFriends;

        Scanner keyborad = new Scanner(System.in);

        System.out.print("How many friends do you have?: ");
        numFriends = keyborad.nextInt();
        keyborad.nextLine();

        System.out.print("Enter the filename: ");
        filename = keyborad.nextLine();

        FileWriter fWriter = new FileWriter(filename);
        PrintWriter outputFile = new PrintWriter(fWriter);

        for (int i = 1; i <= numFriends; i++) {
            System.out.print("Enter the name of  friend " + "number " + i + "");
            friendName = keyborad.nextLine();
            outputFile.println(friendName);
        }
        outputFile.close();
        System.out.println("Data written to ");
    }
}
