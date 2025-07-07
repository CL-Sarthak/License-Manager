from django.shortcuts import render, get_object_or_404
from .models import Client, Instance, License
from datetime import date, timedelta
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Contact, Instance
from .forms import ClientForm, LicenseReplaceForm




def dashboard(request):
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


def clients_list(request):
    clients = Client.objects.all()
    return render(request, 'licenses/clients.html', {'clients': clients})


def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    instances = client.instances.all()
    contacts = client.contacts.all()
    return render(request, 'licenses/client_detail.html', {
        'client': client,
        'instances': instances,
        'contacts': contacts
    })


def instance_detail(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    licenses = instance.licenses.all().order_by('-created_at')
    return render(request, 'licenses/instance_detail.html', {
        'instance': instance,
        'licenses': licenses
    })

def clients_list_view(request):
    clients = Client.objects.all()
    return render(request, 'licenses/clients.html', {'clients': clients})

def client_detail_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    contacts = client.contacts.all()
    instances = client.instances.all()
    return render(request, 'licenses/client_detail.html', {
        'client': client,
        'contacts': contacts,
        'instances': instances
    })



def client_add_view(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clients_list')
    return render(request, 'licenses/client_form.html', {'form': form, 'title': 'Add Client'})

def client_edit_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'licenses/client_form.html', {'form': form, 'title': 'Edit Client'})


from .models import Instance, License
from .forms import InstanceForm

def instance_add_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    form = InstanceForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.client = client
        instance.save()
        return redirect('client_detail', client_id=client.id)
    return render(request, 'licenses/instance_form.html', {'form': form, 'title': 'Add Instance', 'client': client})


def instance_edit_view(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    form = InstanceForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('instance_detail', instance_id=instance.id)
    return render(request, 'licenses/instance_form.html', {'form': form, 'title': 'Edit Instance', 'client': instance.client})


def instance_detail_view(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    licenses = instance.licenses.all().order_by('-created_at')
    return render(request, 'licenses/instance_detail.html', {
        'instance': instance,
        'licenses': licenses
    })
from django.http import HttpResponse

def license_download_view(request, license_id):
    return HttpResponse(f"Download license {license_id}")

def license_replace_view(request, license_id):
    return HttpResponse(f"Replace license {license_id}")

def license_history_view(request, license_id):
    return HttpResponse(f"History of license {license_id}")
def license_create_or_replace_view(request, instance_id):
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

            # Deactivate others
            License.objects.filter(instance=instance).exclude(id=new_license.id).update(is_active=False)
            return redirect('client_detail', client_id=instance.client.id)
    else:
        form = LicenseReplaceForm(instance=existing_license if existing_license else None)

    return render(request, 'licenses/license_form.html', {
        'form': form,
        'title': "Add/Replace License"
    })



def license_history_view(request, license_id):
    current = get_object_or_404(License, id=license_id)
    history = License.objects.filter(instance=current.instance).order_by('-created_at')
    return render(request, 'licenses/license_history.html', {
        'license': current,
        'history': history
    })
