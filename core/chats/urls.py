from django.urls import path
from . import views

app_name = 'chats'  # Changed from 'messages'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<int:item_id>/', views.start_conversation, name='start_conversation'),
]