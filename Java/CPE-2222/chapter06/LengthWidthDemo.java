
public class LengthWidthDemo {

    public static void main(String[] args) {
        Rectangle box = new Rectangle();
        Rectangle box2 = new Rectangle();

        box.setLength(10.0);
        box2.setLength(11.0);

        box.setWidth(20.0);
        box.setColor("Red");
        
        System.out.println("The box's length is " + box.getLength());
        System.out.println("The box's width is " + box.getWidth());

        System.out.println("The box's length is " + box2.getLength());
        System.out.println("The box's area is " + box.getArea());
        System.out.println(box.getClass());
    }

}
