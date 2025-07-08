from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Clients
    path('clients/', views.clients_list_view, name='clients_list'),
    path('clients/add/', views.client_add_view, name='client_add'),
    path('clients/<int:client_id>/', views.client_detail_view, name='client_detail'),
    path('clients/<int:client_id>/edit/', views.client_edit_view, name='client_edit'),

    # Instances
    path('clients/<int:client_id>/instances/add/', views.instance_add_view, name='instance_add'),
    path('instances/<int:instance_id>/', views.instance_detail_view, name='instance_detail'),
    path('instances/<int:instance_id>/edit/', views.instance_edit_view, name='instance_edit'),

    # Licenses
    path('licenses/<int:license_id>/download/', views.license_download_view, name='license_download'),
    path('instances/<int:instance_id>/license/manage/', views.license_create_or_replace_view, name='license_manage'),
    path('licenses/<int:license_id>/history/', views.license_history_view, name='license_history'),

    #settings

    path('settings/', views.settings_home, name='settings_home'),

    # StatusTag
    path('settings/status-tags/', views.status_tag_list, name='status_tag_list'),
    path('settings/status-tags/add/', views.status_tag_create, name='status_tag_create'),
    path('settings/status-tags/<int:pk>/edit/', views.status_tag_edit, name='status_tag_edit'),
    path('settings/status-tags/<int:pk>/delete/', views.status_tag_delete, name='status_tag_delete'),

    # DeploymentMethod
    path('settings/deployment-methods/', views.deployment_method_list, name='deployment_method_list'),
    path('settings/deployment-methods/add/', views.deployment_method_create, name='deployment_method_create'),
    path('settings/deployment-methods/<int:pk>/edit/', views.deployment_method_edit, name='deployment_method_edit'),
    path('settings/deployment-methods/<int:pk>/delete/', views.deployment_method_delete, name='deployment_method_delete'),

    # Feature
    path('settings/features/', views.feature_list, name='feature_list'),
    path('settings/features/add/', views.feature_create, name='feature_create'),
    path('settings/features/<int:pk>/edit/', views.feature_edit, name='feature_edit'),
    path('settings/features/<int:pk>/delete/', views.feature_delete, name='feature_delete'),

]
