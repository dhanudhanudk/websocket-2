from django.urls import path
from .views import *
from chatapp import views as chat_views
from . import views
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', LoginPage.as_view(), name='login_page'),
    path('user/', UserList.as_view(), name='user_page'),
    path('chat_history/<int:sender_id>/<int:receiver_id>/', ChatHistoryView.as_view(), name='get_chat_history'),
    path("chatroom/", chat_views.chatPage, name="chat_page"),
    path("auth/logout/", LogoutView.as_view(), name="logout_user"),
    # path('room/<str:receiver_id>/', RoomChatCreated.as_view(), name='chat_room'),
    # path("chatroom/", create_room.as_view(), name="chatroom"),
]

