from direct.showbase import DirectObject
from direct.task import Task


class Controls(DirectObject.DirectObject):
	def __init__(self, app):
		self.app = app
		self.app.disableMouse()

		self.mouseX = None
		self.mouseY = None

		self.accept("w", self.moveCamera, ["forward"])
		self.accept("a", self.moveCamera, ["left"])
		self.accept("s", self.moveCamera, ["back"])
		self.accept("d", self.moveCamera, ["right"])

		self.accept("w-up", self.stopCamera, ["forward"])
		self.accept("a-up", self.stopCamera, ["left"])
		self.accept("s-up", self.stopCamera, ["back"])
		self.accept("d-up", self.stopCamera, ["right"])

		self.accept("mouse3", self.turnCamera)
		self.accept("mouse3-up", self.stopCamera, ["turn"])

	def moveCamera(self, direction):
		self.app.taskMgr.add(self.moveCamera_task, "Camera_" + direction, extraArgs=[direction])

	def moveCamera_task(self, direction):
		if direction == "forward":
			forward = self.app.render.getRelativeVector(self.app.camera, (0, 1, 0))
			self.app.camera.setPos(self.app.camera.getPos() + forward)
		elif direction == "back":
			forward = self.app.render.getRelativeVector(self.app.camera, (0, -1, 0))
			self.app.camera.setPos(self.app.camera.getPos() + forward)
		elif direction == "left":
			forward = self.app.render.getRelativeVector(self.app.camera, (-1, 0, 0))
			self.app.camera.setPos(self.app.camera.getPos() + forward)
		elif direction == "right":
			forward = self.app.render.getRelativeVector(self.app.camera, (1, 0, 0))
			self.app.camera.setPos(self.app.camera.getPos() + forward)

		return Task.cont

	def stopCamera(self, direction):
		self.app.taskMgr.remove("Camera_" + direction)

	def turnCamera(self):
		self.mouseX = self.app.mouseWatcherNode.getMouseX()
		self.mouseY = self.app.mouseWatcherNode.getMouseY()
		self.app.taskMgr.add(self.turnCamera_task, "Camera_turn")

	def turnCamera_task(self, task):
		x = self.app.mouseWatcherNode.getMouseX()
		y = self.app.mouseWatcherNode.getMouseY()

		dx = self.mouseX - x
		dy = self.mouseY - y

		self.app.camera.setHpr(self.app.camera.getHpr() + (dx * 30, -dy * 30, 0))

		self.mouseX = x
		self.mouseY = y

		return Task.cont
