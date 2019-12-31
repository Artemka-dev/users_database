from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserObj(models.Model):
	user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

	name = models.CharField(max_length=150, db_index=True)
	phone_number = models.CharField(max_length=20, blank=True, db_index=True, unique=True)
	email = models.EmailField(max_length=70, blank=True, null= True, unique= True, db_index=True)
	address = models.CharField(max_length=150, blank=True, db_index=True)
	description = models.TextField(db_index=True, blank=True)
	date_pub = models.DateField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return self.name
