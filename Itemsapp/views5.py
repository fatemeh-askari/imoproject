# # views.py
# from django.http import HttpResponse
# from django.shortcuts import render, redirect, get_object_or_404
# from django.template.loader import render_to_string
#
# from .models import Item, Request, SelectedItem
# from .forms import RequestForm
# from xhtml2pdf import pisa
#
# # View to create a new request
# def create_request(request):
#     if request.method == 'POST':
#         form = RequestForm(request.POST)
#         if form.is_valid():
#             new_request = form.save()
#             return redirect('item_list_for_request', request_id=new_request.id)
#     else:
#         form = RequestForm()
#     return render(request, 'Itemsapp/create-request.html', {'form': form})
#
# # View to list all items for a specific request
# def item_list_for_request(request, request_id):
#     items = Item.objects.all()
#     current_request = get_object_or_404(Request, id=request_id)
#     selected_items = SelectedItem.objects.filter(request=current_request).values_list('item_id', flat=True)
#     return render(request, 'Itemsapp/items_list.html', {
#         'items': items,
#         'selected_items': selected_items,
#         'current_request': current_request
#     })
#
# # View to add an item to the selected list for a specific request
# def add_to_selected_for_request(request, request_id, pk):
#     current_request = get_object_or_404(Request, id=request_id)
#     item = get_object_or_404(Item, pk=pk)
#     if not SelectedItem.objects.filter(request=current_request, item=item).exists():
#         SelectedItem.objects.create(request=current_request, item=item)
#     return redirect('item_list_for_request', request_id=request_id)
#
#
# # View to remove an item from the selected list for a specific request
# def remove_from_selected_for_request(request, request_id, pk):
#     current_request = get_object_or_404(Request, id=request_id)
#     item = get_object_or_404(Item, pk=pk)
#     SelectedItem.objects.filter(request=current_request, item=item).delete()
#     return redirect('item_list_for_request', request_id=request_id)
#
#
# # View to list selected items for a specific request
# def selected_items_list_for_request(request, request_id):
#     current_request = get_object_or_404(Request, id=request_id)
#     selected_items = SelectedItem.objects.filter(request=current_request)
#     return render(request, 'Itemsapp/selected_items_list.html', {
#         'selected_items': selected_items,
#         'current_request': current_request
#     })
#
#
# # def render_to_pdf(template_src, context_dict):
# #     # Render the template with the given context
# #     template = render_to_string(template_src, context_dict)
# #     response = HttpResponse(content_type='application/pdf')
# #     response['Content-Disposition'] = 'attachment; filename="output.pdf"'
# #
# #     # Create PDF from the rendered HTML template
# #     pisa_status = pisa.CreatePDF(template, dest=response)
# #
# #     # Check for errors
# #     if pisa_status.err:
# #         return HttpResponse('We had some errors while generating the PDF.')
# #
# #     return response
# #
# # def pdf_view(request, request_id):
# #     # Retrieve the current request and selected items
# #     current_request = get_object_or_404(Request, id=request_id)
# #     selected_items = SelectedItem.objects.filter(request=current_request)
# #
# #     # Define the context for the PDF
# #     context = {
# #         'request_name': current_request.name,
# #         'request_date': current_request.created_at,
# #         'selected_items': selected_items
# #     }
# #
# #     # Call the render_to_pdf function with the template and context
# #     return render_to_pdf('Itemsapp/pdf_template.html', context)
#
#
#
# import re
# from urllib.parse import quote
#
#
# def sanitize_filename(name):
#     return re.sub(r'[<>:"/\\|?*]', '_', name)
#
#
# def render_to_pdf(template_src, context_dict, request_name, request_date):
#     template = render_to_string(template_src, context_dict)
#
#     response = HttpResponse(content_type='application/pdf')
#
#     formatted_date = request_date.strftime('%Y-%m-%d')
#
#     filename = f"{sanitize_filename(request_name)}_{formatted_date}.pdf"
#
#     response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
#
#     pisa_status = pisa.CreatePDF(template, dest=response, encoding='UTF-8')
#
#     if pisa_status.err:
#         return HttpResponse('We had some errors while generating the PDF.')
#
#     return response
#
# from django.shortcuts import get_object_or_404
#
# def pdf_view(request, request_id):
#     current_request = get_object_or_404(Request, id=request_id)
#     selected_items = SelectedItem.objects.filter(request=current_request)
#
#     context = {
#         'request_name': current_request.name,
#         'request_date': current_request.created_at,
#         'selected_items': selected_items
#     }
#
#     return render_to_pdf('Itemsapp/pdf_template.html', context, current_request.name, current_request.created_at)
#
#
# def request_list_view(request):
#     requests = Request.objects.all().order_by('-created_at')
#
#     return render(request, 'Itemsapp/request_list.html', {'requests': requests})
#
#
#

# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from .models import Item, Request, SelectedItem
from .forms import RequestForm
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required



@login_required
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


# View to list selected items for a specific request************
# def selected_items_list_for_request(request, request_id):
#     current_request = get_object_or_404(Request, id=request_id)
#     selected_items = SelectedItem.objects.filter(request=current_request)
#     return render(request, 'Itemsapp/selected_items_list.html', {
#         'selected_items': selected_items,
#         'current_request': current_request
#     })




