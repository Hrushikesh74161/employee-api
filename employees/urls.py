from django.urls import path
from rest_framework.routers import DefaultRouter

from employees import views

router = DefaultRouter(trailing_slash=False)
router.register('employee', views.EmployeeViewSet)
urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('register', views.UserRegisterView.as_view(), name='register'),
]
urlpatterns += router.urls
