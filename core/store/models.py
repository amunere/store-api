import PIL
from django.db import models
from pytils.translit import slugify
from django.conf import settings
from account.models import User
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Category(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=55, unique=True)
    desc = models.TextField(max_length=300)
    slug = models.SlugField(max_length=80, unique=True)
    parent_category = models.ForeignKey('self', related_name='children', 
                                           on_delete=models.SET_NULL, null=True, blank=True)
    # seo fields 
    page_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)    
    meta_description = models.TextField(null=True, blank=True)
    # seo fields end
    available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
       
    def __str__(self):
        return self.name


class Product(models.Model):
    creater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=120)
    SKU = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = 'Category', related_name = 'categories_products')
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='Price') 
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, null=True, blank=True)
    discount_price = models.PositiveIntegerField(verbose_name='Discount price', null=True, blank=True)
    height = models.CharField(max_length=100, null=True, blank=True)
    length = models.CharField(max_length=100, null=True, blank=True)
    width = models.CharField(max_length=100, null=True, blank=True)
    weight = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True)
    available = models.BooleanField(default=False)
    # seo fields 
    page_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)    
    meta_description = models.TextField(null=True, blank=True)
    # seo fields end
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.discount and self.discount.active:
            self.discount_price = self.price-round(self.price*(self.discount.discount_percent/100))
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/image/%Y/%m/%d/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='products/thumb/%Y/%m/%d/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = PIL.Image.open(self.image)
        width, height = image.size
        if width > 1980 or height > 1080:
            image = image.resize((1980, 1080), PIL.Image.Resampling.LANCZOS)  
        image.save(self.image.path, quality=90)                
        
        thumb = PIL.Image.open(self.thumbnail) 
        thumb = thumb.resize((128, 128), PIL.Image.Resampling.LANCZOS)             
        thumb.save(self.thumbnail.path, quality=90)        

    def __str__(self):
        return f"id: {self.pk} {self.thumbnail}"


class Discount(models.Model):
    name = models.CharField(max_length=55)
    desc = models.TextField(max_length=100)
    discount_percent = models.PositiveIntegerField(validators=PERCENTAGE_VALIDATOR, verbose_name='Discount price')
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name