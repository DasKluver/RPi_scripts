from sense_hat import SenseHat
from time import sleep, time
from random import randrange

def random_color():
  r = randrange(0, 255)
  g = randrange(0, 255-r)
  b = 255-(r+g)
  color = (r, g, b)
  return color

def random_pos():
  x = randrange(0, 8)
  y = randrange(0, 8)
  pos = [x,y]
  return pos

def random_vel():
  x = randrange(-3, 4)
  y = randrange(-3, 4)
  vel = [x,y]
  return vel

class klebrig_ball():
  def __init__(ball, pos, vel, color,classSenseHat):
    ball.ballPos = pos
    ball.ballVel = vel
    ball.ballColor = color

    ball.sh = classSenseHat
    ball.sh.clear()

    ball.timeStart = time()
    ball.timeCurrent = ball.timeStart
    
  def move_ball(ball, ballAccel):

    if abs(ball.ballVel[0]) < 0.5 and abs(ball.ballVel[1]) < 0.5:
  
      accelX = ballAccel['x']
      accelY = ballAccel['y']

      ball.sh.set_pixel(round(ball.ballPos[0]), round(ball.ballPos[1]), ball.ballColor)

      if abs(accelX) > 3 or abs(accelY) > 3:
        ball.ballVel[0] = accelX
        ball.ballVel[1] = accelY

    else:

      ball.timeCurrent = time()
      if ball.timeCurrent - ball.timeStart > 0.1:
        ball.timeStart = ball.timeCurrent        

        if ball.ballPos[0] >= 7:
          ball.ballVel[0] = -ball.ballVel[0]
          ball.ballVel[0] += 0.1

        if ball.ballPos[0] <= 0:
          ball.ballVel[0] = -ball.ballVel[0]
          ball.ballVel[0] -= 0.1

        if ball.ballPos[1] >= 7:
          ball.ballVel[1] = -ball.ballVel[1]
          ball.ballVel[1] += 0.1

        if ball.ballPos[1] <= 0:
          ball.ballVel[1] = -ball.ballVel[1]
          ball.ballVel[1] -= 0.1

        ball.sh.set_pixel(round(ball.ballPos[0]), round(ball.ballPos[1]), (0,0,0))
        
        ball.ballPos[0] += ball.ballVel[0]
        ball.ballPos[1] += ball.ballVel[1]

        if ball.ballPos[0] > 7:
          ball.ballPos[0] = 7
        if ball.ballPos[1] > 7:
          ball.ballPos[1] = 7
        if ball.ballPos[0] < 0:
          ball.ballPos[0] = 0
        if ball.ballPos[1] < 0:
          ball.ballPos[1] = 0
        
        ball.sh.set_pixel(round(ball.ballPos[0]), round(ball.ballPos[1]), ball.ballColor)
        #End class
        
senseHat = SenseHat()
senseHat.clear()

ball = []

action = []
direction = []
x = 0

while True:
  
  if "pressed" in action and "middle" in direction:
    ball.append("ball" + str(x))

    ballPos = random_pos()
    ballVel = random_vel()
    ballColor = random_color()
    
    ball[x] = klebrig_ball(ballPos, ballVel, ballColor, senseHat)
    
    x += 1
    action = []
    direction = []
  else:
    for event in senseHat.stick.get_events():
        action.append(event.action)
        direction.append(event.direction)
  accel = senseHat.get_accelerometer_raw()
  for i in range(0, x):  
    ball[i].move_ball(accel)
