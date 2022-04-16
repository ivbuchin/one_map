from django.urls import path
from . import views


app_name = 'forum'
urlpatterns = [
    path("", views.AllTopicsView.as_view(), name="all_topics"),
    path("search/", views.search_topics_or_messages, name="search"),
    path("filter/", views.filter_by_section, name="filter_by_section"),
    path("sorting/", views.sorting_topics, name="sorting_topics"),
    path("add_topic/", views.CreateTopicView.as_view(), name="create_topic"),
    path("<slug:slug>/", views.TopicDetailView.as_view(), name="topic_detail"),
    path("add_message/<int:pk>/", views.AddMessageView.as_view(), name="add_message"),
]
