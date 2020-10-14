from sense_hat import SenseHat
from time import sleep, time
from random import randrange

senseHat = SenseHat()
senseHat.clear()

ballColor = (0,0,255)

matrix = [[(0,0,0)] * 8 for i in range(8)]
liste = [(0,0,0)] * 64

ball_pos = [4, 0]
ball_vel = [0, 0]

timeStart = time()
timeCurrent = timeStart

senseHat.set_pixel(round(ball_pos[0]), round(ball_pos[1]), ballColor)
while True:
  accel = senseHat.get_accelerometer_raw()
  accelX = accel['x']
  accelY = accel['y']

  if abs(accelX) > 3 or abs(accelY) > 3:
    ball_vel[0] = accelX
    ball_vel[1] = accelY

  while abs(ball_vel[0]) >= 0.5 and abs(ball_vel[1]) >= 0.5:

    timeCurrent = time()
    if timeCurrent - timeStart > 0.1:
      timeStart = timeCurrent
      senseHat.clear()
      #print(ball_pos, ball_vel)
      if ball_pos[0] > 7:
        ball_pos[0] = 7
      if ball_pos[1] > 7:
        ball_pos[1] = 7
      if ball_pos[0] < 0:
        ball_pos[0] = 0
      if ball_pos[1] < 0:
        ball_pos[1] = 0
      senseHat.set_pixel(round(ball_pos[0]), round(ball_pos[1]), ballColor)

      if ball_pos[0] >= 7:
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] += 0.1

      if ball_pos[0] <= 0:
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] -= 0.1

      if ball_pos[1] >= 7:
        ball_vel[1] = -ball_vel[1]
        ball_vel[1] += 0.1

      if ball_pos[1] <= 0:
        ball_vel[1] = -ball_vel[1]
        ball_vel[1] -= 0.1

      ball_pos[0] += ball_vel[0]
      ball_pos[1] += ball_vel[1]
