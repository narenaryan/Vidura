from django.urls import include, path

import promptbook.register_models
from . import views
from rest_framework import routers

urlpatterns = [
    path('login/', views.login, name='login'),
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/<int:category_id>/prompts/', views.list_prompts, name='list_prompts'),
    path('logout/', views.logout, name='logout'),
    path('prompts/edit/<int:prompt_id>/', views.edit_prompt, name='edit_prompt'),
    path('toggle-prompt-public/<int:prompt_id>/', views.toggle_prompt_public, name='toggle_prompt_public'),
    # clone prompt
    path('prompts/clone/<int:prompt_id>/', views.clone_public_prompt, name='clone_public_prompt'),
    path('labels/<int:label_id>/prompts/', views.list_prompts_by_label, name='list_prompts_by_label'),
    path('editor/', views.editor, name='editor'),
    path('delete_prompt/<int:prompt_id>/', views.delete_prompt, name='delete_prompt'),
    path('search/', views.search, name='search'),
    path('', views.activity_stream, name='index'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('create_category/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/toggle_pinned/', views.toggle_pinned_category, name='toggle_pinned_category'),
]

api_urls = [
    # add CategoryListCreateView to the urls
    path('api/categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('api/categories/<int:category_id>/prompts/', views.CategoryPromptsListCreateView.as_view(),
         name='category-prompts-list'),
    path('api/labels/', views.LabelListCreateView.as_view(), name='label-list'),
]

urlpatterns += api_urls