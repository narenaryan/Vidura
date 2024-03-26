from django.urls import include, path

import promptbook.register_models
from . import views
from rest_framework import routers

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # category
    path('', views.list_categories, name='index'),
    path('categories/', views.list_categories, name='list_categories'),
    path('create_category/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/toggle_pinned/', views.toggle_pinned_category, name='toggle_pinned_category'),

    #prompt
    path('categories/<int:category_id>/prompts/', views.list_prompts, name='list_prompts'),
    path('categories/<int:category_id>/labels/<int:label_id>/prompts/', views.list_prompts_by_label,
         name='list_prompts_by_label'),
    path('categories/<int:category_id>/prompts/new', views.create_or_edit_prompt, name='create_prompt'),
    path('categories/<int:category_id>/prompts/<int:prompt_id>/', views.create_or_edit_prompt, name='edit_prompt'),
    path('delete_prompt/<int:prompt_id>/', views.delete_prompt, name='delete_prompt'),

    # other
    path('search/', views.search, name='search'),
    path('activities/', views.list_activities, name='list_activities'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),

]

api_urls = [
    # add CategoryListCreateView to the urls
    path('api/', views.ApiRootView.as_view(), name='api-root'),
    path('api/categories/', views.CategoryListCreateView.as_view(), name='api-list-categories'),
    path('api/categories/<int:category_id>/prompts/', views.PromptsListCreateView.as_view(),
         name='api-list-category-prompts-by-id'),
    path('api/categories/<slug:category_name>/prompts/', views.PromptsListCreateView.as_view(),
         name='api-list-category-prompts-by-name'),
    path('api/categories/<int:category_id>/labels/', views.LabelListCreateView.as_view(),
         name='api-list-category-labels-by-id'),
    path('api/categories/<int:category_id>/models/', views.ModelListCreateView.as_view(),
         name='api-list-category-models-by-id'),
]

urlpatterns += api_urls

