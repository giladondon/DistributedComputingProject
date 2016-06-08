from __future__ import unicode_literals
import uuid
from django.db import models

class DCProcess(models.Model):
	process_name = models.CharField(max_length=16)
	trim_function = models.TextField(max_length=1000)
	map_function = models.TextField(max_length=1000)
	reduce_function = models.TextField(max_length=1000)
	process_code = models.CharField(max_length=1000, default='0'*32)

	def __str__(self):
		return self.process_name + ': ' + self.process_code

	@classmethod
	def create(cls, process_name, trim_function, map_function, reduce_function, process_code):
		process = cls(process_name=process_name, trim_function=trim_function, 
			map_function=map_function, reduce_function=reduce_function, process_code=process_code)
		process.save()
		return process
