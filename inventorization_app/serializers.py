from rest_framework import serializers
from .models import Products
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
import secrets
generate_token = secrets.token_urlsafe

class ApiSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Products
        fields = ('id', 
            'product_key', 
            'name', 
            'category',
            'owner')

    def create(self, validated_data):
        product = Products(
            name=validated_data['name'],
            product_key=validated_data['product_key'],
            category=validated_data['category'],
            allow_token = generate_token(10)
        )
        product.save()
        return product


class AcceptSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=20, default='') 
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        product_id = data['product_id']
        token = data['token']
        product = get_object_or_404(Products, id=product_id)
        if token != product.allow_token:
            raise serializers.ValidationError("Product.token is not equal to token")
        return data

    def create(self, validated_data):
        product = get_object_or_404(Products, id=validated_data['product_id'])
        user = get_object_or_404(User, id=validated_data['user_id'])
        product.owner = user
        product.save()
        return validated_data

    def update(self, instance, validated_data):
        product = get_object_or_404(Products, id=instance['product_id'])
        user = get_object_or_404(User, id=instance['user_id'])
        product.owner = user
        product.save()
        return instance

class DenySerializer(AcceptSerializer):
    def create(self, validated_data):
        product = get_object_or_404(Products, id=validated_data['product_id'])
        user = get_object_or_404(User, id=validated_data['user_id'])
        product.allow_token = generate_token()
        product.save()
        return validated_data

    def update(self, instance, validated_data):
        product = get_object_or_404(Products, id=instance['product_id'])
        user = get_object_or_404(User, id=instance['user_id'])
        product.allow_token = generate_token()
        product.save()
        return instance

class EmailSerializer(serializers.Serializer): 
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def send_mail(self, instance):
        request = self.context['request']
        product_id = instance['product_id']
        user_id = instance['user_id']
        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Products, id=product_id)
        product.allow_token = generate_token(10)
        product.save()
        domain_accept = request.build_absolute_uri(reverse('products:products-accept', kwargs={'user_id':user.id,'pk':product.id,'token':product.allow_token}))
        domain_deny = request.build_absolute_uri(reverse( 'products:products-deny', kwargs={'user_id':user.id,'pk':product.id,'token':product.allow_token}))
        context = {
            'product':product,
            'user':user,
            'domain_accept':domain_accept,
            'domain_deny':domain_deny} 
        subject, from_email, to = 'Borrow request', 'pythoninventorizationproject@gmail.com', 'pythoninventorizationproject@gmail.com'
        html_content = render_to_string('borrow_request.html', context) 
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def create(self, validated_data):
        self.send_mail(validated_data)
        return validated_data

    def update(self, instance, validated_data):
        self.send_mail(validated_data)
        return validated_data

class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Products.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'products')