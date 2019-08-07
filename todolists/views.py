from django.shortcuts import redirect, render
from django.http import JsonResponse

from todolists.models import Item, List


def home_page(request):
    return render(request, "todolists/home.html")


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)
    return render(request, "todolists/todolists.html", {'list': list_})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/todolists/%d/' % (list_.id,))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/todolists/%d/' % (list_.id,))


def json_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return JsonResponse(
        {'result': 200, 'msg': [f"id:{item.id}, todoItem:{item.text}" for item in items]})


def delete_item(request, list_id, item_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.filter(list=list_, id=item_id).delete()
    return redirect('/todolists/%d/' % (list_.id,))


def delete_list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
        Item.objects.filter(list=list_).delete()
        List.objects.filter(id=list_id).delete()
    finally:
        return redirect('/')
