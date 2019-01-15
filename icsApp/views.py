from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from collections import OrderedDict

# Create your views here.

# Import from Excel
class Customer:
    def __init__(self, item_name,
                 quantity, location,
                 item_position, category,
                 vendor, link, unit_price, updated_date):
        self.itemName = item_name
        self.quantity = quantity
        self.location = location
        self.itemPosition = item_position
        self.category = category
        self.vendor = vendor
        self.link = link
        self.unitPrice = unit_price
        # self.updatedDate = updated_date

import csv
import sys

def import_data(request):
    return render(request, 'upload_data.html')

def upload_data(request):
    if request.method == 'POST':
        csv_file = request.FILES["csv_file"]
        print(csv_file)
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        for row in reader:
            data_dict = dict(OrderedDict(row))
            item_count = Inventory.objects.filter(item_name=data_dict['item_name']).count()
            print(item_count)
            print(data_dict)
            if item_count == 1:
                form = InventoryForm(data_dict)
                # print(form)
                if form.is_valid():
                    inventory = form.save()
                    inventory.save()
            elif item_count == 0:
                form1 = InventoryForm(data_dict)
                # print(form1)
                if form1.is_valid():
                    form1.save()
    return HttpResponseRedirect("/inventory/")



# List inventory items
def inventory_list(request):
    inventory = Inventory.objects.order_by('-updated_date')
    return render(request, 'inventory_list.html', {'inventorys': inventory})

#sort by item
def ascending_item(request):
    inventory = Inventory.objects.order_by('item_name')
    return render(request, 'inventory_list.html', {'inventorys': inventory})

def descending_item(request):
    inventory = Inventory.objects.order_by('-item_name')
    return render(request, 'inventory_list.html', {'inventorys': inventory})

#sort by category
def ascending_category(request):
    inventory = Inventory.objects.order_by('category')
    return render(request, 'inventory_list.html', {'inventorys': inventory})

def descending_category(request):
    inventory = Inventory.objects.order_by('-category')
    return render(request, 'inventory_list.html', {'inventorys': inventory})

#sort by vendor
def ascending_vendor(request):
    inventory = Inventory.objects.order_by('vendor')
    return render(request, 'inventory_list.html', {'inventorys': inventory})

def descending_vendor(request):
    inventory = Inventory.objects.order_by('-vendor')
    return render(request, 'inventory_list.html', {'inventorys': inventory})

# Add Inventory item
def inventory_new(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.updated_date = datetime.date.today()
            inventory.save() #saves the values
            return HttpResponseRedirect("/inventory/")
    else:
        form = InventoryForm()
    return render(request, 'inventory_new.html', {'form': form})

# Edit inventory item
def inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            inventory.updated_date = datetime.date.today()
            inventory = form.save()
            inventory.save()
            return HttpResponseRedirect("/inventory/")
    else:
        form = InventoryForm(instance=inventory)
    return render(request, 'inventory_edit.html', {'form': form})

# Delete Inventory item
def inventory_delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    return HttpResponseRedirect("/inventory/")

def quantity_increase(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.quantity = inventory.quantity + 1
    inventory.save()
    return HttpResponseRedirect("/inventory/")

def quantity_decrease(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.quantity = inventory.quantity - 1
    inventory.save()
    return HttpResponseRedirect("/inventory/")

def search(request):
    query = request.POST['usr_query']
    inventory = Inventory.objects.filter(item_name__contains=query)
    return render(request, 'inventory_list.html', {'inventorys': inventory})


def export_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="InventoryList.csv"'
    writer = csv.writer(response)
    writer.writerow(['item_name', 'quantity', 'location', 'Item Position', 'category', 'vendor', 'link', 'Unit Price', 'Updated Date'])
    records = Inventory.objects.all()

    for record in records:
        arr = []
        arr.append(record.item_name)
        arr.append(record.quantity)
        arr.append(record.location)
        arr.append(record.item_position)
        arr.append(record.category)
        arr.append(record.vendor)
        arr.append(record.link)
        arr.append(record.unit_price)
        arr.append(record.updated_date)
        writer.writerow(arr)
    return response
