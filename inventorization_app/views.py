from .models import Products
from django.shortcuts import render
#from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsAdminOrOwnerOrReadOnly
from easy_pdf.views import PDFTemplateView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import Api_serializer
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import viewsets
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse

def send_mail_to_admin(request, pk=None):
    user=request.user
    product = get_object_or_404(Products, id=pk)
    #product.access_token = GENERATE_USING_HASH_FUNCTION()
    #product.deny_token = GENERATE_USING_HASH_FUNCTION()  
    #product.save()
    #product = get_object_or_404(Products, id=pk)
    #message = user.username + ' wants to borrow ' +product.name+ '. Do you agree?'    
    domain_accept = request.build_absolute_uri(reverse('products:deny_access', args=[product.id,]))
    domain_deny = request.build_absolute_uri(reverse( 'products:deny_access', args=[product.id]))
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
    
    
    #user = request.user


    #send_mail(
        #'Borrow request',
        #message,
        #'pythoninventorizationproject@gmail.com',
        #['pythoninventorizationproject@gmail.com'],
         #fail_silently=False,
    #)
    return render(request, 'test.html')

class CheckAcessView(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ProductListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = Api_serializer
    permission_classes = (IsAuthenticated,)

class ProductCreateView(generics.CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = Api_serializer
    permission_classes = (IsAdminUser,)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = Api_serializer
    permission_classes = (IsAdminOrOwnerOrReadOnly, IsAuthenticated, )
    def get_queryset(self):
        productc = Products.objects.filter(id=self.kwargs['pk'])
        return productc


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