import random
from django.core.mail import send_mail
import string


def send_email(email, code):
    send_mail(
        subject='验证码',
        message=f'您的验证码是{code}, 请在1分钟内注册。',
        from_email='760903933@qq.com',
        recipient_list=[email],
        fail_silently=False,
    )


def get_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code

def generate_invite_code(length=20):
    """
    生成指定长度的随机邀请码
    """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))