from django.urls import path

from . import views

urlpatterns = [
	path('make_order', views.make_order, name='make_order'),
	path('make_order/create_invoice_link', views.create_invoice_link, name='create_invoice_link')
]
