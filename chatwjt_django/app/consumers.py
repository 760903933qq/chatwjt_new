import json
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone
from channels.db import database_sync_to_async
import os
import openai
import asyncio


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        from app.models import ChatRecord, ChatLabel
        super().__init__(*args, **kwargs)
        self.id = -1
        self.len = 0
        self.chat_list = []
        self.chat_label_list = []
        self.user = None
        self.Chat_record = ChatRecord
        self.Chat_label = ChatLabel
        self.chat_record = None
        self.label = None
        openai.api_key = os.environ.get('OPEN_AI_KEY')

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.save_chat()

    async def receive(self, text_data):

        if text_data == 'ping':
            await self.send('pong')
        # 验证用户
        elif text_data.startswith('token'):
            token = text_data.split(' ')[1]
            User = get_user_model()
            self.user = await User.objects.aget(token=token)
            await self.send_message(self.chat_list)
        # 获取聊天标签
        elif text_data == 'getchatlableshc93h4uh2g4i9a':
            await self.get_chat_label()
            response = {
                'status': 'chat_label',
                'chat_label': self.chat_label_list
            }
            response = json.dumps(response)
            await self.send(response)
        # 获取聊天列表
        elif text_data.startswith('chatlistjoidwaj98y4h0h1c4'):
            await self.save_chat()
            self.chat_list = []
            self.id = -1
            label = text_data.split(' ')[1]
            await self.get_chat_list(label)
            self.label = label

            if self.chat_list:
                await self.send_message(self.chat_list)

        # 新增聊天
        elif text_data.startswith('addLabel0j13e09ujv09ujdv0s8ujv12-'):
            label = text_data.split(' ')[1]
            await self.Chat_label.objects.acreate(
                user=self.user,
                label=label
            )
            await self.get_chat_label()
            response = {
                'status': 'add_success',
            }
            response = json.dumps(response)
            await self.send(response)
        # 删除聊天
        elif text_data.startswith('delLabel0dha0shd10nv09isad-34'):
            label = text_data.split(' ')[1]
            await self.del_label(label)
            self.label = None
            response = {
                'status': 'del_success',
            }
            response = json.dumps(response)
            await self.send(response)
        # 回复消息
        else:
            data = json.loads(text_data)
            content = data['content']
            star = data['star']
            id1 = self.get_id()
            self.add_chat(data=content)

            ai_response = await self.response(star)

            self.add_chat(ai_response, sender=1)

    @database_sync_to_async
    def del_label(self, label):
        if label:
            self.Chat_label.objects.filter(label=label).delete()
        return

    def add_chat(self, data, sender=0):
        if sender == 0:
            _chat = {
                'id': self.id,
                'sender': 0,
                'content': data,
                'time': timezone.now()
            }
            self.chat_list.append(_chat)
        else:
            _chat = {
                'id': self.id,
                'sender': 1,
                'content': data,
                'time': timezone.now()
            }
            self.chat_list.append(_chat)

    @database_sync_to_async
    def get_chat_list(self, label):
        chat_label = self.Chat_label.objects.filter(user=self.user, label=label).first()
        if chat_label:
            chat_records = chat_label.chat_records.order_by('-created_at')[:20]
            self.len = len(chat_records)
            for chat_record in reversed(chat_records):
                _chat = {
                    'id': self.get_id(),
                    'sender': chat_record.sender,
                    'content': chat_record.message,
                    'time': chat_record.created_at
                }
                self.chat_list.append(_chat)
            return self.chat_list

    @database_sync_to_async
    def get_chat_label(self):
        chat_labels = self.Chat_label.objects.filter(user=self.user).order_by('-created_at')
        for chat_label in reversed(chat_labels):
            self.chat_label_list.append(chat_label.label)
        return

    def get_id(self):
        self.id += 1
        return self.id

    async def send_message(self, data):
        if isinstance(data, list):
            for chat in data:
                response = {'id': chat['id'], 'sender': chat['sender'], 'content': chat['content'], 'star': False}
                response = json.dumps(response)

                await self.send(response)

    async def save_chat(self):
        if self.user and self.label:
            label = await self.Chat_label.objects.aget(user=self.user, label=self.label)
            for chat in self.chat_list[self.len:]:
                await self.Chat_record.objects.acreate(
                    sender=chat['sender'],
                    message=chat['content'],
                    user=self.user,
                    created_at=chat['time'],
                    label=label
                )

    async def response(self, star):
        results = []
        messages = []
        if star:
            results = [self.chat_list[i] for i in star]
        results.append(self.chat_list[-1])
        for result in results:
            role = 'user' if result['sender'] == 0 else 'assistant'
            messages.append({'role': role, 'content': result['content']})


        try:

            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            stream=True
            )
            collected_response = []
            completion_text = ' '
            id = self.get_id()
            for chunk in completion:
                collected_response.append(chunk)
                event_text = chunk['choices'][0]['delta']
                if 'content' in event_text:
                    content = event_text['content']
                    completion_text += content
                    response = {'id': id, 'sender': 1, 'content': content, 'star': True}
                    response = json.dumps(response)
                    await asyncio.sleep(0.00001)
                    await self.send(response)
            return completion_text
        except:
            return '出错了, 请刷新页面'
