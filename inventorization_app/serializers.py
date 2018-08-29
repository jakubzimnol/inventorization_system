from rest_framework import serializers
from .models import Products
from django.contrib.auth.models import User

class Api_serializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Products
        fields = (
            'id', 
            'product_key', 
            'name', 
            'category',
            'owner')

class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Products.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'products')