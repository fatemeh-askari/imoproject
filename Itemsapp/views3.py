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



# View to create a new request

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
    # پاکسازی نام فایل از کاراکترهای غیرمجاز
    return re.sub(r'[<>:"/\\|?*]', '_', name)


# def render_to_pdf(response, request_name, request_date, selected_items):
#     # ثبت فونت فارسی
#     pdfmetrics.registerFont(TTFont('IRANSans', 'static/assets/fonts/IRANSansWeb.ttf'))
#
#     # ایجاد یک شی canvas برای PDF
#     c = canvas.Canvas(response, pagesize=letter)
#     width, height = letter
#
#     # تنظیم فونت
#     c.setFont("IRANSans", 12)
#
#     # شکل‌دهی و مرتب‌سازی متن‌ها برای نمایش از راست به چپ
#     reshaped_title = get_display(arabic_reshaper.reshape("گزارش درخواست"))
#     reshaped_request_name = get_display(arabic_reshaper.reshape(f"نام درخواست: {request_name}"))
#     reshaped_request_date = get_display(arabic_reshaper.reshape(f"تاریخ درخواست: {request_date.strftime('%Y/%m/%d')}"))
#
#     # رسم متن‌ها در PDF با استفاده از drawRightString برای راست‌چین کردن
#     c.drawRightString(width - 1 * inch, height - 1 * inch, reshaped_title)
#     c.drawRightString(width - 1 * inch, height - 1.5 * inch, reshaped_request_name)
#     c.drawRightString(width - 1 * inch, height - 2 * inch, reshaped_request_date)
#
#     # رسم جدول برای موارد انتخاب شده
#     reshaped_header = get_display(arabic_reshaper.reshape("موارد انتخاب شده:"))
#     c.drawRightString(width - 1 * inch, height - 3 * inch, reshaped_header)
#     c.drawRightString(width - 1 * inch, height - 3.5 * inch,
#                       get_display(arabic_reshaper.reshape("عنوان مورد  |  توضیح کوتاه  |  دسته‌بندی")))
#     c.drawRightString(width - 1 * inch, height - 4 * inch,
#                       get_display(arabic_reshaper.reshape("-------------------------------------------------")))
#
#     # افزودن اطلاعات موارد انتخاب شده به جدول
#     y = height - 4.5 * inch
#     for selected_item in selected_items:
#         item = selected_item.item  # مطمئن شوید که به درستی به آیتم دسترسی دارید
#         title = get_display(arabic_reshaper.reshape(item.title))
#         short_description = get_display(arabic_reshaper.reshape(item.short_description))
#         category = get_display(arabic_reshaper.reshape(item.category))
#
#         # رسم هر سطر در جدول به صورت راست‌چین
#         row_text = f"{title}  |  {short_description}  |  {category}"
#         c.drawRightString(width - 1 * inch, y, row_text)
#         y -= 0.5 * inch
#
#     # بستن و ذخیره PDF
#     c.showPage()
#     c.save()


# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.lib import colors
#
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from bidi.algorithm import get_display
# import arabic_reshaper
# import re
#
# def is_persian(text):
#     """ Helper function to detect if the text contains Persian characters. """
#     persian_characters = re.compile("[\u0600-\u06FF]")  # Persian Unicode range
#     return bool(persian_characters.search(text))
#
# def render_to_pdf(response, request_name, request_date, selected_items):
#     # Register Persian Font
#     pdfmetrics.registerFont(TTFont('IRANSans', 'static/assets/fonts/Digi-Mitra-Circle-Bold.ttf'))
#     # Register English Font (Sans Serif)
#     pdfmetrics.registerFont(TTFont('SansSerif', 'static/assets/fonts/IRANSansWeb.ttf'))
#
#     # Create canvas for PDF
#     c = canvas.Canvas(response, pagesize=letter)
#     width, height = letter
#
#     # Draw the border around the page
#     c.setStrokeColor(colors.black)
#     c.setLineWidth(2)
#     c.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)
#
#     # Set fonts and draw text based on content language
#     def draw_text(content, x, y):
#         if is_persian(content):
#             c.setFont("IRANSans", 12)
#             reshaped_text = get_display(arabic_reshaper.reshape(content))
#             c.drawRightString(x, y, reshaped_text)
#         else:
#             c.setFont("SansSerif", 12)
#             c.drawString(x, y, content)  # Left-align for English
#
#     # Title
#     draw_text("گزارش درخواست", width - 1 * inch, height - 1 * inch)
#
#     # Request Name and Date (Persian and possibly English mixed)
#     draw_text(f"نام درخواست: {request_name}", width - 1 * inch, height - 1.5 * inch)
#     draw_text(f"تاریخ درخواست: {request_date.strftime('%Y/%m/%d')}", width - 1 * inch, height - 2 * inch)
#
#     # Header for selected items list
#     draw_text("موارد انتخاب شده:", width - 1 * inch, height - 3 * inch)
#
#     # List of selected items (assume item names might contain both English and Persian)
#     y = height - 3.5 * inch
#     for selected_item in selected_items:
#         item_name = selected_item.item.title  # Access item title
#         draw_text(item_name, width - 1 * inch, y)
#         y -= 0.5 * inch  # Move down for the next item
#
#     # Save the PDF
#     c.showPage()
#     c.save()



# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.lib import colors
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from bidi.algorithm import get_display
# import arabic_reshaper
# import re
#
# def is_persian(text):
#     """ Helper function to detect if the text contains Persian characters. """
#     persian_characters = re.compile("[\u0600-\u06FF]")  # Persian Unicode range
#     return bool(persian_characters.search(text))
#
# def render_to_pdf(response, request_name, request_date, selected_items):
#     # Register Persian Font (B-Mitra)
#     pdfmetrics.registerFont(TTFont('IRANSans', 'static/assets/fonts/Digi-Mitra-Circle-Bold.ttf'))
#     # Register English Font (Sans Serif)
#     pdfmetrics.registerFont(TTFont('SansSerif', 'static/assets/fonts/IRANSansWeb.ttf'))
#
#     # Create canvas for PDF
#     c = canvas.Canvas(response, pagesize=letter)
#     width, height = letter
#
#     # Draw the border around the page
#     c.setStrokeColor(colors.black)
#     c.setLineWidth(2)
#     c.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)
#
#     # Set fonts and draw text based on content language
#     def draw_text(content, x, y):
#         if is_persian(content):
#             c.setFont("IRANSans", 12)
#             reshaped_text = get_display(arabic_reshaper.reshape(content))
#             c.drawRightString(x, y, reshaped_text)
#         else:
#             c.setFont("SansSerif", 12)
#             c.drawString(x, y, content)  # Left-align for English text
#
#     # Title (in Persian)
#     draw_text("In The Name Of God", width - 1 * inch, height - 1 * inch)
#
#     # Request Name and Date (mixed Persian/English)
#     draw_text(f"نام درخواست: {request_name}", width - 1 * inch, height - 1.5 * inch)
#     draw_text(f"تاریخ درخواست: {request_date.strftime('%Y/%m/%d')}", width - 1 * inch, height - 2 * inch)
#
#     # Header for selected items list
#     draw_text("موارد انتخاب شده:", width - 1 * inch, height - 3 * inch)
#
#     # Numbered list of selected items
#     y = height - 3.5 * inch
#     for index, selected_item in enumerate(selected_items, start=1):
#         item_name = selected_item.item.title  # Access item title
#         numbered_item = f"{index}. {item_name}"  # Prepend the number
#         draw_text(numbered_item, width - 1 * inch, y)
#         y -= 0.5 * inch  # Move down for the next item
#
#     # Save the PDF
#     c.showPage()
#     c.save()


from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import re


def is_persian(text):
    """ Helper function to detect if the text contains Persian characters. """
    persian_characters = re.compile("[\u0600-\u06FF]")  # Persian Unicode range
    return bool(persian_characters.search(text))


# def render_to_pdf(response, request_name, request_date, request_details, selected_items):
#     # Register Persian Font
#     pdfmetrics.registerFont(TTFont('IRANSans', 'static/assets/fonts/Digi-Mitra-Rectangle-Bold.ttf'))
#
#     # Create canvas for PDF
#     c = canvas.Canvas(response, pagesize=letter)
#     width, height = letter
#
#     # Draw the border around the page
#     c.setStrokeColor(colors.black)
#     c.setLineWidth(1)
#     c.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)
#
#     # Function to draw text based on alignment (center, left, right)
#     def draw_text(content, x, y, alignment="right", font_size=None):
#         if font_size is None:
#             font_size = 14
#         c.setFont("IRANSans", font_size)  # Use the same Persian font for all text
#         reshaped_text = get_display(arabic_reshaper.reshape(content))
#
#         if alignment == "center":
#             c.drawCentredString(x, y, reshaped_text)
#         elif alignment == "left":
#             c.drawString(x, y, reshaped_text)
#         else:  # Default is right alignment
#             c.drawRightString(x, y, reshaped_text)
#
#     # Centered title ("In The Name Of God")
#     draw_text("In The Name Of God", width / 2, height - 1 * inch, alignment="center", font_size=30)
#
#     # Left-aligned Request Name and Date
#     draw_text(f"Survay Name: {request_name}", 1 * inch, height - 1.5 * inch, alignment="left")
#     draw_text(f"Date: {request_date.strftime('%Y/%m/%d')}", 1 * inch, height - 2 * inch, alignment="left")
#     # Right-aligned Request Details
#     draw_text(f"شرح: {request_details}", width - 1 * inch, height - 3.5 * inch, alignment="right")
#
#     # Left-aligned Header for selected items list
#     draw_text("موارد انتخاب شده:", width - 1 * inch, height - 4 * inch)
#
#     # List of selected items (right-aligned)
#     y = height - 4.5 * inch
#     for index, selected_item in enumerate(selected_items, start=1):
#         item_name = f"{index}. {selected_item.item.title}"  # Number the items
#         draw_text(item_name, width - 1 * inch, y, alignment="right")
#         y -= 0.5 * inch  # Move down for the next item
#
#     # Save the PDF
#     c.showPage()
#     c.save()



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from bidi.algorithm import get_display
import arabic_reshaper

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from bidi.algorithm import get_display
import arabic_reshaper

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from bidi.algorithm import get_display
import arabic_reshaper


