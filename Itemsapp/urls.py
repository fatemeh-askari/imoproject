# urls.py
from django.urls import path
from . import views
from .views import request_list_view, pdf_view
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('create-request/', views.create_request, name='create_request'),
    path('request/<int:request_id>/items/', views.item_list_for_request, name='item_list_for_request'),
    path('request/<int:request_id>/add_to_selected/<int:pk>/', views.add_to_selected_for_request, name='add_to_selected_for_request'),
    path('request/<int:request_id>/remove_from_selected/<int:pk>/', views.remove_from_selected_for_request, name='remove_from_selected_for_request'),
    path('request/<int:request_id>/selected_items/', views.selected_items_list_for_request, name='selected_items_list_for_request'),
    path('request/<int:request_id>/pdf/', pdf_view, name='pdf_view'),
    path('requests/', request_list_view, name='request_list'),

    path('', views.custom_login, name='custom_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='custom_login'), name='logout'),
    path('request/<int:request_id>/delete-detail/<int:detail_id>/', views.delete_request_detail, name='delete_request_detail'),
    path('request/<int:request_id>/delete-details/<int:detail_id>/', views.delete_request_details, name='delete_request_details'),
    path('get-selected-items/<int:request_id>/', views.get_selected_items, name='get_selected_items'),
    path('update-item-selection/<int:request_id>/<int:item_id>/', views.update_item_selection, name='update_item_selection'),
    # path('update-item-selection/<int:item_id>/<int:request_id>/', views.update_item_selection, name='update_item_selection'),
    # path('selected-items/<int:request_id>/', views.get_selected_items, name='get_selected_items'),






]
