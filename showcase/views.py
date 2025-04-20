from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Item
from .forms import ItemForm
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    items = Item.objects.exclude(name="").exclude(image="")  # Filter out blank entries
    return render(request, 'showcase/index.html', {'items': items})

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect('index')
    else:
        form = ItemForm()
    return render(request, 'showcase/add_item.html', {'form': form})


@login_required
def update_item(request, id):
    # Fetch the item by ID
    item = get_object_or_404(Item, id=id)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after update
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'showcase/update_item.html', {'form': form, 'item': item})


@login_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if item.owner != request.user:
        return HttpResponseForbidden("You can't delete this item.")
    item.delete()
    return redirect('index')
