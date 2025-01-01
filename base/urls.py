from django.urls import path
from . import views
from .views import login_view


urlpatterns = [


    path('login/', views.loginPage, name='login'),
    path('login/', login_view, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('',views.home,name='home'),
    path('room/<str:pk>/' , views.room, name='room'),
    path('user-Profile/<str:pk>/' , views.userProfile, name='user-Profile'),

    path('create-room/' , views.create_room, name='create-room'),

    path('update-room/<str:pk>' , views.update_room, name='update-room'),

    path('delete-room/<str:pk>' , views.delete_room, name='delete-room'),
    path('deleteMessage/<str:pk>', views.deleteMessage, name='deleteMessage')

]



