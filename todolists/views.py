from django.shortcuts import redirect, render

from todolists.models import Item


def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/todolists/worldshare/')

    return render(request, "todolists/home.html")


def view_list(request):
    items = Item.objects.all()
    return render(request, "todolists/todolists.html", {'items': items})
