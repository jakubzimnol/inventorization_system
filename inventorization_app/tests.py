from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status
#from rest_framework.reverse import reverse as reverse
from .models import Products 
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()

# class AutherizationDetailApiTestCase(APITestCase):
#     def __init__(self, url, data, proper_status):
#         self.url = url
#         self.data = data
#         self.proper_status = proper_status
        
#     @classmethod
#     def setUpTestData(cls):    
#         cls.user= User(username='testuser', email='test@test.com')
#         cls.user.set_password("randompassword")
#         cls.user.save()
#         cls.my_admin = User.objects.create_superuser(
#             'superuser', 'test@test.com', 'randompassword')

#     def test_not_authorized(self):
#         response = self.client.get(self.url, self.data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_authorization(self):
#         self.client.force_login(self.user)
#         response = self.client.get(self.url, self.data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_super_authorization(self):
#         self.client.force_login(self.my_admin)
#         response = self.client.get(self.url, self.data, format='json')
#         self.assertEqual(response.status_code, self.proper_status)


class InventorizationAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Products.objects.create(
            name='name', product_key=999, category='category',)
        cls.product_data = {"name":"some_name", "product_key":1234, "category":"category"}
        cls.empty_data = {}
        cls.url_list = reverse("products:products-list")
        cls.url_detail = reverse("products:products-detail", kwargs={'pk':cls.product.pk})
        cls.url_email = reverse("products:products-email", kwargs={'pk':cls.product.pk})
        cls.url_createpdf = reverse("products:products-createpdf")
        cls.user= User(username='testuser', email='test@test.com')
        cls.user.set_password("randompassword")
        cls.user.save()
        cls.my_admin = User.objects.create_superuser(
            'superuser', 'test@test.com', 'randompassword')

    def setUp(self):
        super()
        pass

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
        #import pdb;pdb.set_trace()
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

    def test_udate_item_super_authorized(self):
        self.client.force_login(self.my_admin)
        response = self.client.put(self.url_detail, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_item(self):
    #     response = self.client.delete(self.url_detail, self.product_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

    # def test_delete_item_authorized(self):
    #     self.client.force_login(self.user)
    #     response = self.client.delete(self.url_detail, self.product_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_delete_item_super_authorized(self):
    #     self.client.force_login(self.my_admin)
    #     response = self.client.delete(self.url_detail, self.product_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_accepting(self):
        pass

    # def test_dening(self):
    #     pass

    
        #   data = {"name":"some_name", 
        #         "product_key":1234}
        # # factory = APIRequestFactory()
        # user = User.objects.first()
        # product = Products.objects.first()
        # # view = ProductCreateView.as_view()
        # url = reverse("products:detail", kwargs={'pk':product.pk})
        # self.client.login(username=user.username, password=user.password)
        # response = self.client.get(url, data, format='json')
        # #self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        # # url = reverse("products:detail", kwargs={'pk':product.pk})
        # # request = factory.put(url, data, format='json')
        # # force_authenticate(request, user=user)
        # # view = ProductCreateView.as_view()
        # # response = view(request)
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    # def test_get_item_authorized(self):
    #     user = User.objects.first()
    #     factory = APIRequestFactory()
    #     product = Products.objects.first()
    #     data = {}
    #     url = reverse("products:detail", kwargs={'pk':product.pk})
    #     request = factory.get(url, data, format='json')
    #     force_authenticate(request, user=user) 
    #     view = ProductListView.as_view()
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)       
    # 