# import re
# from urllib.parse import quote
#
#
# def sanitize_filename(name):
#     return re.sub(r'[<>:"/\\|?*]', '_', name)
#
#
# def render_to_pdf(template_src, context_dict, request_name, request_date):
#     template = render_to_string(template_src, context_dict)
#
#     response = HttpResponse(content_type='application/pdf')
#
#     formatted_date = request_date.strftime('%Y-%m-%d')
#
#     filename = f"{sanitize_filename(request_name)}_{formatted_date}.pdf"
#
#     response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
#
#     pisa_status = pisa.CreatePDF(template, dest=response, encoding='UTF-8')
#
#     if pisa_status.err:
#         return HttpResponse('We had some errors while generating the PDF.')
#
#     return response
#
# from django.shortcuts import get_object_or_404
#
# def pdf_view(request, request_id):
#     current_request = get_object_or_404(Request, id=request_id)
#     selected_items = SelectedItem.objects.filter(request=current_request)
#
#     context = {
#         'request_name': current_request.name,
#         'request_date': current_request.created_at,
#         'selected_items': selected_items
#     }
#
#     return render_to_pdf('Itemsapp/pdf_template.html', context, current_request.name, current_request.created_at)



import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from urllib.parse import quote  # Import for URL encoding

def sanitize_filename(name):
    """Sanitize the filename by removing or replacing any disallowed characters."""
    import re
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def render_to_pdf(template_src, context_dict, request_name=None, request_date=None):
    # Render the HTML template with the context
    template = render_to_string(template_src, context_dict)

    # Path to wkhtmltopdf binary (update the path according to your system)
    path_to_wkhtmltopdf = r'C:\wkhtmltox\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    # Generate PDF from the rendered template
    pdf = pdfkit.from_string(template, False, configuration=config)

    # Sanitize request_name for safe filename usage
    sanitized_request_name = sanitize_filename(request_name)

    # Format the request_date as a string (YYYY-MM-DD)
    formatted_date = request_date.strftime('%Y-%m-%d')

    # Construct the filename with request_name and request_date
    filename = f"{sanitized_request_name}_{formatted_date}.pdf"

    # URL-encode the filename to handle special characters
    encoded_filename = quote(filename)

    # Set the Content-Disposition header for file download with the encoded filename
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"; filename*=UTF-8\'\'{encoded_filename}'

    return response




from django.shortcuts import get_object_or_404

def pdf_view(request, request_id):
    current_request = get_object_or_404(Request, id=request_id)
    selected_items = SelectedItem.objects.filter(request=current_request)
    request_details_spacial = RequestDetail.objects.filter(request=current_request)

    context = {
        'request_name': current_request.name,
        'request_date': current_request.created_at,
        'request_details': current_request.details,
        'selected_items': selected_items,
        'request_details_spacial': request_details_spacial
    }

    # Pass the necessary arguments to render_to_pdf
    return render_to_pdf('Itemsapp/pdf_template.html', context, current_request.name, current_request.created_at)




def request_list_view(request):
    requests = Request.objects.all().order_by('-created_at')

    return render(request, 'Itemsapp/request_list.html', {'requests': requests})




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('create-request/')  # Redirect to the home page after login
            else:
                return render(request, 'Itemsapp/login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'Itemsapp/login.html', {'form': form})











from django.shortcuts import render, redirect, get_object_or_404
from .models import Request, RequestDetail, SelectedItem
from .forms import RequestDetailForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Request, RequestDetail, SelectedItem
from .forms import RequestDetailForm


def selected_items_list_for_request(request, request_id):
    # دریافت درخواست خاص با ID مشخص
    current_request = get_object_or_404(Request, id=request_id)

    # دریافت آیتم‌های انتخابی برای این درخواست
    selected_items = SelectedItem.objects.filter(request=current_request)

    # نمایش جزئیات قبلی برای درخواست
    existing_details = RequestDetail.objects.filter(request=current_request)

    # اگر درخواست POST باشد، یعنی فرم ارسال شده است
    if request.method == 'POST':
        form = RequestDetailForm(request.POST)
        if form.is_valid():
            # ذخیره جزئیات جدید
            new_detail = form.save(commit=False)
            new_detail.request = current_request
            new_detail.save()
            # بعد از ذخیره، به صفحه فعلی برگشت
            return redirect('selected_items_list_for_request', request_id=request_id)
    else:
        # اگر درخواست GET باشد، فرم خالی را نمایش بده
        form = RequestDetailForm()

    # ارسال داده‌ها به قالب
    return render(request, 'itemsapp/selected_items_list.html', {
        'selected_items': selected_items,
        'current_request': current_request,
        'existing_details': existing_details,  # جزئیات قبلی
        'form': form,  # فرم برای افزودن جزئیات جدید
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Request, RequestDetail
from django.http import HttpResponse


def delete_request_detail(request, request_id, detail_id):
    # پیدا کردن جزئیه با استفاده از ID
    detail = get_object_or_404(RequestDetail, id=detail_id, request_id=request_id)

    # حذف جزئیه
    detail.delete()

    # بعد از حذف، کاربر را به صفحه جزئیات درخواست هدایت می‌کنیم
    return redirect('selected_items_list_for_request', request_id=request_id)



