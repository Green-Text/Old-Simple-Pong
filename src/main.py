#   Pong Game Tutorial Implementation from kivy.org

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file("main.kv")

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounceBall(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            bounced = Vector(-1*vx,vy)
            if((abs(bounced.x) <= 20) and ( abs(bounced.y <= 20))):
                vel = bounced*-1.25
            else:
                vel = bounced*1.25
            ball.velocity = vel.x, vel.y

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x,velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    def serve_ball(self, vel = (4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel
    
    def update(self, dt):
        self.ball.move()
        self.player1.bounceBall(self.ball)
        self.player2.bounceBall(self.ball)
        self.p1Score.text = str(self.player1.score)
        self.p2Score.text = str(self.player2.score)
        
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        if (self.ball.x < 0):
            self.player2.score += 1
            self.serve_ball(vel=(4,0))
        if (self.ball.right > self.width):
            self.player1.score += 1
            self.serve_ball(vel= (-4,0))
    
    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update,1.0/60.0)
        return game

if __name__ == "__main__":
    PongApp().run()