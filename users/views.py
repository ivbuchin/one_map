from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from django.urls import reverse_lazy

from actions.models import Action
from .models import User
from followers.models import Follow


# Создание пользователя
class UserCreateView(CreateView):
    model = User
    fields = ['email', 'username', 'password', 'avatar', 'first_name', 'last_name', 'city', 'gender', 'age', 'master',
              'about_us', 'status']
    success_url = reverse_lazy('users:login')


# Редактирование данных пользователя
class UserUpdateView(UpdateView):
    model = User
    fields = ['email', 'username', 'avatar', 'first_name', 'last_name', 'city', 'gender', 'age', 'master',
              'about_us', 'status']
    template_name_suffix = '_update_form'


# Удаление пользователя
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('tutorial:main')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


# Вывод страницы пользователя
class UserDetailView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.pk == self.request.user.id:
            actions = Action.objects.exclude(user=self.request.user)
            new_actions = actions.filter(viewed=False)
            new_actions_count = new_actions.count()
            context['new_actions_count'] = new_actions_count
        context['subscriptions'] = Follow.objects.filter(user_from=self.object.pk)
        return context


# Вывод ленты пользователя
class UserFeedView(TemplateView):
    template_name = "users/feed.html"

    def get_context_data(self, **kwargs):
        actions = Action.objects.exclude(user=self.request.user)
        new_actions = actions.filter(viewed=False)
        for action in new_actions:
            action.viewed = True
            action.save()
        following_ids = self.request.user.following.values_list('id', flat=True)
        if following_ids:
            actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user').prefetch_related('target')[:10]
        context = super().get_context_data(**kwargs)
        context['actions'] = actions
        return context


# Вывод подписок пользователя
class UserSubscriptionsView(TemplateView):
    template_name = "users/subscriptions.html"

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriptions = Follow.objects.filter(user_from=pk)
        users = []
        for subscription in subscriptions:
            user_id = subscription.user_to.id
            user = User.objects.get(id=user_id)
            users.append(user)
        context['subscriptions'] = users
        return context


# Вывод подписчиков пользователя
class UserFollowersView(TemplateView):
    template_name = "users/followers.html"

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=pk)
        followers = user.followers.all()
        context['followers'] = followers
        return context
