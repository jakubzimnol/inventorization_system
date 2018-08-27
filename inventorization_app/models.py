from django.db import models


class User(models.Model):
    def borrow_product(self, product_id):
        pass


class Admin(User):
    def create_pdf(self):
        pass

        
class Products(models.Model):
    product_key = models.IntegerField(default=0)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    owner = models.ForeignKey(User, null=True, on_delete= models.SET_NULL, related_name='my_products')



