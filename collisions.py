"""
Collision functions
takes 2 cars and bounces the first off of the second,
or a car and an obstacle and bounces the car
"""
from __future__ import division
import math


def collideCars(firstCar, secondCar):
    x = secondCar.model.getX() - firstCar.model.getX()
    y = secondCar.model.getY() - firstCar.model.getY()
    angle = (math.degrees(math.atan2(y, x))-90) % 360
    firstM = firstCar.vel.getMInD(angle)
    secondM = secondCar.vel.getMInD(angle)
    firstCar.vel.addDM(angle, -firstM)
    firstCar.vel.addDM(angle, secondM)
    secondCar.vel.addDM(angle, firstM)
    secondCar.vel.addDM(angle, -secondM)
    dist = math.hypot(x, y)
    if dist < 1:
       dx = 1 / dist * x
       dy = 1 / dist * y
       firstCar.model.setPos(firstCar.model.getX() - dx + x, firstCar.model.getY() - dy + y)

def bumperCollision(car, bumper):
    pass