from turtle import Screen
from time import sleep
from player import Player
from traffic import Traffic
from scoreboard import Scoreboard


def init_screen() -> Screen():
    screen = Screen()
    screen.setup(width=600, height=600)
    screen.tracer(0)
    screen.listen()
    return screen

def update_screen(screen) -> None:
    sleep(0.1)
    screen.update()

def main() -> None:
    screen = init_screen()
    player = Player()
    score = Scoreboard()
    traffic = Traffic()

    screen.onkey(player.move, 'Up')

    game_on = True
    while game_on:
        if player.is_at_finish_line():
            player.restart()
            traffic.level_up()
            score.increment()
        for car in traffic.cars:
            if car.distance(player) < 20:
                game_on = False
                score.game_over()
        traffic.create_car()
        traffic.move_cars()
        update_screen(screen)

    screen.exitonclick()

if __name__ in '__main__':
    main()
