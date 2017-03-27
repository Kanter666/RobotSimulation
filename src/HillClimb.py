from random import random
from random import uniform
from math import acos
from math import sqrt
from math import pi
import time

#TODO implement map and algorithm to find highest point in enviroment(or at least local max)
def blindClimb(vehicle):
    print('Start of follow function')

    time.sleep(10)
    top = vehicle.getPosXYZ()
    print("top: ", top)

    for i in range(0,100):
        print("Going nowhere")
        vehicle.setEngineForce(1000)
        dt = globalClock.getDt()
        if(random()>0.5):
            vehicle.setAngle(True, dt)
        else:
            vehicle.setAngle(False, dt)
        # gets current data of vehicles
        currentPos = vehicle.getPosXYZ()
        currentDir = vehicle.getDirection()

        if(top[2]<=currentPos[2]):
            top = currentPos
        time.sleep(0.01*i)

    # main loop that directs vehicle to the followed vehicle, runs forever
    while (True):
        # gets current data of vehicles
        currentPos = vehicle.getPosXYZ()
        currentDir = vehicle.getDirection()

        if(top[2]<=currentPos[2]):
            top = currentPos
            if(random()<0.0005):
                print(random())
                print(random())
                print(random())
                vehicle.setEngineForce(0)
                vehicle.setBrakeForce(100)
                print("Found top!!")
                break

        if(random()>0.2):
            # calculates vector to the final position
            routeVector = [top[0] - currentPos[0], top[1] - currentPos[1]]

            angleLeft = angle(currentDir, routeVector)
            currentSteering = vehicle.getAngle()
            dt = globalClock.getDt()
            # deciding where to turn - and if it should change steering
            if (angleLeft < 0):
                if (angleLeft < currentSteering):
                    vehicle.setAngle(False, dt)
                else:
                    vehicle.setAngle(True, dt)
            else:
                if (angleLeft > currentSteering):
                    vehicle.setAngle(True, dt)
                else:
                    vehicle.setAngle(False, dt)

            distance = sqrt((routeVector[0] ** 2) + (routeVector[1] ** 2))
            # setting motor power
            if (distance > 25):
                vehicle.setEngineForce(1100)
            else:
                vehicle.setEngineForce(600)
        else:
            print("Going to fake top")
            fakeTop = [top[0]+uniform(0.01, 3.5),top[0]+uniform(0.01, 3.5),top[0]+uniform(0.01, 3.5)]
            # calculates vector to the final position
            routeVector = [fakeTop[0] - currentPos[0], fakeTop[1] - currentPos[1]]

            angleLeft = angle(currentDir, routeVector)
            currentSteering = vehicle.getAngle()
            dt = globalClock.getDt()
            # deciding where to turn - and if it should change steering
            if (angleLeft < 0):
                if (angleLeft < currentSteering):
                    vehicle.setAngle(False, dt)
                else:
                    vehicle.setAngle(True, dt)
            else:
                if (angleLeft > currentSteering):
                    vehicle.setAngle(True, dt)
                else:
                    vehicle.setAngle(False, dt)

            distance = sqrt((routeVector[0] ** 2) + (routeVector[1] ** 2))
            # setting motor power
            if (distance > 25):
                vehicle.setEngineForce(1100)
            else:
                vehicle.setEngineForce(600)





# part that calculates angle
# - means angle is clockwise
# + means angle is counterclockwise
def length(v):
    return sqrt(v[0] ** 2 + v[1] ** 2)

def dot_product(v, w):
    return v[0] * w[0] + v[1] * w[1]

def determinant(v, w):
    return v[0] * w[1] - v[1] * w[0]

def inner_angle(v, w):
    try:
        cosx = dot_product(v, w) / (length(v) * length(w))
        rad = acos(cosx)  # in radiann
        return rad * 180 / pi  # returns degrees
    except(ZeroDivisionError):
        return 0  # starting values are 0s -> that results into division by 0

def angle(A, B):
    inner = inner_angle(A, B)
    det = determinant(A, B)
    if det < 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
        return -inner
    else:  # if the det > 0 then A is immediately clockwise of B
        return inner

