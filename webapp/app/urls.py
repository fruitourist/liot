from django.urls import path

from . import views

urlpatterns = [
    path('make_order', views.make_order, name='make_order'),

    path('get_free_dates', views.get_free_dates, name='get_free_dates'),
    path('get_active_appointments', views.get_active_appointments, name='get_active_appointments'),
    path('create_invoice_link', views.create_invoice_link, name='create_invoice_link'),
    path('make_appointment', views.make_appointment, name='make_appointment'),
]
