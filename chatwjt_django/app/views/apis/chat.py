from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['get'])
def right(request):
    user = request.user
    count =  user.chat_records.count()
    if count > 50:
        i = user.invite.claimed_by
        if i < 3:
            return Response({'code': 201, 'msg': '您的聊天内容超过50句,请在邀请3人注册后继续使用'})
    return Response({'code': 200, 'msg': '成功'})