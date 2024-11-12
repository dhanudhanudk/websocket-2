from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, email, phonenumber, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, phonenumber=phonenumber, **extra_fields)
        user.set_password(password)  # This hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phonenumber, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, phonenumber, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = None
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=100, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Add this line

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phonenumber']

    def __str__(self):
        return self.email

class ChatRoom(models.Model):
    room_name=models.CharField(max_length=50,unique=True)
    send_user= models.ForeignKey(User, related_name="chat_room_send",on_delete=models.CASCADE,null=True)
    receiv_user= models.ForeignKey(User, related_name="chat_room_recipient",on_delete=models.CASCADE,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        db_table="chatroom"

class MassageBox(models.Model):
    sender= models.ForeignKey(User,related_name="sender_user",on_delete=models.CASCADE)
    receiver= models.ForeignKey(User,related_name="receiver_user",on_delete=models.CASCADE)
    room= models.ForeignKey(User,related_name="room_name",on_delete=models.CASCADE,null=True)
    message= models.TextField(null=True)
    is_read= models.BooleanField(default=False, null= True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        db_table="Messagebox"