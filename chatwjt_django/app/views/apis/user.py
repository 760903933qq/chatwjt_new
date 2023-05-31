from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.core.cache import cache
from app.utils.utils import get_code, send_email
from app.serializers import EmailSerializer, UserSerializer, LoginSerializer, ForgetSerializer
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from app.models import CustomUser, Invite
from rest_framework.authtoken.models import Token


# 注册

@permission_classes([])
@authentication_classes([])
@api_view(['post'])
def register(request):
    ser = UserSerializer(data=request.data)
    if not ser.is_valid():
        return Response({'code': 400, 'msg': ser.errors})
    ser.save()
    return Response({'code': 200, 'msg': '注册成功'})


@permission_classes([])
@authentication_classes([])
@api_view(['get'])
def captcha(request):
    """注册发送邮箱"""

    ser = EmailSerializer(data=request.GET)
    if not ser.is_valid():
        return Response({'code': 400, 'msg': ser.errors})
    email = ser.data['email']
    if not cache.get(email):
        code = get_code()
        send_email(email, code)
        cache.set(email, code, timeout=60)
        return Response({'code': 200, 'msg': '验证码已发送'})
    else:
        return Response({'code': 400, 'msg': '发送失败,请间隔一分钟再发送'})


# 登陆
@permission_classes([])
@authentication_classes([])
@api_view(['post'])
def api_login(request):
    ser = LoginSerializer(data=request.data)
    if not ser.is_valid():
        return Response({'code': 400, 'msg': ser.errors})
    username = ser.data['username']
    user = CustomUser.objects.get(username=username)
    token, created = Token.objects.get_or_create(user=user)
    user.token = token
    user.save()
    login(request._request, user)
    return Response({'code': 200, 'msg': '登陆成功', 'data': {
        'token': token.key,
        'username': username,
        'id': user.id,
    }})


@permission_classes([])
@authentication_classes([])
@api_view(['post'])
def forget(request):
    ser = ForgetSerializer(data=request.data)
    if not ser.is_valid():
        return Response({'code': 400, 'msg': ser.errors})
    user = CustomUser.objects.filter(email=ser.data['email']).first()
    if not user:
        return Response({'code': 401, 'msg': '修改失败, 该用户不存在'})

    user.set_password(ser.data['password1'])
    user.save()
    return Response({'code': 200, 'msg': '修改成功'})


@api_view(['get'])
def home(request):
    user = request.user
    invite_code = user.invite.code
    invite_number = user.invite.claimed_by
    data = {
        'username': user.username,
        'invite_code': invite_code,
        'invite_number': invite_number
    }

    return Response({'code': 200, 'msg': '成功', 'data': data})
