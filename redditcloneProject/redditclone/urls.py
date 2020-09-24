from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('home', views.home.as_view(), name='home'),
    path('registration', views.registration.as_view(), name='registration'),
    path('login/', views.loginView.as_view(), name='login'),
    path('create_tread', views.treadCreate.as_view(), name='create_tread'),
    path('tread/<int:tread_id>', views.tread.as_view(), name='tread'),
    path('edit_comment/<int:comment_id>', views.edit.as_view(), name='edit_comment'),
    path('logout', views.logoutView.as_view(), name='logout'),
    path('comments/', include('django_comments.urls')),
]