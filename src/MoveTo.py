from src.VehicleModel import Vehicle
from math import acos
from math import sqrt
from math import pi
import time


#function that takes XY values of point and a vehicle and navigates vehicle to that point
def goTo(finalPos, vehicle):
    print('Start of goTo')
    currentPos = vehicle.getPosXYZ()

    #main loop that directs vehicle to the final point
    while((currentPos[0]>(finalPos[0]+3) or currentPos[0]<(finalPos[0]-3)) or (currentPos[1]>(finalPos[1]+3) or currentPos[1]<(finalPos[1]-3))):
        #gets current data of vehicle
        currentPos = vehicle.getPosXYZ()
        currentDir = vehicle.getDirection()

        #calculates vector to the final position
        routeVector = [finalPos[0] - currentPos[0], finalPos[1] - currentPos[1]]

        angleLeft = angle(currentDir, routeVector)
        currentSteering = vehicle.getAngle()
        dt = globalClock.getDt()
        #deciding where to turn - and if it should change steering
        if(angleLeft<0):
            if(angleLeft<currentSteering):
                vehicle.setAngle(False, dt)
            else:
                vehicle.setAngle(True, dt)
        else:
            if (angleLeft > currentSteering):
                vehicle.setAngle(True, dt)
            else:
                vehicle.setAngle(False, dt)

        distance = sqrt((routeVector[0] ** 2)+(routeVector[1] ** 2))
        #setting motor power
        if(distance>25):
            vehicle.setEngineForce(1100)
        else:
            vehicle.setEngineForce(600)

    vehicle.setEngineForce(0)
    print('found right position', finalPos, currentPos)
    vehicle.setBrakeForce(200)

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
