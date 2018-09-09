from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from easy_pdf.views import PDFTemplateView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAdminUser 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
import django_filters.rest_framework
from .models import Products
from .serializers import ApiSerializer
from .serializers import AcceptSerializer
from .serializers import DenySerializer
from .serializers import EmailSerializer
from .permissions import IsOwnerOrReadOnly
from .permissions import PermisionOr
import pdfkit
from django.template import loader
from django.http import HttpResponse
from rest_condition import Or

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ApiSerializer
    filter_backends = (filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
    search_fields = ('product_key', 'name', 'category')
    filter_fields = ('product_key', 'name', 'category')
    permission_classes = (IsAuthenticated, PermisionOr(IsAdminUser, IsOwnerOrReadOnly))
                                   
    def validate_and_response(self, serializer, data):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    @action(methods=['post'], detail=True, url_path=r'accept/(?P<user_id>\d+)/(?P<token>\w+)', url_name='accept', permission_classes = (IsAdminUser,))
    def accept_owner(self, request, user_id, pk, token):
        data = {'user_id':user_id,
                'product_id':pk,
                'token':token,}       
        serializer = AcceptSerializer(data=data)
        return self.validate_and_response(serializer, data)
                   
    @action(methods=['post'], detail=True, url_path=r'deny/(?P<user_id>\d+)/(?P<token>\w+)', url_name='deny', permission_classes = (IsAdminUser,))
    def deny_owner(self, request, user_id, pk, token):
        data = {'user_id':user_id,
                'product_id':pk,
                'token':token,}
        serializer = DenySerializer(data=data)
        return self.validate_and_response(serializer, data)

    @action(methods=['post'], detail=True, permission_classes = (IsAuthenticated,), url_name='email')
    def send_mail_to_admin(self, request, pk=None):
        user=request.user
        data = {'user_id':user.id,
                'product_id':pk,}
        serializer = EmailSerializer(data=data,context={'request':request})
        return self.validate_and_response(serializer, data)

    @action(methods=['post'], detail=False, url_path=r'createpdf', url_name='createpdf', permission_classes = (IsAdminUser,))
    def create_pdf(self, request):
        products = Products.objects.all()
        html = loader.render_to_string('product_list.html', {'products':products})
        output= pdfkit.from_string(html, output_path=False)
        response = HttpResponse(content_type="application/pdf")
        response.write(output)
        return response

            