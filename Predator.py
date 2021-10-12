from Bird import Bird


class Predator(Bird):
	def __init__(self, app):
		super().__init__(app)
		self.nodePath.setColor(1, 0, 0, 1)

	def move(self):
		self.basicMove()
