
public class ConstructorDemo {

    public static void main(String[] args) {
        Rectangle box, box2;
        box = new Rectangle(5.0, 15.0, "Blue");
        box2 = new Rectangle();

        System.out.println("The box's length is " + box.getLength());
        System.out.println("The box's width is " + box.getWidth());
        System.out.println("The box's area is " + box.getArea());
        System.out.println("Color = " + box.getColor());
    }
}
