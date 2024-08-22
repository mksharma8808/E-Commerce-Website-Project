from django.db import models

# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=100)
    # fname=models.CharField(max_length=50,null=True)
    email=models.EmailField()
    # gender=models.CharField(max_length=8,null=True)
    # phone=models.CharField(max_length=12)
    # address=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=20)
    # image=models.FileField(upload_to="customer_image/")

class Address(models.Model):
    cname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal = models.IntegerField()
    cust_reference = models.ForeignKey(Customer,on_delete=models.CASCADE)
