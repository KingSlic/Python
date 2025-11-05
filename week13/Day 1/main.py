from math import pi

class Shape:
    def __init__(self, color):
        self.color = color

    # # [Abstraction] The area method implementation is abstracted away
    def area(self):
        raise NotImplementedError("Subclass must implement the area method")
        
    def print_shape_color(self):
        print(f"I'm {self.__class__.__name__} and my color is: {self.color}")
         
# Class Circle inherits (Shape) class, meaning it ends up having access to its attributes and methods
class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.__radius = radius # Radius is a private attribute that is only accessible inside the Circle class

    # Polymorphism, area method implementation is different for each class (Circle and Rectangle)
    def area(self):
        return pi * (self.__radius**2)


class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.__width = width
        self.__height = height

    def area(self):
        return self.__width * self.__height

circle1 = Circle("Red", 3)
print(circle1.area())

rectangle1 = Rectangle("Blue", 5, 6)
print(rectangle1.area())


circle1.print_shape_color()

rectangle1.print_shape_color()