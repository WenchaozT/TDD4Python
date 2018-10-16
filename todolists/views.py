from django.shortcuts import redirect, render

from todolists.models import Item, List


def home_page(request):
    return render(request, "todolists/home.html")


def view_list(request):
    items = Item.objects.all()
    return render(request, "todolists/todolists.html", {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/todolists/worldshare/')
