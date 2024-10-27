from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50)
    des=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    Category=models.ForeignKey(Category,null=True,on_delete=models.CASCADE)
    image=models.FileField(upload_to='product_Image/')
    des=models.CharField(max_length=100)
    item_qty=models.IntegerField(null=True)
    # season=models.CharField(max_length=30,null=True)
    # company=models.CharField(max_length=30,null=True)
    
class Comments(models.Model):
    message = models.CharField(max_length = 255)
    owner_of_comment = models.CharField(max_length = 50)
    comment_reference = models.ForeignKey(Product,on_delete=models.CASCADE)
    review = models.CharField(max_length=10)