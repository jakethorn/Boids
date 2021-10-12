from Bird import Bird


class Predator(Bird):
	def __init__(self, sim):
		super().__init__(sim)
		self.nodePath.setColor(1, 0, 0, 1)

	def move(self):
		self.basicMove()
