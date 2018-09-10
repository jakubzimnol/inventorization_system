from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Products


class InventorizationAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User(username='testuser', email='test@test.com')
        cls.user.set_password("randompassword")
        cls.user.save()
        cls.my_admin = User.objects.create_superuser(
            'superuser', 'test@test.com', 'randompassword')
        cls.product = Products.objects.create(
            name='name', product_key=999, category='category', allow_token='1234567890',)
        cls.product_data = {"name": "some_name", "product_key": 1234, "category": "category", }
        cls.empty_data = {}
        cls.token_data = {'pk': cls.product.pk, 'user_id': cls.user.id, 'token': '1234567890'}
        cls.delete_data = {'id': 1}
        cls.url_list = reverse("products:products-list")
        cls.url_detail = reverse("products:products-detail", kwargs={'pk': cls.product.pk})
        cls.url_email = reverse("products:products-email", kwargs={'pk': cls.product.pk})
        cls.url_createpdf = reverse("products:products-createpdf")
        cls.url_accept = reverse("products:products-accept", kwargs= cls.token_data)
        cls.url_deny = reverse("products:products-deny", kwargs= cls.token_data)

    def setUp(self):
        super().setUp()

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_get_list(self):
        response = self.client.get(self.url_list, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_autohorized(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url_list, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        response = self.client.post(self.url_list, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_item_authorized(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url_list, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_item_super_authorized(self):
        self.client.force_login(self.my_admin)
        response = self.client.post(self.url_list, self.product_data, format='json')
        # import pdb;pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_item(self):
        response = self.client.get(self.url_detail, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_item_authorized(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url_detail, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        response = self.client.put(self.url_detail, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_item_authorized(self):
        self.client.force_login(self.user)
        response = self.client.put(self.url_detail, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_item_super_authorized(self):
        self.client.force_login(self.my_admin)
        response = self.client.put(self.url_detail, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        response = self.client.delete(self.url_detail, self.delete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_item_authorized(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url_detail, self.delete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_item_super_authorized(self):
        self.client.force_login(self.my_admin)
        response = self.client.delete(self.url_detail, self.delete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_email_send(self):
        response = self.client.post(self.url_email, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_email_send_authorized(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url_email, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pdf_create(self):
        response = self.client.post(self.url_createpdf, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pdf_create_authorized(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url_createpdf, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pdf_create_super_authorized(self):
        self.client.force_login(self.my_admin)
        response = self.client.post(self.url_createpdf, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept(self):
        response = self.client.post(self.url_accept, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_authorized(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url_accept, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_super_authorized(self):
        self.client.force_login(self.my_admin)
        response = self.client.post(self.url_accept, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deny(self):
        response = self.client.post(self.url_deny, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_authorized(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url_deny, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_super_authorized(self):
        self.client.force_login(self.my_admin)
        response = self.client.post(self.url_deny, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
