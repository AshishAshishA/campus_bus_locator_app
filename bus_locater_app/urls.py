from django.urls import path
from .views import route_list, route_update, route_create, route_delete, login_view, logout_view

urlpatterns = [
    
    path('', route_list, name='route-list'),
    path('route/update/<int:pk>/', route_update, name='route-update'),
    path('route/create/', route_create, name='route-create'),
    path('route/delete/<int:pk>/', route_delete, name='route-delete'),

    path('staff/login/', login_view, name='login'),
    path('staff/logout/', logout_view, name='logout'),
]