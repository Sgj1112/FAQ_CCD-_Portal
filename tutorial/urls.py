from django.urls import path
from django.conf.urls import url
from . import views
from .views import PostUpdateView,PostDeleteView
from django.contrib.auth.decorators import login_required

urlpatterns = [
  # /tutorial
  path('', views.home, name='home'),
  path('signin/', views.sign_in, name='signin'),
  path('callback/', views.callback, name='callback'),
  path('signout/', views.sign_out, name='signout'),
  path('search/', views.search_ques, name='search_ques'),
  path('sort/', views.sort_ques, name='sort_ques'),
  path('myquestions/', views.my_ques, name='my_ques'),
  path('all/', views.all, name='all'),
  path('ques/<int:pk>/update/', PostUpdateView.as_view(), name='ques-update'),
  path('ques/<int:pk>/delete/', PostDeleteView.as_view(), name='ques-delete'),
  url(r'^(?P<slug>[\w-]+)/like/$', views.PostLikeToggle.as_view(), name='like-toggle'),

]