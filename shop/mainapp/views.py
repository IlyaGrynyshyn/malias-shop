from re import template
from django.shortcuts import render
from django.views.generic import DetailView
from .models import SmartHouse,SmartPhone,SmartWatch,Accessory


class ProductDetailView(DetailView):

	CT_MODEL_MODEL_CLASS = {
		'smarthouse' : SmartHouse,
		'smartphone' : SmartPhone,
		'smartwatch' : SmartWatch,
		'accessory' : Accessory
	}

	def dispatch(self, request, *args, **kwarks):
		self.model = self.CT_MODEL_MODEL_CLASS[kwarks['ct_model']]
		self.queryset = self.model._base_manager.all()
		return super().dispatch(request, *args, **kwarks)

	#model = Model
	#queryset = Model.objects.all()
	context_object_name = 'product'
	template_name = 'product-detail.html'
	slug_url_kwarg = 'slug'
