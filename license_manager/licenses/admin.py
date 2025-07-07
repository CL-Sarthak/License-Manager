from django.contrib import admin
from .models import Client, Contact, Instance, License, Feature, StatusTag, DeploymentMethod

admin.site.register(Client)
admin.site.register(Contact)
admin.site.register(Instance)
admin.site.register(License)
admin.site.register(Feature)
admin.site.register(StatusTag)
admin.site.register(DeploymentMethod)