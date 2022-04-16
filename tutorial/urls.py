from django.urls import path
from . import views


app_name = 'tutorial'
urlpatterns = [
    path("", views.LessonsView.as_view(), name="main"),
    path("lessons_by_branch/", views.LessonsByBranchView.as_view(), name="lessons_by_branch"),
    path("filter/<int:pk>/", views.FilterByBranchView.as_view(), name="filter_by_branch"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<slug:slug>/", views.LessonDetailView.as_view(), name="lesson_detail"),
    path("add_like/<int:pk>/", views.AddLikeView.as_view(), name="add_like"),
    path("remove_like/<int:pk>/", views.RemoveLikeView.as_view(), name="remove_like"),
    path("comment/<int:pk>/", views.AddCommentView.as_view(), name="add_comment"),
]
