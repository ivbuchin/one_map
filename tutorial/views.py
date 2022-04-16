from django.views.generic.base import View
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.db.models import F, Q

from .models import Lesson, Branch
from .forms import CommentForm


# Вывод всех уроков постранично
class LessonsView(ListView):
    paginate_by = 3
    model = Lesson
    queryset = Lesson.objects.filter(draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['branchs'] = Branch.objects.all()
        context['most_popular_lessons'] = Lesson.objects.order_by('-count')[:3]
        context['url_name'] = 'main'
        return context


# Фильтр уроков по ветке
class FilterByBranchView(ListView):
    template_name = 'tutorial/lesson_list.html'
    paginate_by = 3

    def get_queryset(self):
        branch = Branch.objects.get(id=self.kwargs['pk'])
        print(self.kwargs['pk'])
        return Lesson.objects.filter(branch=branch)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["url_name"] = "filter_by_branch"
        context["branchs"] = Branch.objects.all()
        context["most_popular_lessons"] = Lesson.objects.order_by('-count')[:3]
        return context


# Вывод страницы со всеми уроками, классифицированными по ветке
class LessonsByBranchView(TemplateView):
    template_name = "tutorial/lessons_by_branch.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['branchs'] = Branch.objects.all()
        context['lessons'] = Lesson.objects.filter(draft=False)
        context['url_name'] = 'lessons_by_branch'
        return context


# Вывод страницы урока
class LessonDetailView(DetailView):
    model = Lesson
    slug_field = "url"

    def get_context_data(self, **kwargs):
        Lesson.objects.filter(pk=self.object.pk).update(count=F('count') + 1)
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["branchs"] = Branch.objects.all()
        context['most_popular_lessons'] = Lesson.objects.order_by('-count')[:3]
        return context


# Вывод страницы "О нас"
class AboutUsView(TemplateView):
    template_name = "about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'about_us'
        return context


# Добавление лайка к уроку
class AddLikeView(View):
    def get(self, request, pk):
        try:
            if str(pk) in request.COOKIES:
                return redirect('/')
            else:
                lesson = Lesson.objects.get(id=pk)
                lesson.likes += 1
                lesson.save()
                response = redirect(request.META.get('HTTP_REFERER'))
                response.set_cookie(str(pk), "liked")
                return response
        except ObjectDoesNotExist:
            raise Http404


# Удаление лайка к уроку
class RemoveLikeView(View):
    def get(self, request, pk):
        if str(pk) in request.COOKIES:
            lesson = Lesson.objects.get(id=pk)
            lesson.likes -= 1
            lesson.save()
            response = redirect(request.META.get('HTTP_REFERER'))
            response.delete_cookie(str(pk))
            return response


# Добавление комментария к уроку
class AddCommentView(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        lesson = Lesson.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.lesson = lesson
            form.save()
        return redirect(lesson.get_absolute_url())


# Вывод результата поиска
class SearchView(ListView):
    template_name = 'tutorial/search_list.html'

    def get_queryset(self):
        return Lesson.objects.filter(Q(title__icontains=self.request.GET.get("q")) |
                                     Q(description__icontains=self.request.GET.get("q")) |
                                     Q(content__icontains=self.request.GET.get("q")) |
                                     Q(task__icontains=self.request.GET.get("q")))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        context["url_name"] = "search"
        return context
