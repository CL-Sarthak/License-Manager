from django import forms
from .models import Client, Contact

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'status_tag', 'is_active', 'primary_contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status_tag': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(),
            'primary_contact': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if instance:
            # Editing: show only contacts related to this client
            self.fields['primary_contact'].queryset = Contact.objects.filter(client=instance)
        else:
            # Creating: no contacts exist yet → empty + disabled
            self.fields['primary_contact'].queryset = Contact.objects.none()
            self.fields['primary_contact'].widget.attrs['disabled'] = True

from .models import Instance
from django import forms

class InstanceForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = ['name', 'start_date', 'end_date', 'renewal_date', 'deployment_method', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'renewal_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'deployment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
from .models import License
from django import forms

class LicenseReplaceForm(forms.ModelForm):
    class Meta:
        model = License
        fields = [
            'user_count', 'start_date', 'end_date', 'renewal_date',
            'environment_type', 'deployment_method', 'features', 'version_id'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'renewal_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'user_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'environment_type': forms.TextInput(attrs={'class': 'form-control'}),
            'deployment_method': forms.Select(attrs={'class': 'form-control'}),
            'features': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'version_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import StatusTag, DeploymentMethod, Feature

class StatusTagForm(forms.ModelForm):
    class Meta:
        model = StatusTag
        fields = ['name']

class DeploymentMethodForm(forms.ModelForm):
    class Meta:
        model = DeploymentMethod
        fields = ['name', 'is_active']

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name', 'description']
