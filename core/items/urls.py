from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('item/<int:item_id>/mark-returned/', views.mark_as_returned, name='mark_as_returned'),
]