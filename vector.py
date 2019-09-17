from math import sqrt
class Vector:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def normalize(self):
		length = sqrt(self.x**2 + self.y**2 + self.z**2)
		self.x = self.x/length
		self.y = self.y/length
		self.z = self.z/length
	def __str__(self):
		return str(self.x) + " " + str(self.y) + " " + str(self.z)