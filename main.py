from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from Bird import Bird
from Controls import Controls


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

	def flockTask(self, task):
		for bird in self.birds:
			bird.move()

		return Task.cont


app = App(100)
cnt = Controls(app)

app.run()
