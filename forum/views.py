from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F, Q
from django.shortcuts import render
from django.http import HttpResponseNotFound

from actions.utils import create_action
from .models import Section, Topic, Message


# Вывод всех топиков постранично
class AllTopicsView(ListView):
    paginate_by = 5
    model = Topic
    ordering = ['-datetime']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        context['url_name'] = 'workshop'
        return context


# Фильтр топиков по секции
def filter_by_section(request):
    print(request.GET.get('section_id'))
    section_id = request.GET.get('section_id')
    try:
        section = Section.objects.get(id=section_id)
    except:
        return HttpResponseNotFound('<h1>Нет топиков в этой секции</h1>')

    topics_of_section = Topic.objects.filter(section=section)
    return render(request, 'forum/topics_of_section.html', {'topics': topics_of_section})


# Сортировка топиков
def sorting_topics(request):
    sorting = request.GET.get('sorting')
    active_section_id = request.GET.get('active_section_id')

    if not active_section_id:
        if sorting == "latest":
            topic_list = Topic.objects.order_by('-datetime')
        elif sorting == "popular":
            topic_list = Topic.objects.order_by('-views')
        elif sorting == "solved":
            topic_list = Topic.objects.order_by('-solved')
        elif sorting == "unsolved":
            topic_list = Topic.objects.order_by('solved')
        elif sorting == "no_replies_yet":
            topic_list = Topic.objects.filter(messages=None).order_by('-datetime')
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return render(request, 'forum/sorting_list.html', {'topic_list': topic_list})

    else:
        try:
            section = Section.objects.get(id=active_section_id)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        topics_of_section = Topic.objects.filter(section=section)

        if sorting == "latest":
            topic_list = topics_of_section.order_by('-datetime')
        elif sorting == "popular":
            topic_list = topics_of_section.order_by('-count')
        elif sorting == "solved":
            topic_list = topics_of_section.order_by('-solved')
        elif sorting == "unsolved":
            topic_list = topics_of_section.order_by('solved')
        elif sorting == "no_replies_yet":
            topic_list = topics_of_section.filter(topic__messages=None).order_by('-datetime')
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return render(request, 'forum/sorting_list.html', {'topic_list': topic_list})


# Вывод страницы топика
class TopicDetailView(DetailView):
    model = Topic
    slug_field = "url"

    def get_context_data(self, **kwargs):
        Topic.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        context['url_name'] = "workshop"
        return context


# Создание топика
class CreateTopicView(CreateView):
    model = Topic
    fields = ["title", "text", "section"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.url = str(Topic.objects.last().pk + 1)
        self.object.save()
        create_action(self.request.user, 'create topic', self.object)
        return HttpResponseRedirect(self.get_success_url())


# Добавление сообщения
class AddMessageView(CreateView):
    model = Message
    fields = ["text"]

    def post(self, request, pk):
        form = self.get_form()

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.topic = Topic.objects.get(id=pk)
            self.object.save()
            create_action(self.request.user, 'write message', self.object)
            return HttpResponseRedirect(self.get_success_url())


# Поиск топиков и сообщений
def search_topics_or_messages(request):
    query = request.GET.get("q")
    topics = Topic.objects.filter(Q(title__icontains=query) |
                                  Q(text__icontains=query))
    messages = Message.objects.filter(Q(text__icontains=query))

    return render(request, "forum/search_result.html", {'topics': topics, 'messages': messages,
                                                        'q': query})
