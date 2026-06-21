from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.home_view, name='home'),

    # Members
    path('members/', views.member_list_view, name='member_list'),
    path('members/register/', views.member_create_view, name='member_create'),
    path('members/<int:pk>/', views.member_detail_view, name='member_detail'),
    path('members/<int:pk>/edit/', views.member_edit_view, name='member_edit'),

    # Polling Stations
    path('stations/', views.station_list_view, name='station_list'),
    path('stations/add/', views.station_create_view, name='station_create'),
    path('stations/<int:pk>/', views.station_detail_view, name='station_detail'),
    path('stations/<int:pk>/edit/', views.station_edit_view, name='station_edit'),
    path('station/<int:pk>/export', views.export_data, name='export_data'),

    # Electoral Area
    path('electoral-areas/', views.electoral_area_list_view, name='area_list'),
    path('electoral-area/add/',views.electoral_area_create_view,name='area_create'),
    path('electoral-area/<int:pk>/', views.electoral_area_details_view, name='area_detail'),

    # Admin Dashboard (staff only — NOT the Django /admin/ panel)
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/users/<int:user_id>/toggle/', views.admin_user_toggle_view, name='admin_user_toggle'),
    path('admin-panel/users/<int:user_id>/delete/', views.admin_user_delete_view, name='admin_user_delete'),

   
]
