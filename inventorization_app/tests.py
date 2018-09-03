from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from .models import Products
User = get_user_model()

from rest_framework_jwt.settings import api_settings
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

class InventorizationAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testuser', email='test@test.com')
        user_obj.set_password("randompassword")
        user_obj.save()
        User.objects.create_superuser('superuser', 'test@test.com', 'randompassword')
        
        user_obj.save()        
        product = Products.objects.create(name='name',
                                          product_key=999,
                                          category='category',
                                          owner=user_obj)
    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)
        
    def test_get_list(self):
        data = {}
        url = api_reverse("products:list")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_post_item(self):
        data = {"name":"some_name", "product_key":1234}
        url = api_reverse("products:create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    
        
    #def test_get_item(self):
        #product = Products.objects.first()
        #data = {}
        #url = api_reverse("products:detail", kwargs={'pk':product.pk})
        #response = self.client.get(url, data, format='json')
        #print(response.data)
        #self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    #def test_udate_item(self):
        #product = Products.objects.first()
        #data = {"name":"some_name", "product_key":1234}
        #url = api_reverse("products:detail", kwargs={'pk':product.pk})
        #response = self.client.put(url, data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
        
    def test_udate_item_authorized(self):
        user = User.objects.first()
        payload = payload_handler(user)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        product = Products.objects.first()
        data = {"name":"some_name", "product_key":1234}
        url = api_reverse("products:detail", kwargs={'pk':product.pk})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_item_authorized(self):
        user = User.objects.first()
        payload = payload_handler(user)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        product = Products.objects.first()
        data = {}
        url = api_reverse("products:detail", kwargs={'pk':product.pk})
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
    
    def test_udate_item_super_authorized(self):
        super_user = User.objects.get(username='superuser')
        payload = payload_handler(super_user)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        product = Products.objects.first()
        data = {"name":"some_name", "product_key":1234}
        url = api_reverse("products:detail", kwargs={'pk':product.pk})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)       