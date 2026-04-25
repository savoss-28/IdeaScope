from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('analyze/', views.analyze_idea_view, name='analyze'),
    path('result/<int:idea_id>/', views.result, name='result'),
    path('compare/', views.compare_ideas, name='compare'),
    path('delete/<int:idea_id>/', views.delete_idea, name='delete_idea'),
    path('generate-insights/', views.generate_insights_api, name='generate_insights'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
]
