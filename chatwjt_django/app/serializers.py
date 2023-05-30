from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers
from app.models import CustomUser, Invite, ChatRecord, ChatLabel
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from app.utils.utils import generate_invite_code

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError('Invalid email format')
        return value

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2,max_length=20)
    password1 = serializers.CharField(min_length=6,max_length=32, write_only=True)
    password2 = serializers.CharField(min_length=6,max_length=32, write_only=True)
    email = serializers.EmailField()
    invitation = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    captcha = serializers.CharField(max_length=4)

    def validate(self, data):
        # 检查密码是否匹配
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("密码不匹配")
        # 检查验证码是否正确
        captcha_local = cache.get(data['email'])
        if data['captcha'] != captcha_local:  # 这里假设验证码是固定的'1234'
            raise serializers.ValidationError("验证码不匹配")
        # 检查电子邮件是否已经注册
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return data

    def create(self, validated_data):
        invite_code = generate_invite_code()
        # 创建新用户
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        code = validated_data.get('invitation')
        if code:
            invite = Invite.objects.filter(code=code).first()
            if invite:
                invite.claimed_by += 1
                invite.save()
        Invite.objects.create(code=invite_code, user=user)
        label = ChatLabel.objects.create(user=user, label='新聊天标签')
        ChatRecord.objects.create(sender=1, message='您好,有什么可以帮您的吗?', label=label, user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2,max_length=20)
    password = serializers.CharField(min_length=6,max_length=32, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        print(username, password)
        if not user:
            raise serializers.ValidationError('用户名密码不匹配')

        return data

class ForgetSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=6, max_length=32)
    password2 = serializers.CharField(min_length=6, max_length=32)
    email = serializers.EmailField()
    captcha = serializers.CharField(max_length=4)

    def validate(self, data):
        # 检查密码是否匹配
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("密码不匹配")
        # 检查验证码是否正确
        captcha_local = cache.get(data['email'])
        if data['captcha'] != captcha_local:  # 这里假设验证码是固定的'1234'
            raise serializers.ValidationError("验证码不匹配")
        return data


