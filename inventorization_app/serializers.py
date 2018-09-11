import secrets

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from rest_framework import serializers

from .models import Products

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
            allow_token=generate_token(10)
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

    def change_owner(self, instantce):
        product = get_object_or_404(Products, id=instantce['product_id'])
        user = get_object_or_404(User, id=instantce['user_id'])
        product.owner = user
        product.save()
        return instantce

    def create(self, validated_data):
        return self.change_owner(validated_data)

    def update(self, instance, validated_data):
        return self.change_owner(validated_data)


class DenySerializer(AcceptSerializer):
    def reset_token(self, instance):
        product = get_object_or_404(Products, id=instance['product_id'])
        user = get_object_or_404(User, id=instance['user_id'])
        product.allow_token = generate_token()
        product.save()
        return instance

    def create(self, validated_data):
        return self.reset_token(validated_data)

    def update(self, instance, validated_data):
        return self.reset_token(validated_data)


class EmailSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def generate_product_token(self, product):
        product.allow_token = generate_token(10)
        product.save()

    def get_data_from_db(self, validated_data):
        request = self.context['request']
        product_id = validated_data['product_id']
        user_id = validated_data['user_id']
        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Products, id=product_id)
        self.generate_product_token(product)
        return user, product, request

    def generate_mail_message(self, user, product, request):
        url_data = {'user_id': user.id, 'pk': product.id, 'token': product.allow_token}
        domain_accept = request.build_absolute_uri(reverse('products:products-accept', kwargs=url_data))
        domain_deny = request.build_absolute_uri(reverse('products:products-deny', kwargs=url_data))
        context = {'product': product, 'user': user, 'domain_accept': domain_accept, 'domain_deny': domain_deny}
        subject, from_email = 'Borrow request', 'pythoninventorizationproject@gmail.com'
        to = 'pythoninventorizationproject@gmail.com'
        html_content = render_to_string('borrow_request.html', context)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        return msg, html_content

    def send_mail(self, validated_data):
        user, product, request = self.get_data_from_db(validated_data)
        msg, html_content = self.generate_mail_message(user, product, request)
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
