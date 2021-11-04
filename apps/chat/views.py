from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .models import PrivateChat

UserModel = get_user_model()


class IndexPageView(TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            context = {'users': UserModel.objects.filter(~Q(id=user.id))}
        else:
            context = {}
        return context


class PrivateChatView(View):
    def get(self, request, user2_id):
        user1 = self.request.user

        if not user1.is_authenticated:
            return HttpResponseForbidden()

        if user1.id == user2_id:
            return HttpResponseForbidden()
        # TODO create PrivateChat

        private_chat = PrivateChat.objects.get_or_create(user1_id=user1.id, user2_id=user2_id)
        print(private_chat)
        context = {}
        return render(request, 'chat/private_chat.html', context=context)
