from turtle import Turtle


MOVE_DIST = 60


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.color('steel blue')
        self.shape('square')
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=10)
        self.goto(x=0, y=-280)

    def move_left(self):
        if self.xcor() <= -490:
            return
        self.backward(MOVE_DIST)

    def move_right(self):
        if self.xcor() >= 490:
            return
        self.forward(MOVE_DIST)

    def paddle_reset(self):
        self.clear()
