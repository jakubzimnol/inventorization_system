import pdfkit
from django.http import HttpResponse
from django.template import loader
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Products
from .permissions import IsOwnerOrReadOnly, IsAdmin
from .permissions import permision_or
from .serializers import AcceptSerializer
from .serializers import ApiSerializer
from .serializers import DenySerializer
from .serializers import EmailSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ApiSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('product_key', 'name', 'category')
    filter_fields = ('product_key', 'name', 'category')
    permission_classes = (IsAuthenticated, permision_or(IsAdmin, IsOwnerOrReadOnly))

    def validate_and_response(self, serializer, data):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path=r'accept/(?P<user_id>\d+)/(?P<token>\w+)', url_name='accept',
            permission_classes=(IsAdminUser,))
    def accept_owner(self, request, user_id, pk, token):
        data = {'user_id': user_id,
                'product_id': pk,
                'token': token, }
        serializer = AcceptSerializer(data=data)
        return self.validate_and_response(serializer, data)

    @action(methods=['post'], detail=True, url_path=r'deny/(?P<user_id>\d+)/(?P<token>\w+)', url_name='deny',
            permission_classes=(IsAdminUser,))
    def deny_owner(self, request, user_id, pk, token):
        data = {'user_id': user_id,
                'product_id': pk,
                'token': token, }
        serializer = DenySerializer(data=data)
        return self.validate_and_response(serializer, data)

    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated,), url_name='email')
    def send_mail_to_admin(self, request, pk=None):
        user = request.user
        data = {'user_id': user.id,
                'product_id': pk, }
        serializer = EmailSerializer(data=data, context={'request': request})
        return self.validate_and_response(serializer, data)

    @action(methods=['post'], detail=False, url_path=r'createpdf', url_name='createpdf',
            permission_classes=(IsAdminUser,))
    def create_pdf(self, request):
        products = Products.objects.all()
        html = loader.render_to_string('product_list.html', {'products': products})
        output = pdfkit.from_string(html, output_path=False)
        response = HttpResponse(content_type="application/pdf")
        response.write(output)
        return response
