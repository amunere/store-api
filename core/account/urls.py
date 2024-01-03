from django.urls import include, path
from rest_framework import routers
from account import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.RegisterView.as_view(), name='signup'),
]