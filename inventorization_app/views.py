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
from .permissions import IsAdminOrOwnerOrReadOnly


class ProductViewSet(viewsets.ViewSet):
    serializer_class = ApiSerializer
    permission_classes_by_action = {'list': [IsAuthenticated],
                                   'create': [IsAdminUser],
                                   'retrieve': [IsAuthenticated],
                                   'update': [IsAdminOrOwnerOrReadOnly, IsAuthenticated],
                                   'destroy': [IsAdminUser],
                                   'accept_owner': [IsAdminUser],
                                   'deny_owner': [IsAdminUser],
                                   'send_mail_to_admin': [IsAuthenticated],}
                                   
    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def list(self, request):
        queryset = Products.objects.all()
        serializer = ApiSerializer(queryset, many=True)
        filter_backends = (filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
        search_fields = ('product_key', 'name', 'category')
        filter_fields = ('product_key', 'name', 'category')
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Products.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ApiSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Products.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ApiSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        serializer = ApiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ApiSerializer(product)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path=r'accept/(?P<user_id>\d+)/(?P<token>\w+)', url_name='accept')
    def accept_owner(self, request, user_id, pk, token):
        data = {'user_id':user_id,
                'product_id':pk,
                'token':token,}
        serializer = AcceptSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
    @action(methods=['post'], detail=True, url_path=r'deny/(?P<user_id>\d+)/(?P<token>\w+)', url_name='deny')
    def deny_owner(self, request, user_id, pk, token):
        data = {'user_id':user_id,
                'product_id':pk,
                'token':token,}
        serializer = DenySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True)
    def send_mail_to_admin(self, request, pk=None):
        user=request.user
        data = {'user_id':user.id,
                'product_id':pk,}
        serializer = EmailSerializer(data=data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListPDFView(PDFTemplateView):
    template_name = 'product_list.html'
    permission_classes = (IsAdminUser,)   
    def get_context_data(self, **kwargs):
        products = Products.objects.all()
        print(products)
        return super(ProductListPDFView, self).get_context_data(
            pagesize='A4',
            products=products,
            **kwargs
        )    