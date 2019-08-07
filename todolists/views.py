from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, Http404

from todolists.models import Item, List


def home_page(request):
    return render(request, "todolists/home.html")


def view_list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
        return render(request, "todolists/todolists.html", {'list': list_})
    except List.DoesNotExist:
        return JsonResponse(
            {'result': 404, 'msg': f'List {list_id} does not exist'})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/todolists/%d/' % (list_.id,))


def add_item(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/todolists/%d/' % (list_.id,))
    except List.DoesNotExist:
        return JsonResponse(
            {'result': 404, 'msg': f'List {list_id} does not exist'})


def json_list(request, list_id):
    list_ = get_object_or_404(List, id=list_id)
    items = Item.objects.filter(list=list_)
    return JsonResponse(
        {'result': 200, 'msg': [f"id:{item.id}, todoItem:{item.text}" for item in items]})


def delete_item(request, list_id, item_id):
    try:
        list_ = List.objects.get(id=list_id)
        Item.objects.filter(list=list_, id=item_id).delete()
        return redirect('/todolists/%d/' % (list_.id,))
    except List.DoesNotExist:
        return JsonResponse(
            {'result': 404, 'msg': f'List {list_id} does not exist'})


def delete_list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
        Item.objects.filter(list=list_).delete()
        List.objects.filter(id=list_id).delete()
    except List.DoesNotExist:
        raise Http404("List does not exist")
    finally:
        return redirect('/')
