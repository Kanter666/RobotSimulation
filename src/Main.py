# from pandac.PandaModules import loadPrcFileData
# loadPrcFileData('', 'load-display tinydisplay')
from src.VehicleModel import Vehicle
from src.MoveTo import goTo
from src.FollowVehicle import follow

import sys
import _thread as thread


from direct.showbase.ShowBase import ShowBase
from direct.showbase.InputStateGlobal import inputState

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import BitMask32
from panda3d.core import Filename
from panda3d.core import PNMImage
from panda3d.core import GeoMipTerrain


from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import ZUp
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape

class Simulation(ShowBase):
    def __init__(self):

        # Heightfield (static)
        self.height = 38.0


        ShowBase.__init__(self)
        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)

        base.cam.setPos(0, -150, 200)
        base.cam.lookAt(0, 0, 0)

        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alightNP = render.attachNewNode(alight)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = render.attachNewNode(dlight)

        render.clearLight()
        render.setLight(alightNP)
        render.setLight(dlightNP)

        # Input
        self.accept('escape', self.doExit)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('backward', 'x')
        inputState.watchWithModifiers('right', 'd')

        # Task
        taskMgr.add(self.update, 'updateWorld')

        # Physics
        self.setup()

    # _____HANDLER_____

    def doExit(self):
        self.cleanup()
        sys.exit(1)


    # ____TASK___

    def processInput(self, dt):
        for vehicle in self.controlVehicles:
            engineForce = 0.0
            brakeForce = 0.0

            if inputState.isSet('forward'):
                engineForce = 1000.0
                brakeForce = 0.0

            if inputState.isSet('backward'):
                engineForce = -1000.0
                brakeForce = 0.0

            if inputState.isSet('reverse'):
                engineForce = 0.0
                brakeForce = 100.0

            if inputState.isSet('left'):
                vehicle.setAngle(True, dt)

            if inputState.isSet('right'):
                vehicle.setAngle(False, dt)


            # Apply engine and brake to rear wheels
            vehicle.setEngineForce(engineForce)
            vehicle.setBrakeForce(brakeForce)


            #print(vehicle.getAngle())


    def update(self, task):
        dt = globalClock.getDt()

        self.processInput(dt)
        self.world.doPhysics(dt, 10, 0.008)

        self.terrain.update()

        return task.cont

    def cleanup(self):
        self.world = None
        self.worldNP.removeNode()

    def setup(self):
        self.worldNP = render.attachNewNode('World')

        # World
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        #height map
        # Filename:
        # small ->  'Maps/HeightMapSmall.png'
        # big   ->  'Maps/HeightMapBig.png'
        img = PNMImage(Filename('Maps/HeightMapSmall.png'))
        shape = BulletHeightfieldShape(img, self.height, ZUp)
        shape.setUseDiamondSubdivision(True)

        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Heightfield'))
        np.node().addShape(shape)
        np.setPos(0, 0, 0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        #adding Texture
        #setColorMap:
        #small ->   'Maps/TextureMapSmall.jpg'
        #big   ->   'Maps/TextureMapBig.jpg'
        self.terrain = GeoMipTerrain('terrain')
        self.terrain.setHeightfield(img)
        self.terrain.setColorMap('Maps/TextureMapSmall.jpg')
        self.terrain.setBruteforce(True)  # level of detail

        self.terrain.setBlockSize(32)
        self.terrain.setNear(50)
        self.terrain.setFar(100)
        self.terrain.setFocalPoint(base.camera)


        rootNP = self.terrain.getRoot()
        rootNP.reparentTo(render)
        rootNP.setSz(self.height)

        offset = img.getXSize() / 2.0 - 0.5
        rootNP.setPos(-offset, -offset, -self.height / 2.0)

        self.makeMapBorders(offset)
        self.terrain.generate()

        # creating vehicles
        #controlled vehicles
        self.controlVehicles = []
        self.controlVehicles.append(Vehicle(0, 00, 40, "B", self.worldNP, self.world))

        #vehicles goint to a specific point
        self.vehicles = []
        self.vehicles.append(Vehicle(0, 50, 40, "G", self.worldNP, self.world))
        thread.start_new_thread(goTo, ([100, -30], self.vehicles[0]))

        #vehicles following user
        self.followVehicles = []
        self.followVehicles.append(Vehicle(-offset+10, -offset+10, 40, "R", self.worldNP, self.world))
        self.followVehicles.append(Vehicle(offset-10, offset-10, 60, "R", self.worldNP, self.world))
        for veh in self.followVehicles:
            thread.start_new_thread(follow, (veh, self.controlVehicles[0]))
    #Borders around the map that vehicles won't fall from terrain
    def makeMapBorders(self, offset):
        plane1 = BulletPlaneShape(Vec3(1, 0, 0), 0)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('border1'))
        np.node().addShape(plane1)
        np.setPos(-offset, -offset, -self.height / 2.0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())
        plane2 = BulletPlaneShape(Vec3(0, 1, 0), 0)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('border2'))
        np.node().addShape(plane2)
        np.setPos(-offset, -offset, -self.height / 2.0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())
        plane3 = BulletPlaneShape(Vec3(0, -1, 0), 0)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('border3'))
        np.node().addShape(plane3)
        np.setPos(offset, offset, self.height / 2.0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())
        plane4 = BulletPlaneShape(Vec3(-1, 0, 0), 0)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('border4'))
        np.node().addShape(plane4)
        np.setPos(offset, offset, self.height / 2.0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())



sim = Simulation()
run()