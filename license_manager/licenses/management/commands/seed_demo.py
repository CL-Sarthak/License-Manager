from django.core.management.base import BaseCommand
from licenses.models import (
    Client, Contact, Instance, License, Feature,
    StatusTag, DeploymentMethod
)
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seed demo data for License Manager'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding demo data...")

        # Clear old demo data
        License.objects.all().delete()
        Instance.objects.all().delete()
        Contact.objects.all().delete()
        Client.objects.all().delete()
        Feature.objects.all().delete()
        StatusTag.objects.all().delete()
        DeploymentMethod.objects.all().delete()

        # Create status tags
        tags = ['In Progress', 'QA', 'Suspended']
        for tag in tags:
            StatusTag.objects.create(name=tag)

        # Create deployment methods
        methods = ['On-Prem', 'AWS', 'Azure', 'GCP']
        for m in methods:
            DeploymentMethod.objects.create(name=m)

        # Create features
        feature_list = ['LT Genius', 'Audit Engine', 'Compliance Tracker']
        features = [Feature.objects.create(name=f) for f in feature_list]

        # Create a superuser (if not exists)
        admin_user, created = User.objects.get_or_create(username='admin')
        if created:
            admin_user.set_password('admin')
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()

        # Create demo clients
        for i in range(3):
            client = Client.objects.create(
                name=f"Client {i+1}",
                status_tag=StatusTag.objects.order_by('?').first(),
                is_active=True,
                primary_contact=None
            )
            contact = Contact.objects.create(
                client=client,
                name=f"Contact {i+1}",
                email=f"contact{i+1}@example.com"
            )
            client.primary_contact = contact
            client.save()

            # Add instance
            instance = Instance.objects.create(
                client=client,
                name=f"{client.name} - PROD",
                deployment_method=DeploymentMethod.objects.order_by('?').first(),
                start_date=date.today(),
                end_date=date.today() + timedelta(days=365),
                renewal_date=date.today() + timedelta(days=340),
                notes="Production instance"
            )

            # Add license
            lic = License.objects.create(
                instance=instance,
                user_count=random.randint(5, 100),
                start_date=date.today(),
                end_date=date.today() + timedelta(days=365),
                renewal_date=date.today() + timedelta(days=340),
                environment_type='PROD',
                deployment_method=instance.deployment_method,
                version_id=f"v1.{i+1}",
                is_active=True,
                created_by=admin_user
            )
            lic.features.set(features)

        self.stdout.write(self.style.SUCCESS("Demo data created successfully!"))
