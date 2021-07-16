from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductDetailView

urlpatterns = [
	path('products/<str:ct_model>/<str:slug>/',ProductDetailView.as_view(), name="product_detail")
]