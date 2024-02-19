import json
import reversion
from enum import Enum

from django.db import transaction, IntegrityError
from django.db.models import Count
from .models import Category, Prompt, Label, LLMModel
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Exists, OuterRef
from django.db.models import Count, Max
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Cast
from django.db.models import IntegerField

from actstream import action
from actstream.models import Action
from rest_framework import viewsets, permissions
from promptbook.serializers import (
    CategorySerializer,
    PromptSerializer,
    LabelSerializer,
    LLMModelSerializer
)

from django.utils.translation import gettext as _

# API根视图
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse as drf_reverse


class PrompVisibility(Enum):
    yes = 'yes'
    no = 'no'


@login_required(login_url='/login/')
def list_categories(request):
    user = request.user
    # Only get categories of user
    categories = Category.objects.filter(owner=user).annotate(
        num_prompts=Count('prompt'),
        last_updated=Max('prompt__modified_at')
    )
    # Get two most recent prompts for each category
    for category in categories:
        category.recent_prompts = category.prompt_set.order_by('-modified_at')[:2]

    # Get only pinned categories for this user
    pinned_categories = categories.filter(pinned_by=user)
    unpinned_categories = categories.exclude(pinned_by=user)

    context = {'categories': categories, 'pinned_categories': pinned_categories,
               'unpinned_categories': unpinned_categories}
    return render(request, 'list_categories.html', context)


@login_required(login_url='/login/')
def list_prompts(request, category_id):
    category = Category.objects.get(pk=category_id, owner=request.user)
    # Show prompts that belong to the current user
    prompts = category.prompt_set.order_by('-created_at')

    return render(request, 'list_prompts.html', {
        'category': category,
        'prompts': prompts,
    })


@login_required(login_url='/login/')
def list_prompts_by_label(request, category_id, label_id):
    label = get_object_or_404(Label, pk=label_id, category_id=category_id)

    # prompt_labels = PromptLabel.objects.filter(label=label)
    # prompts = [pl.prompt for pl in prompt_labels]

    prompts = label.prompts.all()

    return render(request, 'list_prompts_by_label.html', {'label': label, 'prompts': prompts})


# @csrf_exempt
# @login_required(login_url='/login/')
# def edit_prompt(request, prompt_id):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             prompt = Prompt.objects.get(pk=prompt_id)
#             prompt.text = data.get('text', prompt.text)
#             prompt.save()
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def create_or_edit_prompt(request, category_id, prompt_id=None):
    print('create_or_edit_prompt', category_id, prompt_id)
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        prompt_name = request.POST['prompt_name']
        prompt_text = request.POST['prompt_text']
        selected_label_ids = request.POST.getlist('labels')
        selected_labels = Label.objects.filter(id__in=selected_label_ids)
        selected_model_ids = request.POST.getlist('models')
        selected_models = LLMModel.objects.filter(id__in=selected_model_ids)

        if prompt_id:
            prompt = get_object_or_404(Prompt, pk=prompt_id, category=category)
            prompt.name = prompt_name
            prompt.text = prompt_text
        else:
            prompt = Prompt(category=category, name=prompt_name, text=prompt_text)
        try:
            with transaction.atomic():
                # 尝试保存，这里是可能会触发IntegrityError的操作
                prompt.save()
                prompt.labels.set(selected_labels)
                prompt.llm_models.set(selected_models)
        except IntegrityError as e:
            # load the same page with an error message
            return render(request, 'create_or_edit_prompt.html', {
                'category': category,
                'prompt_name': prompt_name,
                'prompt_text': prompt_text,
                'selected_labels': selected_labels,
                'selected_models': selected_models,
                'error_message': _('A prompt with this text already exists. Please enter a different prompt.'),
            })
        if prompt_id:
            action.send(request.user, verb='modified', target=prompt)
        else:
            action.send(request.user, verb='created', target=prompt)

        return HttpResponseRedirect(reverse('list_prompts', args=[category_id]))
    else:

        if prompt_id:
            prompt = get_object_or_404(Prompt, pk=prompt_id, category=category)
            return render(request, 'create_or_edit_prompt.html', {
                'category': category,
                'prompt_name': prompt.name,
                'prompt_text': prompt.text,
                'selected_labels': prompt.labels.all(),
                'selected_models': prompt.llm_models.all(),
            })
        else:
            return render(request, 'create_or_edit_prompt.html', {
                'category': category,
            })


