from python.Lib.random import random
from direct.showbase import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import LPoint3f


def randPos(radius):
	return random() * radius - (radius/2)


def randRot():
	return random() * 360


class Bird:
	def __init__(self, app):
		self.app = app

		self.nodePath = app.loader.loadModel("models/jack")
		self.nodePath.reparentTo(app.render)
		self.nodePath.setPos(randPos(20), randPos(20), randPos(20))
		self.nodePath.setHpr(randRot(), randRot(), randRot())
		self.nodePath.setScale(.5, .75, .5)

		self.targetForward = self.getForward()

	def getForward(self):
		return self.app.render.getRelativeVector(self.nodePath, (0, 1, 0))

	def translate(self, translation):
		self.nodePath.setPos(self.nodePath.getPos() + translation)

	def move(self):
		# update target
		forward = self.getForward()
		toCenter = -self.nodePath.getPos().normalized()
		angle = forward.dot(toCenter)
		if self.nodePath.getPos().length() > 10 and angle < 0:
			self.targetForward = LPoint3f(randPos(5), randPos(5), randPos(5)) - self.nodePath.getPos().normalized()

		# update forward
		forward = forward + (self.targetForward - forward).normalized() * .05
		self.nodePath.lookAt(self.nodePath.getPos() + forward)

		# move forward
		self.translate(self.getForward() * .05)


class App(ShowBase):
	def __init__(self, num_birds):
		ShowBase.__init__(self)

		# initialise birds
		self.birds = []
		for x in range(num_birds):
			bird = Bird(self)
			self.birds.append(bird)

		self.taskMgr.add(self.flockTask, "FlockTask")

		# initialise camera
		self.camera.setPos(0, 50, 0)
		self.camera.lookAt(0, 0, 0)

		self.disableMouse()
		self.taskMgr.add(self.cameraTask, "CameraTask")

	def flockTask(self, task):
		for bird in self.birds:
			bird.move()

		return Task.cont

	def cameraTask(self, task):

		return Task.cont


class KeyboardHandler(DirectObject.DirectObject):
	def __init__(self):
		self.accept('mouse1', self.printHello)

	def printHello(self):
		print('Hello!')


kh = KeyboardHandler()

app = App(100)
app.run()
