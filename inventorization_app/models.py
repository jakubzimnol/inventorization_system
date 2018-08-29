from django.db import models

        
class Products(models.Model):
    product_key = models.IntegerField(default=0)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    owner = models.ForeignKey('auth.User', related_name='products', null=True, on_delete=models.SET_NULL)
    #owner = models.ForeignKey(User, null=True, on_delete= models.SET_NULL, related_name='my_products')



