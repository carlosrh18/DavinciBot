from django.db import models

# Create your models here.
class Messages(models.Model):
	body = models.CharField(max_length=200)

	def __str__(self):
		return self.body


# Food order model
class FoodOrder(models.Model):
	Table = models.IntegerField()
	MenuPick = models.IntegerFIeld()
	Instruc = models.TextField()
	coupon = models.CharField(max_length=10, blank=True)
	