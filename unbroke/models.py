from django.db import models

class salary(models.Model):
	amount = models.IntegerField()
	frequency = models.IntegerField()
	monthlysalary = models.IntegerField()

	def __str__(self):
		return self.id
	
class income(models.Model):
	otherincome = models.IntegerField()
	total = models.IntegerField()
	
	def __str__(self):
		return self.id

class savings(models.Model):
	totalsavings = models.IntegerField()
	
	def __str__(self):
		return self.id

class wishlist(models.Model):
	prodname = models.CharField(max_length=255)
	prodamount = models.DecimalField(decimal_places=2, max_digits=12)
	progress = models.IntegerField()
	
	def __str__(self):
		return self.id