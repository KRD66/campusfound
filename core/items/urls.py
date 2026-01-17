
from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]