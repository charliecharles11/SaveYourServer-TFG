from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view_data/<str:pk>/', views.view_data, name='view_data'),
    path('delete_user/<str:pk>/', views.deleteUser, name='delete_user'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('files/', views.file_list, name='file_list'),
    path('who_are_we/', views.who_are_we, name='who_are_we'),
    path('privacity/', views.privacity, name='privacity'),
    path('terms/', views.terms, name='terms'),
    path('how_it_works/', views.how_it_works, name='how_it_works'),

    path('notification/', views.notification, name='notification'),
    path('show/<str:notification_id>', views.show_notification, name='show_notification'),
    path('delete/<str:notification_id>', views.delete_notification, name='delete_notification'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
