from __future__ import unicode_literals

from django.db import models

class Feature(models.Model):
	name = models.CharField(max_length=16)
	trim_function = models.TextField(max_length=1000)
	map_function = models.TextField(max_length=1000)
	reduce_function = models.TextField(max_length=1000)

	def __str__(self):
		return self.name
