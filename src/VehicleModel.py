from panda3d.bullet import BulletVehicle
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import TransformState
from panda3d.core import Point3
from panda3d.core import Vec3
from panda3d.bullet import ZUp

class Vehicle(BulletVehicle):

    def __init__(self, posx, posy, posz, color, worldNP, world):

        # Chassis
        shape = BulletBoxShape(Vec3(0.45, 0.98, 0.25))
        ts = TransformState.makePos(Point3(0, 0, 0.06))

        np = worldNP.attachNewNode(BulletRigidBodyNode('Vehicle'))
        np.node().addShape(shape, ts)
        np.setPos(posx, posy, posz)
        np.node().setMass(700.0)
        np.node().setDeactivationEnabled(False)

        world.attachRigidBody(np.node())

        # np.node().setCcdSweptSphereRadius(1.0)
        # np.node().setCcdMotionThreshold(1e-7)

        # Vehicle
        super(Vehicle, self).__init__(world, np.node())
        self.setCoordinateSystem(ZUp)
        world.attachVehicle(self)

        if(color == "B"):
            yugoNP = loader.loadModel('../Models/ChassisB.egg')
        elif(color == "G"):
            yugoNP = loader.loadModel('../Models/ChassisG.egg')
        else:
            yugoNP = loader.loadModel('../Models/ChassisR.egg')
        yugoNP.reparentTo(np)

        # Right front wheel
        np = loader.loadModel('../Models/wheel.egg')
        np.reparentTo(worldNP)
        self.addWheel(Point3(0.60, 0.95, 0.3), True, np)

        # Left front wheel
        np = loader.loadModel('../Models/wheel.egg')
        np.reparentTo(worldNP)
        self.addWheel(Point3(-0.60, 0.95, 0.3), True, np)

        # Right rear wheel
        np = loader.loadModel('../Models/wheel.egg')
        np.reparentTo(worldNP)
        self.addWheel(Point3(0.60, -0.95, 0.3), False, np)

        # Left rear wheel
        np = loader.loadModel('../Models/wheel.egg')
        np.reparentTo(worldNP)
        self.addWheel(Point3(-0.60, -0.95, 0.3), False, np)

        # Steering info
        self.steering = 0.0  # degree
        self.steeringClamp = 45.0  # degree
        self.steeringIncrement = 120.0  # degree per second

    def addWheel(self, pos, front, np):
        wheel = self.createWheel()

        wheel.setNode(np.node())
        wheel.setChassisConnectionPointCs(pos)
        wheel.setFrontWheel(front)

        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setWheelAxleCs(Vec3(1, 0, 0))
        wheel.setWheelRadius(0.33)
        wheel.setMaxSuspensionTravelCm(40.0)

        wheel.setSuspensionStiffness(40.0)
        wheel.setWheelsDampingRelaxation(2.3)
        wheel.setWheelsDampingCompression(4.4)
        wheel.setFrictionSlip(100.0)
        wheel.setRollInfluence(0.1)

    #function that returns position of front wheel
    def getPosXYZ(self):
        # gettingPos
        position = self.getWheel(0).getNode()
        try:
            arrayOfStrings = str(position).split()
            z = arrayOfStrings[5]
            posXYZ = [float(arrayOfStrings[3]), float(arrayOfStrings[4]), float(z[:-1])]
            return (posXYZ)
        except IndexError:
            return ([0.0 , 0.0 , -200.0])

    #function chor changin steering of front wheels
    def setAngle(self, left, dt):
        if(left):
            self.steering += dt * self.steeringIncrement
            self.steering = min(self.steering, self.steeringClamp)
        else:
            self.steering -= dt * self.steeringIncrement
            self.steering = max(self.steering, -self.steeringClamp)
        # Apply steering to front wheels
        self.setSteeringValue(self.steering, 0)
        self.setSteeringValue(self.steering, 1)

    #function that sets engine force of rear wheels
    def setEngineForce(self, engineForce):
        self.applyEngineForce(engineForce, 2)
        self.applyEngineForce(engineForce, 3)

    #function that sets brake
    def setBrakeForce(self, brakeForce):
        self.setBrake(brakeForce, 2)
        self.setBrake(brakeForce, 3)

    #function that returns current steering of front wheels
    def getAngle(self):
        return self.steering

    #function that returns direction of vehicle
    def getDirection(self):
        position = self.getWheel(0).getNode()
        try:
            arrayOfStrings = str(position).split()
            z = arrayOfStrings[5]
            posXY1 = [float(arrayOfStrings[3]), float(arrayOfStrings[4])]
        except IndexError:
            return ([0.0, 0.0])
        position = self.getWheel(2).getNode()
        try:
            arrayOfStrings = str(position).split()
            z = arrayOfStrings[5]
            posXY2 = [float(arrayOfStrings[3]), float(arrayOfStrings[4])]
        except IndexError:
            return ([0.0, 0.0])
        return ([(posXY1[0]-posXY2[0])/1.9, (posXY1[1]-posXY2[1])/1.9])