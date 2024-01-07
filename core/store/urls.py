from django.urls import include, path
from rest_framework import routers
from store import views

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('discounts', views.DiscountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('new-product/', views.ProductCreateView.as_view(), name="create_product")
]