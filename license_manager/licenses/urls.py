# licenses/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('instances/<int:instance_id>/', views.instance_detail, name='instance_detail'),
    path('clients/', views.clients_list_view, name='clients_list'),
    path('clients/add/', views.client_add_view, name='client_add'),
    path('clients/<int:client_id>/', views.client_detail_view, name='client_detail'),
    path('clients/<int:client_id>/edit/', views.client_edit_view, name='client_edit'),
    path('clients/<int:client_id>/instances/add/', views.instance_add_view, name='instance_add'),
    path('instances/<int:instance_id>/', views.instance_detail_view, name='instance_detail'),
    path('instances/<int:instance_id>/edit/', views.instance_edit_view, name='instance_edit'),
    path('licenses/<int:license_id>/download/', views.license_download_view, name='license_download'),
    path('instances/<int:instance_id>/license/manage/', views.license_create_or_replace_view, name='license_manage'),
    path('licenses/<int:license_id>/history/', views.license_history_view, name='license_history'),
    


]
