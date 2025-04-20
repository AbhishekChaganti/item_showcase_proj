from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image')
    url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name
