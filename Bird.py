from python.Lib.random import random
from direct.task import Task
from panda3d.core import LPoint3f


def randPos(radius):
	return random() * radius - (radius / 2)


def randRot():
	return random() * 360


class Bird:
	def __init__(self, sim):
		self.sim = sim

		# initialise 3d model
		self.nodePath = self.sim.loader.loadModel("models/jack")
		self.nodePath.reparentTo(self.sim.render)
		self.nodePath.setPos(randPos(20), randPos(20), randPos(20))
		self.nodePath.setHpr(randRot(), randRot(), randRot())
		self.nodePath.setScale(.5, .75, .5)

		# initialise movement direction
		self.targetForward = self.getForward()

		# start movement task
		def move_task(task):
			self.move()
			return Task.cont

		self.sim.taskMgr.add(move_task, "Move")

	def getForward(self):
		return self.sim.render.getRelativeVector(self.nodePath, (0, 1, 0))

	def getClosestPredator(self):
		closest = self.sim.predators[0].nodePath.getPos()
		for predator in self.sim.predators:
			closestDistance = (closest - self.nodePath.getPos()).length()
			currentDistance = (predator.nodePath.getPos() - self.nodePath.getPos()).length()
			if currentDistance < closestDistance:
				closest = predator.nodePath.getPos()

		return closest

	def getFearVector(self):
		predator = self.getClosestPredator()
		toPredator = predator - self.nodePath.getPos()
		return -toPredator.normalized()

	def translate(self, translation):
		self.nodePath.setPos(self.nodePath.getPos() + translation)

	def basicMove(self):
		# update target
		toCenter = -self.nodePath.getPos().normalized()
		angle = self.targetForward.dot(toCenter)
		if self.nodePath.getPos().length() > 10 and angle < 0:
			self.targetForward = LPoint3f(randPos(5), randPos(5), randPos(5)) - self.nodePath.getPos().normalized()

		# update forward
		forward = self.getForward()
		turning = forward + (self.targetForward - forward).normalized() * .05
		self.nodePath.lookAt(self.nodePath.getPos() + turning)

		# move forward
		self.translate(self.getForward() * .05)

	def preyMove(self):
		# update target
		# stay within bounds
		toCenter = -self.nodePath.getPos().normalized()
		angle = self.targetForward.dot(toCenter)
		if self.nodePath.getPos().length() > 10 and angle < 0:
			self.targetForward = LPoint3f(randPos(5), randPos(5), randPos(5)) - self.nodePath.getPos().normalized()

		# stay away from predators
		if len(self.sim.predators) > 0:
			predator = self.getClosestPredator()
			if (predator - self.nodePath.getPos()).length() < 5:
				self.targetForward = self.getFearVector()

		# update forward
		forward = self.getForward()
		turning = forward + (self.targetForward - forward).normalized() * .05
		self.nodePath.lookAt(self.nodePath.getPos() + turning)

		# move forward
		self.translate(self.getForward() * .05)

	def move(self):
		self.preyMove()

	def flock(self, allBirds):
		# rule 1: separation
		# rule 2: alignment
		# rule 3: cohesion
		return None
