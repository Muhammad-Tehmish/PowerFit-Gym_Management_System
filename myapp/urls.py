from django.contrib import admin
from django.urls import path
from myapp import views 

urlpatterns = [
    path("", views.index, name = 'myapp'), 
    path("index", views.index, name = 'index'),
    path("signin", views.signin, name = 'signin'),
    path('signup/', views.signup, name='signup'),
    path("admin-login", views.adminlogin, name = 'adminlogin'),
    path("admin-dashboard", views.admindashboard, name = 'admindashboard'),
    path("admin-dashboard-members", views.admindashboardmembers, name = 'admindashboardmembers'),
    path("admin-dashboard-trainers", views.admindashboardtrainers, name = 'admindashboardtrainers'),
    path("admin-dashboard-equipment", views.admindashboardequipment, name = 'admindashboardequipment'),
    path("admin-dashboard-plans", views.admindashboardplans, name = 'admindashboardplans'),
    path("member-dashboard", views.memberdashboard, name = 'memberdashboard'),
    path("member-dashboard-schedule", views.memberdashboardschedule, name = 'memberdashboardschedule'),
    path("member-dashboard-fee", views.memberdashboardfee, name = 'memberdashboardfee'),
    path('add-trainer', views.addtrainer, name='addtrainer'),
    path('delete_mem/<int:id>/', views.delete_mem, name='delete_mem'),
    # path('add_train/<int:id>/', views.add_train, name='add_train'),
    path('delete_train/<int:id>/', views.delete_train, name='delete_train'),
    path('update_plan/<str:name>/', views.update_plan, name='update_plan'),
] 