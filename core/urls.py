from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name='core'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('login/', views.login_user, name='login'),
    path('account_info/', views.account_info, name='account_info'),
    path('profile/', views.dashboard, name='account'),
    path('logout/', views.logout_user, name='logout'),
    path('transfer/', views.transfer, name = 'transfer'),
    path('confirmation/', views.confirm_transaction, name='confirm_transaction'),
    path('transactions/', views.transactions, name='transactions'),
]
