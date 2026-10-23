# Object-Oriented Programming Concepts

## Introduction
Object-Oriented Programming (OOP) is a programming paradigm that revolves around the concept of objects and classes. It provides a set of principles and techniques for designing, implementing, and managing complex software systems.

## Classes and Objects
A class is a blueprint or a template that defines the properties and behavior of an object. An object is an instance of a class, and has its own set of attributes (data) and methods (functions).

## Inheritance
Inheritance is the mechanism by which one class can inherit the properties and behavior of another class. The child class inherits all the fields and methods of the parent class and can also add new fields and methods or override the ones inherited from the parent class.

## Polymorphism
Polymorphism is the ability of an object to take on multiple forms. This can be achieved through method overriding or method overloading. Method overriding is when a child class provides a different implementation of a method that is already defined in its parent class. Method overloading is when multiple methods with the same name can be defined, but with different parameter lists.

## Encapsulation
Encapsulation is the concept of hiding the implementation details of an object from the outside world and only exposing the necessary information through public methods. This helps to protect the internal state of an object from external interference and misuse.

## Abstraction
Abstraction is the concept of showing only the necessary information to the outside world while hiding the internal details. This helps to reduce complexity and improve modularity.

## Composition
Composition is the concept of creating objects from other objects or collections of objects. This helps to create complex objects from simpler ones.

## Interfaces
An interface is a abstract class that defines a contract or a set of methods that must be implemented by any class that implements it. Interfaces are used to define a common set of methods that can be called by other classes.

## Access Modifiers
Access modifiers are used to control access to the members of a class. The most common access modifiers are public, private, and protected. Public members can be accessed from anywhere, private members can only be accessed within the same class, and protected members can be accessed within the same class and its child classes.

## SOLID Principles
SOLID is an acronym that stands for five design principles of object-oriented programming that aim to promote simpler, more robust, and updatable code for software development in object-oriented languages. Each letter in SOLID represents a principle for development:

### Single Responsibility Principle (SRP)
The Single Responsibility Principle states that a class should have only one reason to change. This means that a class should have only one responsibility or one single purpose.

### Open/Closed Principle (OCP)
The Open/Closed Principle states that a class should be open for extension but closed for modification. This means that you should be able to add new functionality to a class without modifying its existing code.

### Liskov Substitution Principle (LSP)
The Liskov Substitution Principle states that derived classes should be substitutable for their base classes. This means that any code that uses a base class should be able to work with a derived class without knowing the difference.

### Interface Segregation Principle (ISP)
The Interface Segregation Principle states that clients should not be forced to depend on interfaces they do not use. This means that instead of having a large, fat interface, you should have multiple smaller interfaces that are more specific to the needs of the clients.

### Dependency Inversion Principle (DIP)
The Dependency Inversion Principle states that high-level modules should not depend on low-level modules, but both should depend on abstractions. This means that instead of having a high-level module depend on a low-level module, you should have both modules depend on an abstraction that defines the interface between them.

## Example Use Cases
Here are some example use cases of OOP concepts:

* A banking system where customers are objects and have attributes like name, account number, and balance. The customer class can have methods like deposit, withdraw, and check balance.
* A university management system where students, teachers, and courses are objects. The student class can have attributes like name, roll number, and course enrolled, and methods like enroll course, drop course, and check grades.
* A game where characters, weapons, and levels are objects. The character class can have attributes like name, health, and score, and methods like attack, defend, and move.

## Code Example
# Define a parent class called Vehicle
class Vehicle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = 0

    def drive(self, miles):
        self.mileage += miles

    def describe_vehicle(self):
        print(f"This vehicle is a {self.year} {self.brand} {self.model} with {self.mileage} miles.")

# Define a child class called Car that inherits from Vehicle
class Car(Vehicle):
    def __init__(self, brand, model, year, doors):
        super().__init__(brand, model, year)
        self.doors = doors

    def describe_vehicle(self):
        super().describe_vehicle()
        print(f"It has {self.doors} doors.")

# Define a child class called Truck that inherits from Vehicle
class Truck(Vehicle):
    def __init__(self, brand, model, year, capacity):
        super().__init__(brand, model, year)
        self.capacity = capacity

    def describe_vehicle(self):
        super().describe_vehicle()
        print(f"It has a capacity of {self.capacity} tons.")

# Create objects
my_car = Car('Toyota', 'Corolla', 2015, 4)
my_truck = Truck('Ford', 'F-150', 2010, 2)

# Call methods
my_car.drive(100)
my_car.describe_vehicle()

my_truck.drive(50)
my_truck.describe_vehicle()