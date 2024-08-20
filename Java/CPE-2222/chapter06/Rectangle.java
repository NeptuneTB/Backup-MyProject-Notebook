
public class Rectangle {

    private double length;
    private double width;
    private String color;

    public Rectangle() {
        length = 1.0;
        width = 1.0;
    }

    public Rectangle(double len, double w, String c) {
        length = len;
        width = w;
        color = c;
    }

    public double getLength() {
        return length;
    }

    public void setLength(double length) {
        this.length = length;
    }

    public double getWidth() {
        return width;
    }

    public void setWidth(double width) {
        this.width = width;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public Double getArea() {
        return this.length * this.width;
    }

}
