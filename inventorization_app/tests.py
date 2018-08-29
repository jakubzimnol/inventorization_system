from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from .models import Products
User = get_user_model()

class InventorizationAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testuser', email='test@test.com')
        user_obj.set_password("randompassword")
        user.save()
        product = Products.objects.create(name='name',
                                          product_key=999,
                                          category='category',
                                          owner=user)
    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        
    def test_get_list(self):
        data = {}
        url = api_revers("products:list")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)