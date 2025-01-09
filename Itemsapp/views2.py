
# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .models import Item, Request, SelectedItem
from .forms import RequestForm
from xhtml2pdf import pisa

# View to create a new request
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save()
            return redirect('item_list_for_request', request_id=new_request.id)
    else:
        form = RequestForm()
    return render(request, 'Itemsapp/create-request.html', {'form': form})

# View to list all items for a specific request
def item_list_for_request(request, request_id):
    items = Item.objects.all()
    current_request = get_object_or_404(Request, id=request_id)
    selected_items = SelectedItem.objects.filter(request=current_request).values_list('item_id', flat=True)
    return render(request, 'Itemsapp/items_list.html', {
        'items': items,
        'selected_items': selected_items,
        'current_request': current_request
    })

# View to add an item to the selected list for a specific request
def add_to_selected_for_request(request, request_id, pk):
    current_request = get_object_or_404(Request, id=request_id)
    item = get_object_or_404(Item, pk=pk)
    if not SelectedItem.objects.filter(request=current_request, item=item).exists():
        SelectedItem.objects.create(request=current_request, item=item)
    return redirect('item_list_for_request', request_id=request_id)


# View to remove an item from the selected list for a specific request
def remove_from_selected_for_request(request, request_id, pk):
    current_request = get_object_or_404(Request, id=request_id)
    item = get_object_or_404(Item, pk=pk)
    SelectedItem.objects.filter(request=current_request, item=item).delete()
    return redirect('item_list_for_request', request_id=request_id)


# View to list selected items for a specific request
def selected_items_list_for_request(request, request_id):
    current_request = get_object_or_404(Request, id=request_id)
    selected_items = SelectedItem.objects.filter(request=current_request)
    return render(request, 'Itemsapp/selected_items_list.html', {
        'selected_items': selected_items,
        'current_request': current_request
    })


# def render_to_pdf(template_src, context_dict):
#     # Render the template with the given context
#     template = render_to_string(template_src, context_dict)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="output.pdf"'
#
#     # Create PDF from the rendered HTML template
#     pisa_status = pisa.CreatePDF(template, dest=response)
#
#     # Check for errors
#     if pisa_status.err:
#         return HttpResponse('We had some errors while generating the PDF.')
#
#     return response
#
# def pdf_view(request, request_id):
#     # Retrieve the current request and selected items
#     current_request = get_object_or_404(Request, id=request_id)
#     selected_items = SelectedItem.objects.filter(request=current_request)
#
#     # Define the context for the PDF
#     context = {
#         'request_name': current_request.name,
#         'request_date': current_request.created_at,
#         'selected_items': selected_items
#     }
#
#     # Call the render_to_pdf function with the template and context
#     return render_to_pdf('Itemsapp/pdf_template.html', context)



import re
from urllib.parse import quote


def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def render_to_pdf(template_src, context_dict, request_name, request_date):
    template = render_to_string(template_src, context_dict)

    response = HttpResponse(content_type='application/pdf')

    formatted_date = request_date.strftime('%Y-%m-%d')

    filename = f"{sanitize_filename(request_name)}_{formatted_date}.pdf"

    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'

    pisa_status = pisa.CreatePDF(template, dest=response, encoding='UTF-8')

    if pisa_status.err:
        return HttpResponse('We had some errors while generating the PDF.')

    return response

from django.shortcuts import get_object_or_404

def pdf_view(request, request_id):
    current_request = get_object_or_404(Request, id=request_id)
    selected_items = SelectedItem.objects.filter(request=current_request)

    context = {
        'request_name': current_request.name,
        'request_date': current_request.created_at,
        'selected_items': selected_items
    }

    return render_to_pdf('Itemsapp/pdf_template.html', context, current_request.name, current_request.created_at)


def request_list_view(request):
    requests = Request.objects.all().order_by('-created_at')

    return render(request, 'Itemsapp/request_list.html', {'requests': requests})



