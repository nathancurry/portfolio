from turtle import Turtle
import random

COLORS = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 2
STARTING_COUNT = 10

class Traffic():
    def __init__(self):
        self.cars = []
        self.spares = set()
        self.car_count = STARTING_COUNT
        self.speed = STARTING_MOVE_DISTANCE

    def level_up(self):
        self.increase_speed()
        self.increase_count()

    def increase_speed(self):
        self.speed += MOVE_INCREMENT
    
    def increase_count(self):
        self.car_count += 1

    def create_car(self) -> None:
        if random.randint(1,10) == 1:
            if len(self.cars) < self.car_count:
                self.cars.append(Car())
            elif self.spares:
                index = self.spares.pop()
                self.cars[index].start()

    def move_cars(self) -> None:
        for index,car in enumerate(self.cars):
            if car.xcor() > -320:
                car.move()
            else:
                self.spares.add(index)

class Car(Turtle):
    def __init__(self):
        super().__init__()
        self.speed = None
        self.penup()
        self.shape('square')
        self.shapesize(stretch_len=2)
        self.color(random.choice(COLORS))
        self.setheading(180)
        self.start()

    def move(self):
        self.forward(self.speed)
        
    
    def set_speed(self, speed = STARTING_MOVE_DISTANCE):
        self.speed = speed + random.randint(-1, 1)

    def start(self):
        self.goto(300, random.randint(-250,250))
        self.set_speed()
    

