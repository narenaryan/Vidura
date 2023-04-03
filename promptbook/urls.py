from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/<int:category_id>/prompts/', views.list_prompts, name='list_prompts'),
    path('logout/', views.logout, name='logout'),
    path('prompts/edit/<int:prompt_id>/', views.edit_prompt, name='edit_prompt'),
    path('labels/<int:label_id>/prompts/', views.list_prompts_by_label, name='list_prompts_by_label')
]