def draw_wrapped_text(c, content, x, y, max_width, alignment="right", font_size=14):
    c.setFont("IRANSans", font_size)

    # Reshape and apply BiDi to the Persian text
    reshaped_text = get_display(arabic_reshaper.reshape(content))

    # Split text into words
    words = reshaped_text.split(' ')
    lines = []
    current_line = ""

    # Build lines of text
    for word in words:
        test_line = current_line + (word + " ")  # Prepare the line with the next word
        line_width = c.stringWidth(test_line, 'IRANSans', font_size)

        # Check if the line exceeds max width
        if line_width <= max_width:
            current_line = test_line  # If it fits, add the word
        else:
            if current_line:  # If there's content in the current line, save it
                lines.append(current_line.strip())
            current_line = word + " "  # Start a new line with the current word

    if current_line:  # Append any remaining text
        lines.append(current_line.strip())

    # Draw each line and update y-position correctly
    for line in lines:
        if alignment == "center":
            c.drawCentredString(x, y, line)
        elif alignment == "left":
            c.drawString(x, y, line)
        else:  # Default is right alignment
            c.drawRightString(x, y, line)
        y -= font_size + 2  # Move down for the next line (line height + more space)

    return y  # Return the updated y position after drawing all lines


def render_to_pdf(response, request_name, request_date, request_details, selected_items):
    # Register Persian Font
    pdfmetrics.registerFont(TTFont('IRANSans', 'static/assets/fonts/Digi-Mitra-Rectangle-Bold.ttf'))

    # Create canvas for PDF
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Define margins
    left_margin = 1 * inch
    right_margin = width - 1 * inch
    text_width = right_margin - left_margin

    # Draw the border around the page
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)

    # Centered title ("In The Name Of God")
    y_position = height - 1 * inch
    y_position = draw_wrapped_text(c, "In The Name Of God", width / 2, y_position, text_width, alignment="center",
                                   font_size=10)

    # Left-aligned Request Name and Date
    y_position = draw_wrapped_text(c, f"Survey Name: {request_name}", left_margin, y_position - 0.25 * inch, text_width,
                                   alignment="left")
    y_position = draw_wrapped_text(c, f"Date: {request_date.strftime('%Y/%m/%d')}", left_margin, y_position, text_width,
                                   alignment="left")

    # Right-aligned Request Details with wrapping
    y_position = draw_wrapped_text(c, f"شرح: {request_details}", right_margin, y_position - 0.25 * inch, text_width,
                                   alignment="right")

    # Right-aligned header for the selected items list
    y_position = draw_wrapped_text(c, "موارد انتخاب شده:", right_margin, y_position - 0.25 * inch, text_width,
                                   alignment="right")

    # Right-aligned list of selected items
    for index, selected_item in enumerate(selected_items, start=1):
        item_name = f"{index}. {selected_item.item.title}"
        y_position = draw_wrapped_text(c, item_name, right_margin, y_position - 0.25 * inch, text_width,
                                       alignment="right")

    # Save the PDF
    c.showPage()
    c.save()


def pdf_view(request, request_id):
    # دریافت درخواست و موارد انتخاب شده برای درخواست
    current_request = get_object_or_404(Request, id=request_id)
    selected_items = SelectedItem.objects.filter(request=current_request)

    # ایجاد یک پاسخ PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{sanitize_filename(current_request.name)}.pdf"'

    # فراخوانی تابع render_to_pdf با پارامترهای صحیح
    render_to_pdf(response, current_request.name, current_request.created_at, current_request.details, selected_items)

    return response


def request_list_view(request):
    requests = Request.objects.all().order_by('-created_at')

    return render(request, 'Itemsapp/request_list.html', {'requests': requests})





# views.py
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
