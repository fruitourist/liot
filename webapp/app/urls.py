from django.urls import path

from . import views

urlpatterns = [
	path('liot/make_order', views.make_order, name='make_order'),
	path('liot/make_order/create_invoice_link', views.create_invoice_link, name='create_invoice_link')
]