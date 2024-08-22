from django.db import models
from django.contrib.auth.models import User  # imported for foreign key in cart table


# Create your models here.
class Product(models.Model):
    CAT=((1,'Mobile'),(2,'Shoes'),(3,'Cloths'),(4,'Cycle'))
    name = models.CharField(max_length=20,verbose_name='Product Name') # verbose_name='temp_name' is used for temp name on admin panel
    pdetail = models.CharField(max_length=100)
    cat = models.IntegerField(verbose_name='Category',choices=CAT) # choices are used to disply name of category mentioned in 'CAT' variable
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    pimage = models.ImageField(upload_to='image')  # to store img path 

    def __str__(self):
        return self.name
        
class Cart(models.Model):
    uid=models.ForeignKey('auth.User', on_delete=models.CASCADE,db_column='uid')  # db_column ='name' is used to rename the creted colun while column creation
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    uid=models.ForeignKey('auth.User', on_delete=models.CASCADE,db_column='uid')  # db_column ='name' is used to rename the creted colun while column creation
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()

class OrderHistory(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE, db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()
    


