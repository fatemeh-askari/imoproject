from django.utils import timezone
from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=1000)
    short_description = models.CharField(max_length=2000, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=300, blank=True)
    date = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.title

class Request(models.Model):
    name = models.CharField(max_length=500, verbose_name='Ship Name')
    details = models.TextField(blank=True, verbose_name='Subject')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class SelectedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)  # Link selected items to a request
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.title} for {self.request.name}"


class RequestDetail(models.Model):
    request = models.ForeignKey(Request, related_name='request_details', on_delete=models.CASCADE)  # تغییر related_name
    detail_spacial = models.TextField(blank=True, verbose_name='Add Item ')
    description_spacial = models.TextField(blank=True)
