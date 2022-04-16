from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'
urlpatterns = [
    path("profile/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("edit_profile/<int:pk>/", views.UserUpdateView.as_view(), name="edit_profile"),
    path("profile/<int:pk>/feed/", views.UserFeedView.as_view(), name="feed"),
    path("profile/<int:pk>/subscriptions/", views.UserSubscriptionsView.as_view(), name="subscriptions"),
    path('profile/<int:pk>/followers/', views.UserFollowersView.as_view(), name="followers"),
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("delete_user/<int:pk>/", views.UserDeleteView.as_view(), name="delete_user"),

    path("password_change/",
         auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html',
                                               success_url=reverse_lazy('users:password_change_done')),
         name='password_change'),
    path("password_change/done/",
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),

    path("password_reset/",
         auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                              email_template_name='users/password_reset_email.html',
                                              subject_template_name='users/password_reset_subject.txt',
                                              success_url=reverse_lazy('users:password_reset_done'),),
         name="password_reset"),
    path("password_reset_confirm/<uidb64>/<token>",
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                     success_url=reverse_lazy('users:password_reset_complete'),),
         name="password_reset_confirm"),
    path("password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path("password_reset/complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
