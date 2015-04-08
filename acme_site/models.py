from django.db import models
import json

class TileLayout(models.Model):
	user_name = models.CharField(max_length=100)
	layout_name = models.CharField(max_length=100, default='layout1')
	board_layout = models.CharField(max_length=2000)
	mode = models.CharField(max_length=10, default='day')

	def save_layout(self, layout):
		self.board_layout = json.dumps(layout)

	def get_layout(self, layout):
		return json.loads(left.layout)