from math import pi, sin, cos
import sys

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CompassEffect, WindowProperties, VBase4, PointLight, CardMaker, CollisionRay, CollisionNode, \
    CollisionHandlerQueue, CollisionHandlerFloor, CollisionTraverser, CollisionSphere, TextNode, CollisionBox, Point3, \
    GeomNode
from PIL import Image
from tinydb import TinyDB


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.scene = self.loader.loadModel("models/test.egg")
        self.scene.reparentTo(self.render)
        self.scene.setScale(1, 3, 1)
        # self.scene.setPos(0, 1000, 0)
        sphere = CollisionSphere(0, 0, 0, 50)
        cnode = self.scene.attachNewNode(CollisionNode('cnode_scene'))
        cnode.node().addSolid(sphere)
        # cnode.show()

        base.setBackgroundColor(0, 0.0, 0)

        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        OnscreenText(text='.', pos=(0, 0, 0))

        plight = PointLight('plight')
        plight.setColor(VBase4(2, 2, 2, 1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(0, 0, 100)
        self.render.setLight(plnp)

        # dummy node for camera, attach player to it
        self.camparent = self.render.attachNewNode('camparent')
        self.camparent.reparentTo(self.render)  # inherit transforms
        self.camparent.setEffect(CompassEffect.make(self.render))  # NOT inherit rotation
        self.camparent.setY(-1000)
        self.camparent.setZ(200)

        # the camera
        base.camera.reparentTo(self.camparent)
        base.camera.lookAt(self.camparent)
        base.camera.setY(0)  # camera distance from model

        self.heading = 0
        self.pitch = 0

        self.taskMgr.add(self.cameraTask, 'cameraTask')

        self.keyMap = {
            "left": 0, "right": 0, "forward": 0, "reverse": 0}

        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left", True])
        self.accept("arrow_right", self.setKey, ["right", True])
        self.accept("arrow_up", self.setKey, ["forward", True])
        self.accept("arrow_down", self.setKey, ["reverse", True])
        self.accept("w", self.setKey, ["forward", True])
        self.accept("a", self.setKey, ["left", True])
        self.accept("s", self.setKey, ["reverse", True])
        self.accept("d", self.setKey, ["right", True])
        self.accept("arrow_left-up", self.setKey, ["left", False])
        self.accept("arrow_right-up", self.setKey, ["right", False])
        self.accept("arrow_up-up", self.setKey, ["forward", False])
        self.accept("arrow_down-up", self.setKey, ["reverse", False])
        self.accept("w-up", self.setKey, ["forward", False])
        self.accept("a-up", self.setKey, ["left", False])
        self.accept("s-up", self.setKey, ["reverse", False])
        self.accept("d-up", self.setKey, ["right", False])
        self.accept('mouse1', self.myFunction)

        self.textObject = None

        db = TinyDB('paintings/db.json')
        self.descriptions = dict()

        base.cTrav = CollisionTraverser()

        pickerNode = CollisionNode('mouseRay')
        pickerNP = self.camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        self.queue = CollisionHandlerQueue()
        base.cTrav.addCollider(pickerNP, self.queue)

        id = 0
        for item in db.all():
            self.addImage('paintings/' + item['img'], id=id)
            self.descriptions[id] = item['name']
            id += 1

    def addImage(self, filename='../Artwork/022waVoF8tbU.jpg', name='NAME', id=0):
        cm = CardMaker('card_' + str(id))
        max_width = 120
        with Image.open(filename) as img:
            width, height = img.size
        cm.setFrame(0, max_width, 0, height * max_width * 1. / width)
        card = self.render.attachNewNode(cm.generate())
        card.setPos(-270, 100 - id * max_width * 1.5, (300 - height * max_width * 1. / width) * 0.5)
        # card.setPos(-5, 100, 125)
        card.setHpr(90, 0, 0)

        box = CollisionBox(Point3(), max_width, 1, height * max_width * 1. / width)
        cnodePath = card.attachNewNode(CollisionNode('cnode'))
        cnodePath.node().addSolid(box)
        # cnodePath.show()
        card.setTag('myObjectTag', str(id))

        tex = loader.loadTexture(filename)
        # tex = self.loader.loadTexture('maps/noise.rgb')
        card.setTexture(tex)

    def myFunction(self):
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

        base.cTrav.traverse(self.render)
        # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
        if self.queue.getNumEntries() > 0:
            # This is so we get the closest object.
            self.queue.sortEntries()
            pickedObj = self.queue.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetTag('myObjectTag')
            if not pickedObj.isEmpty():
                if self.textObject:
                    self.textObject.destroy()
                id = int(str(pickedObj)[12:])
                print id
                self.textObject = OnscreenText(text=self.descriptions[id], pos=(0, -0.4), scale=0.07, shadow=(1, 1, 1, 1))
            else:
                if self.textObject:
                    self.textObject.destroy()
                self.textObject = None

    def setKey(self, key, value):
        self.keyMap[key] = value

    # camera rotation task
    def cameraTask(self, task):

        md = base.win.getPointer(0)

        x = md.getX()
        y = md.getY()

        cam_speed = 0.05
        mid = [base.win.getXSize() / 2, base.win.getYSize() / 2]
        if base.win.movePointer(0, mid[0], mid[1]):
            self.heading = self.heading - (x - mid[0]) * cam_speed
            self.pitch = self.pitch - (y - mid[1]) * cam_speed

        self.camparent.setHpr(self.heading, self.pitch, 0)

        speed = 4
        if self.keyMap['forward']:
            self.camparent.setY(base.cam, self.camparent.getY(base.cam) + speed)
        if self.keyMap['reverse']:
            self.camparent.setY(base.cam, self.camparent.getY(base.cam) - speed)
        if self.keyMap['left']:
            self.camparent.setX(base.cam, self.camparent.getX(base.cam) - speed)
        if self.keyMap['right']:
            self.camparent.setX(base.cam, self.camparent.getX(base.cam) + speed)

        return task.cont


app = MyApp()
app.run()
