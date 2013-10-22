"""
Here the product model is created and added to the database. It is changable from 
the admin page.
"""

from django.db import models

class ProductData(models.Model):
	product_code = models.CharField(max_length = 4)
	product_description = models.CharField(max_length = 25)
	product_price = models.DecimalField(max_digits = 6, decimal_places = 2)

	def __unicode__(self):
		return self.product_code
