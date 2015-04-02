from django.db import models
import json

class TileLayout(models.Model):
	user_name = models.CharField(max_length=100)
	board_layout = models.CharField(max_length=500)

	def save_layout(self, layout):
		self.board_layout = json.dumps(layout)

	def get_layout(self, layout):
		return json.loads(left.layout)