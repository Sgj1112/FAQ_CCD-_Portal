from django.contrib import admin
from django.urls import path, include
from tutorial import views

urlpatterns = [
    path('tutorial/', include('tutorial.urls')),
    path('ask/', views.ask, name='ask'),
    path('admin/', admin.site.urls),
]