def login(request):
    if request.method == "POST":
        # Get the username and password from the request body
        body = request.body.decode("utf-8")
        data = json.loads(body)
        username = data.get("username")
        password = data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # If the user is authenticated, log them in and redirect to the dashboard
        if user is not None:
            auth_login(request, user)
            return redirect("list_categories")

        # If the user is not authenticated, display an error message
        else:
            error_message = "Invalid username or password"
            return HttpResponseBadRequest(error_message)

    # If the request method is not POST, render the login form
    else:
        if request.user.is_authenticated:
            return redirect('list_categories')
        return render(request, "login.html")


def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
def delete_prompt(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id, category__owner=request.user)
    prompt.delete()
    return JsonResponse({'status': 'success'})


@login_required
def search(request):
    query = request.GET.get('q', '')

    found_categories = Category.objects.filter(name__icontains=query)
    found_prompts = Prompt.objects.filter(text__icontains=query)

    context = {
        'query': query,
        'found_categories': found_categories,
        'found_prompts': found_prompts,
    }

    return render(request, 'search_results.html', context)


@login_required(login_url='/login/')
def list_activities(request):
    # This version properly type casts SQL queries to SQLite, PostgreSQL databases
    # 我有权限的category下的所有的prompt
    prompts = Prompt.objects.filter(Q(category__owner=request.user))
    actions = Action.objects.annotate(
        target_object_id_as_integer=Cast('target_object_id', IntegerField())
    ).filter(
        Q(target_object_id_as_integer__in=prompts.values_list(
            'id', flat=True), target_content_type=ContentType.objects.get_for_model(Prompt)),
        Q(verb="created") | Q(verb="modified")
    )

    return render(request, 'list_activities.html', {'actions': actions})


@login_required(login_url='/login/')
def upload_avatar(request):
    if request.method == 'POST':

        if not request.FILES:
            error_message = "Invalid file uploaded"
            return HttpResponseBadRequest(error_message)

        avatar = request.FILES.get('avatar')
        if not avatar:
            error_message = "There is no file named `avatar` in form"
            return HttpResponseBadRequest(error_message)

        request.user.profile.avatar = avatar
        request.user.profile.save()
        return redirect('upload_avatar')

    return render(request, 'upload_avatar.html')


@login_required(login_url='/login/')
def create_category(request):
    if request.method == "POST":
        data = json.loads(request.body)
        category_name = data.get("name")
        help_text = data.get("helpText")

        if category_name:
            new_category = Category.objects.create(
                name=category_name, help_text=help_text)
            return JsonResponse({"status": "success", "category_id": new_category.pk})
    return JsonResponse({"status": "error"})


@login_required
def toggle_pinned_category(request, category_id):
    user = request.user
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)

    if user in category.pinned_by.all():
        category.pinned_by.remove(user)
        pinned = False
    else:
        category.pinned_by.add(user)
        pinned = True

    category.save()

    return JsonResponse({"pinned": pinned})


# for apis

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        """
        Optionally filters categories by 'name' query parameter.
        """
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Add the count of  prompts for each category
        for category in serializer.data:
            count = Prompt.objects.filter(
                category_id=category['id']).count()
            category['prompt_count'] = count

        return Response(serializer.data)


class PromptsListCreateView(generics.ListCreateAPIView):
    serializer_class = PromptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return prompts that belong to the current category and
        optionally filter by name if the 'name' query parameter is provided.
        """
        category_id = self.kwargs['category_id']
        queryset = Prompt.objects.filter(category_id=category_id)

        # 获取URL查询参数中的'name'参数
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset

    def perform_create(self, serializer):
        """
        set the category of the prompt before saving it.
        """
        print('perform_create', self.kwargs['category_id'], serializer.validated_data)
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, pk=category_id)
        serializer.save(category=category)


class LabelListCreateView(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, pk=category_id)
        serializer.save(category=category)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        return labels that belong to the current user.
        """
        category_id = self.kwargs['category_id']
        return Label.objects.filter(category_id=category_id)


class ModelListCreateView(generics.ListCreateAPIView):
    queryset = LLMModel.objects.all()
    serializer_class = LLMModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, pk=category_id)
        serializer.save(category=category)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        return labels that belong to the current user.
        """
        category_id = self.kwargs['category_id']
        return LLMModel.objects.filter(category_id=category_id)


class ApiRootView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            'Categories': drf_reverse('api-list-categories',
                                      request=request, format=kwargs.get('format')),
            'Prompts': drf_reverse('api-list-category-prompts', args=[1],
                                   request=request, format=kwargs.get('format')),
            'Labels': drf_reverse('api-list-category-labels', args=[1],
                                  request=request, format=kwargs.get('format')),
            'Models': drf_reverse('api-list-category-models', args=[1],
                                  request=request, format=kwargs.get('format')),
        })
