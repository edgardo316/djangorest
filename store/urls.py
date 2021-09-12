from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from store import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('deals', views.DealsViewSet)
#router.register('store', views.StoreViewSet)


app_name = 'store'

urlpatterns = [
    path('', include(router.urls))
]
