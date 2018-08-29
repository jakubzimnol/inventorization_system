from django.shortcuts import render
from .models import Products
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsAdminOrOwnerOrReadOnly, IsAdminOrReadOnly
from easy_pdf.views import PDFTemplateView
#from rest_framework import routers, viewsets
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .serializers import Api_serializer
from django.shortcuts import get_object_or_404
# from rlextra.rml2pdf import rml2pdf
# import cStringIO
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = Api_serializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = Api_serializer
    permission_classes = (IsAdminOrOwnerOrReadOnly,)
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
    

def generate_pdf(request):
    users = User.objects.all()
    #logic
    products = []
    for user in users:
        products.append( Products.objects.filter(id=user.id) )

    params = {
        'users': users,
        'products': products,
        'request': request
    }
    return render('pdf.html', params)


""" def products_generate_pdf(request):
    products = Products.objects.all()
    rml = getRML(products)  

    buf = cStringIO.StringIO()

    rml2pdf.go(rml, outputFileName=buf)
    buf.reset()
    pdfData = buf.read()
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response  """