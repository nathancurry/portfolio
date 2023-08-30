import turtle
import pandas
import types

FONT = ('Berkeley Mono Variable', 10, 'normal')

image = 'blank_states_img.gif'
csv_file = '50_states.csv'

screen = turtle.Screen()
screen.title('US State Guesser')

screen.addshape(image)
turtle.shape(image)

label = turtle.Turtle()
label.penup()
label.hideturtle()


data = pandas.read_csv(csv_file)
remaining = data
score = set()
while len(score) < 50:
    guess = screen.textinput('Guess the State', prompt='Guess a state name').title()
    if guess == 'Exit' or guess == 'Quit':
        break
    if guess in score:
        print(f'You already guessed {guess.title()}')
    elif guess in data.state.values:
        score.add(guess)
        row = data[data.state == guess]
        label.goto(row.x.values[0],row.y.values[0])
        label.write(guess, align = 'center', font = FONT)
        remaining = remaining.drop(data[data['state'] == guess].index)
    else:
        print(f'{guess} is not a state.  Guess again!')

remaining.to_csv('states_to_learn.csv')