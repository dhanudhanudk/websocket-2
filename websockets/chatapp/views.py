from django.shortcuts import render,redirect
from django.views import View
from.models import *
from .forms import *
from .serializers import *
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView
from django.contrib import messages
from rest_framework.views import APIView, status,Response
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from django.db.models import Q
import json

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "user.html", context)

class LogoutView(TemplateView):
    def logout_view(request):
        logout(request)
        return redirect('login_page')
    

class RegisterView(TemplateView):
    template_name = 'register.html' 

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm() 
        return self.render_to_response({'form': form}) 

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            form.save()  
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login_page') 
        messages.error(request, "Please correct the errors below..")
        return redirect('register')
    
class LoginPage(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.data.get('email')
            password=form.data.get('password')

            user=authenticate(request,email=email,password=password)
            
            if user is not None:
                login(request,user)
                messages.success(request, "successfully log in.")
                return redirect('user_page')
            else:
                messages.error(request, "invalid email or password..")
                return redirect("login_page")
        else:
            messages.error(request, "Please correct the errors below..")
        return self.render_to_response({'form': form}) 

class UserList(TemplateView):
    template_name='user.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(id=self.request.user.id) 
        return context

class ChatHistoryView(ListAPIView):
    def get(self, request, sender_id, receiver_id):
        sender=User.objects.get(id=sender_id)
        receiver=User.objects.get(id=receiver_id)

        chat_history = MassageBox.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) |
            (Q(sender=receiver) & Q(receiver=sender))
        ).order_by('created_on')

        # Prepare chat messages for response
        messages = []
        for message in chat_history:
            messages.append({
                'sender': message.sender.name,
                'receiver': message.receiver.name,
                'message': message.message,
                'is_read': message.is_read,
                'created_on': message.created_on.isoformat(),  
            })

        return JsonResponse({'messages': messages}, status=200)
# class ChatHistoryView(ListAPIView):
#     def get(self, request, room_id):
    
#         chat_history = MassageBox.objects.filter(room_id=room_id).order_by('created_on')

#         # Prepare chat messages for response
#         messages = []
#         for message in chat_history:
#             messages.append({
#                 'sender': message.sender.name,
#                 'receiver': message.receiver.name,
#                 'message': message.message,
#                 'is_read': message.is_read,
#                 'created_on': message.created_on.isoformat(),  
#             })

#         return JsonResponse({'messages': messages}, status=200)

# class RoomChatCreated(APIView):

#     def post(self, request, receiver_id):
#         sender = request.user
#         receiver = User.objects.get(id=receiver_id)

#         if sender == receiver:
#             return JsonResponse({
#                 "message": "Cannot create a room with yourself"
#             }, status=status.HTTP_400_BAD_REQUEST)  # Use 400 for bad requests

#         # Ensure consistent order by user IDs to avoid duplicate rooms
#         room, created = ChatRoom.objects.get_or_create(
#             send_user=sender if sender.id < receiver.id else receiver,
#             receiv_user=receiver if sender.id < receiver.id else sender
#         )

#         room_data = ChatRoomSerializer(room).data
#         room_data["is_new"] = created

        # return JsonResponse(room_data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
