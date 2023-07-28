from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    #path('login/', views.user_login, name= 'login'),
    path('login/',auth_views.LoginView.as_view(), name ='login'),
    path('logout/',views.user_logout ,name ='logout'),
    path('',views.dashboard, name = 'dashboard'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]