from django.db import models
from django.db import models
from django.contrib.auth.models import User

class StatusTag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class DeploymentMethod(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    status_tag = models.ForeignKey(StatusTag, on_delete=models.SET_NULL, null=True, blank=True)
    primary_contact = models.ForeignKey(
        'Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_for_clients'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email})"

class Instance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='instances')
    name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)
    deployment_method = models.ForeignKey(DeploymentMethod, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.client.name} - {self.name or 'Instance'}"

class License(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, related_name='licenses')
    user_count = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    renewal_date = models.DateField(blank=True, null=True)
    environment_type = models.CharField(max_length=50)  # e.g., Dev, QA, Prod
    deployment_method = models.ForeignKey(DeploymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    encrypted_file = models.FileField(upload_to='licenses/')
    is_active = models.BooleanField(default=False)
    version_id = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            License.objects.filter(instance=self.instance, is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"License {self.version_id} for {self.instance}"
