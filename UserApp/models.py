from django.db import models

# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    

class Address(models.Model):
    cname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal = models.IntegerField()
    cust_reference = models.ForeignKey(Customer,on_delete=models.CASCADE)

class Profile(models.Model):
    name = models.CharField(max_length=100)
    fname = models.CharField(max_length=50,null=True)
    gender = models.CharField(max_length=8,null=True)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=100,null=True)
    image = models.FileField(upload_to="customer_image/",null=True)
    reference = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)