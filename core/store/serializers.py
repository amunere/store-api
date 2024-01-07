from rest_framework import serializers
from .models import Category, Product, Image, Discount


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    """
    parent_category = Category.objects.all()

    class Meta:
        model = Category
        fields = ['id', 'url', 'name', 'desc', 'parent_category', 
                  'page_title', 'meta_keywords', 
                  'meta_description', 'available', 'creater']


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Product image serializer
    """
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer
    """
    images =  ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'desc', 'SKU', 'category', 'quantity', 
                  'price', 'discount', 'height', 'length', 
                  'width', 'weight', 'available', 'page_title', 'meta_keywords', 
                  'meta_description', 'creater', 'images', 'uploaded_images']


    def create(self, validated_data):
        """
        Create and return a new Product instance, given the validated data.
        """
        uploaded_images = validated_data.pop('uploaded_images')  
        product = Product.objects.create(**validated_data)
        
        # save product images
        for image in uploaded_images:
            Image.objects.create(product=product, image=image, thumbnail=image)

        return product


class DiscountSerializer(serializers.ModelSerializer):
    """
    Discount serializer
    """
    class Meta:
        model = Discount
        fields = ['url', 'name', 'desc', 'discount_percent', 'active']