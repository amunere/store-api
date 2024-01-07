from rest_framework import viewsets
from .models import Category, Product, Image, Discount
from .serializers import CategorySerializer, ProductSerializer, \
                        ProductImageSerializer, DiscountSerializer
from rest_framework import permissions
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows category to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product to be viewed or edited.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductImagesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product images to be viewed or edited.
    """   
    queryset = Image.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductCreateView(generics.CreateAPIView):
    """
    API endpoint that allows product create to be created.
    """  
    parser_class = [MultiPartParser, FormParser]
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class DiscountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows category to be viewed or edited.
    """
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]