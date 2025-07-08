from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Contact, Instance, License
from .forms import ClientForm, LicenseReplaceForm, InstanceForm
# from django.contrib.auth.decorators import login_required  # Uncomment for access control

# @login_required
def dashboard(request):
    """Admin dashboard showing total clients, instances, active licenses, and upcoming renewals."""
    total_clients = Client.objects.count()
    total_instances = Instance.objects.count()
    active_licenses = License.objects.filter(is_active=True).count()
    upcoming_renewals = License.objects.filter(renewal_date__lte=date.today() + timedelta(days=30)).count()

    return render(request, 'licenses/dashboard.html', {
        'total_clients': total_clients,
        'total_instances': total_instances,
        'active_licenses': active_licenses,
        'upcoming_renewals': upcoming_renewals
    })

# @login_required
def clients_list_view(request):
    """View to list all clients."""
    clients = Client.objects.all()
    return render(request, 'licenses/clients.html', {'clients': clients})

# @login_required
def client_detail_view(request, client_id):
    """View to show client details, including contacts and instances."""
    client = get_object_or_404(Client, id=client_id)
    contacts = client.contacts.all()
    instances = client.instances.all()
    return render(request, 'licenses/client_detail.html', {
        'client': client,
        'contacts': contacts,
        'instances': instances
    })

# @login_required
def client_add_view(request):
    """View to add a new client."""
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clients_list')
    return render(request, 'licenses/client_form.html', {'form': form, 'title': 'Add Client'})

# @login_required
def client_edit_view(request, client_id):
    """View to edit an existing client."""
    client = get_object_or_404(Client, id=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'licenses/client_form.html', {'form': form, 'title': 'Edit Client'})

# @login_required
def instance_add_view(request, client_id):
    """View to add an instance to a client."""
    client = get_object_or_404(Client, id=client_id)
    form = InstanceForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.client = client
        instance.save()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'licenses/instance_form.html', {'form': form, 'title': 'Add Instance', 'client': client})

# @login_required
def instance_edit_view(request, instance_id):
    """View to edit an instance."""
    instance = get_object_or_404(Instance, id=instance_id)
    form = InstanceForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('instance_detail', instance_id=instance.id)
    return render(request, 'licenses/instance_form.html', {'form': form, 'title': 'Edit Instance', 'client': instance.client})

# @login_required
def instance_detail_view(request, instance_id):
    """View to show instance details including licenses."""
    instance = get_object_or_404(Instance, id=instance_id)
    licenses = instance.licenses.all().order_by('-created_at')
    client = instance.client 
    return render(request, 'licenses/instance_detail.html', {
        'instance': instance,
        'licenses': licenses,
        'client': client
    })

# @login_required
def license_download_view(request, license_id):
    """Placeholder view to download a license file."""
    return HttpResponse(f"Download license {license_id}")

# @login_required
def license_create_or_replace_view(request, instance_id):
    """View to create or replace a license for a given instance."""
    instance = get_object_or_404(Instance, id=instance_id)
    existing_license = instance.licenses.order_by('-created_at').first()

    if request.method == 'POST':
        form = LicenseReplaceForm(request.POST)
        if form.is_valid():
            new_license = form.save(commit=False)
            new_license.instance = instance
            new_license.created_by = request.user
            new_license.is_active = True
            new_license.save()
            form.save_m2m()

            # Deactivate previous licenses
            License.objects.filter(instance=instance).exclude(id=new_license.id).update(is_active=False)
            return redirect('client_detail', client_id=instance.client.id)
    else:
        form = LicenseReplaceForm(instance=existing_license if existing_license else None)

    return render(request, 'licenses/license_form.html', {
        'form': form,
        'title': "Add/Replace License"
    })

# @login_required
def license_history_view(request, license_id):
    """View to show license history for an instance."""
    current = get_object_or_404(License, id=license_id)
    history = License.objects.filter(instance=current.instance).order_by('-created_at')
    return render(request, 'licenses/license_history.html', {
        'license': current,
        'history': history
    })
from django.shortcuts import render, get_object_or_404, redirect
from .models import StatusTag, DeploymentMethod, Feature
from .forms import StatusTagForm, DeploymentMethodForm, FeatureForm

# STATUS TAG VIEWS

def status_tag_list(request):
    tags = StatusTag.objects.all()
    return render(request, 'licenses/status_tag_list.html', {'tags': tags})

def status_tag_create(request):
    if request.method == 'POST':
        form = StatusTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('status_tag_list')
    else:
        form = StatusTagForm()
    return render(request, 'licenses/status_tag_form.html', {'form': form})

def status_tag_edit(request, pk):
    tag = get_object_or_404(StatusTag, pk=pk)
    form = StatusTagForm(request.POST or None, instance=tag)
    if form.is_valid():
        form.save()
        return redirect('status_tag_list')
    return render(request, 'licenses/status_tag_form.html', {'form': form})

def status_tag_delete(request, pk):
    tag = get_object_or_404(StatusTag, pk=pk)
    tag.delete()
    return redirect('status_tag_list')

# DEPLOYMENT METHOD VIEWS

def deployment_method_list(request):
    methods = DeploymentMethod.objects.all()
    return render(request, 'licenses/deployment_method_list.html', {'methods': methods})

def deployment_method_create(request):
    if request.method == 'POST':
        form = DeploymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deployment_method_list')
    else:
        form = DeploymentMethodForm()
    return render(request, 'licenses/deployment_method_form.html', {'form': form})

def deployment_method_edit(request, pk):
    method = get_object_or_404(DeploymentMethod, pk=pk)
    form = DeploymentMethodForm(request.POST or None, instance=method)
    if form.is_valid():
        form.save()
        return redirect('deployment_method_list')
    return render(request, 'licenses/deployment_method_form.html', {'form': form})

def deployment_method_delete(request, pk):
    method = get_object_or_404(DeploymentMethod, pk=pk)
    method.delete()
    return redirect('deployment_method_list')

# FEATURE VIEWS

def feature_list(request):
    features = Feature.objects.all()
    return render(request, 'licenses/feature_list.html', {'features': features})

def feature_create(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feature_list')
    else:
        form = FeatureForm()
    return render(request, 'licenses/feature_form.html', {'form': form})

def feature_edit(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    form = FeatureForm(request.POST or None, instance=feature)
    if form.is_valid():
        form.save()
        return redirect('feature_list')
    return render(request, 'licenses/feature_form.html', {'form': form})

def feature_delete(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    feature.delete()
    return redirect('feature_list')

def settings_home(request):
    return render(request, 'licenses/settings_home.html')
