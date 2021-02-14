from django.urls import path
from .views import register, UserLoginView, logout_user
urlpatterns = [
    path('accounts/signup', register, name='account_signup'),
    path('', UserLoginView.as_view(), name='account_login'),
    path('accounts/logout', logout_user, name='account_logout'),

]
