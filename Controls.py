from direct.showbase import DirectObject
from direct.task import Task
from panda3d.core import WindowProperties


class Controls(DirectObject.DirectObject):
	def __init__(self, sim):
		self.sim = sim

		# disable default control scheme
		self.sim.disableMouse()

		# initialise camera position/orientation
		self.sim.camera.setPos(0, 50, 0)
		self.sim.camera.lookAt(0, 0, 0)

		# keyboard controls: map buttons to controls
		buttons = {"w": (0, 1, 0), "a": (-1, 0, 0), "s": (0, -1, 0), "d": (1, 0, 0)}
		for k, v in buttons.items():
			self.accept(k, self.moveCamera, [v])
			self.accept(f"{k}-up", self.stopCamera, [v])

		# mouse controls
		self.setMouseVisibility(False)
		self.sim.taskMgr.add(self.turnCamera_task, "TurnCamera")

	def setMouseVisibility(self, visible):
		props = WindowProperties()
		props.setCursorHidden(not visible)
		self.sim.win.requestProperties(props)

	def moveCamera(self, direction):
		self.sim.taskMgr.add(self.moveCamera_task, "Cam_" + str(direction), extraArgs=[direction])

	def moveCamera_task(self, direction):
		relativeDir = self.sim.render.getRelativeVector(self.sim.camera, direction)
		self.sim.camera.setPos(self.sim.camera.getPos() + relativeDir)
		return Task.cont

	def stopCamera(self, direction):
		self.sim.taskMgr.remove("Cam_" + str(direction))

	def turnCamera_task(self, task):
		if self.sim.mouseWatcherNode.hasMouse():
			x = self.sim.mouseWatcherNode.getMouseX()
			y = self.sim.mouseWatcherNode.getMouseY()
			self.sim.camera.setHpr(self.sim.camera.getHpr() + (-x * 30, y * 30, 0))

			props = self.sim.win.getProperties()
			self.sim.win.movePointer(0, props.getXSize() // 2, props.getYSize() // 2)

		return Task.cont
