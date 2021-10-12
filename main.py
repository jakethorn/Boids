from direct.showbase.ShowBase import ShowBase
from Bird import Bird
from Predator import Predator
from Controls import Controls


class Simulation(ShowBase):
	def __init__(self, numBirds, numPredators):
		super().__init__()

		# initialise birds
		self.birds = []
		for x in range(numBirds):
			self.birds.append(Bird(self))

		# initialise predators
		self.predators = []
		for x in range(numPredators):
			self.predators.append(Predator(self))

		# initialise keyboard/mouse controls
		self.controls = Controls(self)


sim = Simulation(numBirds=100, numPredators=3)
sim.run()
