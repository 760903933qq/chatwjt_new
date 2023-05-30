from django.db import models
from django.contrib.auth.models import AbstractUser
from cryptography.fernet import Fernet
from django_cryptography.fields import encrypt
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # 添加一个OneToOneField来关联Token模型
    token = models.OneToOneField(Token, on_delete=models.CASCADE, null=True, blank=True, verbose_name='用户令牌')
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Invite(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='邀请码')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='invite', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    claimed_by = models.PositiveIntegerField(default=0, verbose_name='邀请人数')

    def __str__(self):
        return self.code
    class Meta:
        verbose_name = '邀请表'
        verbose_name_plural = '邀请表'

class ChatLabel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_labels', verbose_name='用户')
    label = models.CharField(max_length=32, verbose_name='聊天标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class ChatRecord(models.Model):
    SENDER_CHOICES = (
        (0, 'User'),
        (1, 'AI'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_records')
    sender = models.IntegerField(choices=SENDER_CHOICES)
    label = models.ForeignKey(ChatLabel,on_delete=models.CASCADE, related_name='chat_records')
    key = Fernet.generate_key()
    message = encrypt(models.TextField())
    created_at = models.DateTimeField(auto_now_add=True)
