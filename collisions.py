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
    print firstM
    secondM = secondCar.vel.getMInD(angle)
    print secondM
    firstCar.vel.addDM(angle, -firstM)
    firstCar.vel.addDM(angle, secondM)
    firstCar.takeDamage(int(math.floor(max(0, secondM * -1)))*2)
    secondCar.vel.addDM(angle, firstM)
    secondCar.vel.addDM(angle, -secondM)
    secondCar.takeDamage(int(math.floor(max(0, firstM)))*2)
    dist = math.hypot(x, y)
    if dist < 1:
       dx = 1 / dist * x
       dy = 1 / dist * y
       firstCar.model.setPos(firstCar.model.getX() - dx + x, firstCar.model.getY() - dy + y)

def bumperCollision(car, bumper):
    direction = bumper.getH()
    if direction % 180 == 0:
        if car.model.getX() > bumper.getX() + 25 or car.model.getX() < bumper.getX() - 25:
            car.vel.x *= -1
        else:
            car.vel.y *= -1
    elif direction % 180 == 90:
        if car.model.getY() > bumper.getY() + 25 or car.model.getY() < bumper.getY() - 25:
            car.vel.y *= -1
        else:
            car.vel.x *= -1
    else:
        car.vel.setDM(car.vel.getD(), car.vel.getM() * -1)
    car.vel.setDM(car.vel.getD(), car.vel.getM()*3/4)