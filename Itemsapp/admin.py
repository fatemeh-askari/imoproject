from django.contrib import admin
from .models import Item, Request, SelectedItem

# Customize the admin interface for the Item model
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date')  # Columns to display in the list view
    search_fields = ('title', 'category')         # Enable searching by title and category
    list_filter = ('category', 'date')            # Filters for category and date
    ordering = ('-date',)                         # Order by date descending
    exclude = ('description', 'category')  # حذف فیلدها از فرم جزئیات

# Customize the admin interface for the Request model
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')         # Columns to display in the list view
    search_fields = ('name',)                     # Enable searching by request name
    ordering = ('-created_at',)                   # Order by creation date descending

# Customize the admin interface for the SelectedItem model
@admin.register(SelectedItem)
class SelectedItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'request', 'added_at')    # Display item, associated request, and added date
    search_fields = ('item__title', 'request__name')  # Search by item title or request name
    list_filter = ('request', 'added_at')             # Filter by request and added date
    ordering = ('-added_at',)                         # Order by added date descending
