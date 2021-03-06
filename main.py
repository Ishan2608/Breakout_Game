import turtle as tr
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from ui import UI
from bricks import Bricks
import time

# ---------------------------SETTING UP OUR SCREEN---------------------------
screen = tr.Screen()
screen.setup(width=1200, height=600)
screen.title('Breakout')
screen.bgcolor('black')
screen.tracer(0)

# ----------------------------CREATING OUR OBJECTS----------------------------
ui = UI()
score = Scoreboard(lives=5)
paddle = Paddle()
bricks = Bricks()
ball = Ball()

# --------------------GLOBAL VARIABLES FOR RUNNING THE GAME--------------------
game_paused = False
playing_game = True


def pause_game():
    global game_paused
    if game_paused:
        game_paused = False
    else:
        game_paused = True


# ------------------------SETTING OUR SCREEN LISTENERS------------------------
screen.listen()
screen.onkey(key='Left', fun=paddle.move_left)
screen.onkey(key='Right', fun=paddle.move_right)
screen.onkey(key='space', fun=pause_game)

# ------------DEFINING FUNCTIONS TO MAKE THE GAME OBJECTS INTERACT------------


def check_collision_with_walls(ball, score, ui):
    global playing_game
    # detect collision with left and right walls:
    if ball.xcor() < -580 or ball.xcor() > 570:
        ball.bounce(x_bounce=True, y_bounce=False)
        return

    # detect collision with upper ball
    if ball.ycor() > 277:
        ball.bounce(x_bounce=False, y_bounce=True)
        return

    # detect collision with bottom wall
    # In this case, user failed to hit the ball thus he loses. The game resets.
    if ball.ycor() < -280:
        ball.reset()
        score.decrease_lives()
        if score.lives == 0:
            score.reset()
            playing_game = False
            ui.game_over(win=False)
            return
        ui.change_color()
        return


def check_collision_with_paddle(ball, paddle):
    # record x-axis coordinates of ball and paddle
    paddle_x = paddle.xcor()
    ball_x = ball.xcor()

    # check if ball's distance(from its middle) from paddle(from its middle) is less than
    # width of paddle and ball is belo a certain coordinate to detect their collision
    if ball.distance(paddle) < 110 and ball.ycor() < -250:

        # If Paddle is on Right of Screen
        if paddle_x > 0:
            if ball_x > paddle_x:
                # If ball hits paddles left side it should go back to left
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            else:
                ball.bounce(x_bounce=False, y_bounce=True)
                return

        # If Paddle is left of Screen
        elif paddle_x < 0:
            # If ball hits paddle's left side it should go back to left
            if ball_x < paddle_x:
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            else:
                ball.bounce(x_bounce=False, y_bounce=True)
                return

        # Else Paddle is in the Middle horizontally
        else:
            ball.bounce(x_bounce=False, y_bounce=True)
            return


def check_collision_with_bricks(ball, score, bricks):
    for brick in bricks.bricks:
        if ball.distance(brick) < 40:
            score.increase_score()
            brick.quantity -= 1
            if brick.quantity == 0:
                brick.clear()
                brick.goto(3000, 3000)
                bricks.bricks.remove(brick)

            # detect collision from left or right
            if ball.xcor() < brick.left_wall or ball.xcor() > brick.right_wall:
                ball.bounce(x_bounce=True, y_bounce=False)
                return

            # detect collision from bottom or top
            elif ball.ycor() < brick.bottom_wall or ball.ycor() > brick.upper_wall:
                ball.bounce(x_bounce=False, y_bounce=True)
                return


def play_breakout(paddle, ball, bricks, score, ui):
    global playing_game, game_paused
    while playing_game:
        if not game_paused:

            # ----------------UPDATE SCREEN WITH ALL THE MOTION THAT HAS HAPPENED----------------
            screen.update()
            time.sleep(0.03)
            ball.move()

            # ---------------------------DETECTING COLLISION WITH WALLS---------------------------
            check_collision_with_walls(ball, score, ui)

            # -------------------------DETECTING COLLISION WITH THE PADDLE-------------------------
            check_collision_with_paddle(ball, paddle)

            # ---------------------------DETECTING COLLISION WITH A BRICK---------------------------
            check_collision_with_bricks(ball, score, bricks)

            # -------------------------------DETECTING USER'S VICTORY-------------------------------
            if len(bricks.bricks) == 0:
                ui.game_over(win=True)

        else:
            ui.paused_status()


# ------------------CALL THE MAIN FUNCTION THAT RUNS THE GAME------------------
play_breakout(paddle, ball, bricks, score, ui)

tr.mainloop()
