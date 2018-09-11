from django.shortcuts import redirect, render

from todolists.models import Item


def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    return render(request, "todolists/home.html")
