from src.VehicleModel import Vehicle
from math import acos
from math import sqrt
from math import pi
import time


#function for following vehicle
#algorithm is basically the same as in MoveTo, only final location is not static but it is current location of followed vehicle
def follow(follower, followedVehicle):
    print('Start of follow function')

    #main loop that directs vehicle to the followed vehicle, runs forever
    while(True):
        #gets current data of vehicles
        currentPos = follower.getPosXYZ()
        currentDir = follower.getDirection()
        finalPos = followedVehicle.getPosXYZ()

        #calculates vector to the final position
        routeVector = [finalPos[0] - currentPos[0], finalPos[1] - currentPos[1]]

        angleLeft = angle(currentDir, routeVector)
        currentSteering = follower.getAngle()
        dt = globalClock.getDt()
        #deciding where to turn - and if it should change steering
        if(angleLeft<0):
            if(angleLeft<currentSteering):
                follower.setAngle(False, dt)
            else:
                follower.setAngle(True, dt)
        else:
            if (angleLeft > currentSteering):
                follower.setAngle(True, dt)
            else:
                follower.setAngle(False, dt)

        distance = sqrt((routeVector[0] ** 2)+(routeVector[1] ** 2))
        #setting motor power
        if(distance>15):
            follower.setEngineForce(1000)
        else:
            follower.setEngineForce(0)
            follower.setBrakeForce(200)
        time.sleep(0.01)


#part that calculates angle
# - means angle is clockwise
# + means angle is counterclockwise
def length(v):
    return sqrt(v[0]**2+v[1]**2)
def dot_product(v,w):
   return v[0]*w[0]+v[1]*w[1]
def determinant(v,w):
   return v[0]*w[1]-v[1]*w[0]
def inner_angle(v,w):
   try:
       cosx=dot_product(v,w)/(length(v)*length(w))
       rad=acos(cosx) # in radiann
       return rad*180/pi # returns degrees
   except(ZeroDivisionError):
       return 0     #starting values are 0s -> that results into division by 0
def angle(A, B):
    inner=inner_angle(A,B)
    det = determinant(A,B)
    if det<0: #this is a property of the det. If the det < 0 then B is clockwise of A
        return -inner
    else: # if the det > 0 then A is immediately clockwise of B
        return inner