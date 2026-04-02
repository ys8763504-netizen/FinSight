from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_page,name='index_page'),
    path('admin_login_page/',views.admin_login_page,name='admin_login_page'),
    path('home/',views.home_page,name='home_page'),
    path('login/',views.login_form,name='login_form'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('registration/',views.regis_form,name='regis_form'),
    path('about/',views.about_page,name='about_page'),
    path('profile/',views.profile_page,name='profile_page'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('dashboard/',views.dashboard_page,name='dashboard_page'),
    path('expense/',views.expense_page,name='expense_page'),
    path('add_expanse/',views.add_expense,name='add_expense'),
    path('edit_expense/<int:id>/',views.edit_expense,name='edit_expense'),
    path('update_expense/<int:id>/',views.update_expense,name='update_expense'),
    path('delete_expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('budget_page/', views.budget_page, name='budget_page'),
    path('add_budget/',views.add_budget,name="add_budget"),
    path('edit_budget/<int:id>/',views.edit_budget,name="edit_budget"),
    path('update_budget/<int:id>/',views.update_budget,name='update_budget'),
    path('delete_budget/<int:id>/',views.delete_budget,name="delete_budget"),
    path('report/',views.report_page,name='report_page'),
    path('analytics/', views.analytics_page, name="analytics_page"),
    path('check_budget', views.check_budget, name='check_budget'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/', views.category_page, name='category_page'),
    path('delete_category/<int:id>/',views.delete_category,name="delete_category"),
    path('feedback/', views.feedback_page, name='feedback'),
    path('add_feedback/', views.add_feedback, name='add_feedback'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
   # USERS
    path('panel/delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('panel/edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('panel/update-user/<int:id>/', views.update_user, name='update_user'),

    # EXPENSES
    path('panel/delete-expense/<int:id>/', views.admin_delete_expense, name='admin_delete_expense'),
    path('panel/edit-expense/<int:id>/', views.admin_edit_expense, name='admin_edit_expense'),
    path('panel/update-expense/<int:id>/', views.admin_update_expense, name='admin_update_expense'),

    # BUDGETS
    path('panel/delete-budget/<int:id>/', views.admin_delete_budget, name='admin_delete_budget'),
    path('panel/edit-budget/<int:id>/', views.admin_edit_budget, name='admin_edit_budget'),
    path('panel/update-budget/<int:id>/', views.admin_update_budget, name='admin_update_budget'),

    # FEEDBACK
    path('panel/delete-feedback/<int:id>/', views.delete_feedback, name='delete_feedback'),
    path('panel/delete-category/<int:id>/', views.admin_delete_category, name='admin_delete_category'),

    path("goals/", views.goal_page, name="goal_page"),
    path("add_goal/", views.add_goal, name="add_goal"),
    path("add_saving/<int:id>/", views.add_saving, name="add_saving"),
    path("delete_goal/<int:id>/", views.delete_goal, name="delete_goal"),
]
