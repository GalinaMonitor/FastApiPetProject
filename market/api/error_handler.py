from market.models.operations import Error


class NotFoundException(Exception):
	def __init__(self):
		self.body = Error(code=404, message='Item not found').dict()
