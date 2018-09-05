from django.db import models

        
class Products(models.Model):
    product_key = models.IntegerField(default=0)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    owner = models.ForeignKey('auth.User', related_name='products', blank=True, null=True, on_delete=models.SET_NULL)
    allow_token = models.CharField(max_length=10, default='')
    def get_api_url(self):
        return api_reverse("products:detail", kwargs={'pk':self.id})
