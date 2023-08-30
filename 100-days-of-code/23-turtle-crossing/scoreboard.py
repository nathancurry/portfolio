from turtle import Turtle

FONT = ('Berkeley Mono Variable', 20, 'normal')
POSITION = (-280, 270)

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 1
        self.hideturtle()
        self.penup()
        self.setpos(POSITION)
        self.penup()
        self.update()
        
    def update(self) -> None:
        self.clear()
        self.write(f'Level: {self.score}', align = 'left', font = FONT)

    def increment(self) -> None:
        self.score += 1
        self.update()
    
    def erase(self) -> None:
        self.score = 0
        self.update()
    
    def game_over(self) -> None:
        self.goto((0,0))
        self.write('GAME OVER', align = 'center', font = FONT)