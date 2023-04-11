import json

from enum import Enum

from django.db import IntegrityError
from django.db.models import Count
from .models import Category, Prompt, PromptLabel, Label
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Count, Max
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Cast
from django.db.models import Case, When, Value, CharField, IntegerField

from actstream import action
from actstream.models import Action
from rest_framework import viewsets, permissions
from promptbook.serializers import CategorySerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
import textstat

class PrompVisibility(Enum):
    yes = 'yes'
    no = 'no'

# Calculates the easiness using flesch reading score
easiness_sql_case = Case(
    When(flesch_reading_score__gte=90, then=Value("perfect")),
    When(flesch_reading_score__gte=80, then=Value("highly readable")),
    When(flesch_reading_score__gte=70, then=Value("readable")),
    When(flesch_reading_score__gte=60, then=Value("standard")),
    When(flesch_reading_score__gte=50, then=Value("poor")),
    When(flesch_reading_score__gte=30, then=Value("confusing")),
    default=Value("very confusing"),
    output_field=CharField(),
)


@login_required(login_url='/login/')
def list_categories(request):
    user = request.user
    # Only get categories of user
    categories = Category.objects.all().annotate(
        num_prompts=Count('prompt', filter=Q(prompt__owner=user) | Q(prompt__is_public=True)),
        last_updated=Max('prompt__modified_at', filter=Q(prompt__owner=user))
    )

    # Get two most recent prompts for each category
    for category in categories:
        category.recent_prompts = category.prompt_set.filter(owner=user).order_by('-modified_at')[:2]

    context = {'categories': categories}
    return render(request, 'list_categories.html', context)

@login_required(login_url='/login/')
def list_prompts(request, category_id):
    category = Category.objects.get(pk=category_id)
    # Show prompts that are either public or belong to the current user
    prompts = category.prompt_set.filter(Q(is_public=True) | Q(owner=request.user)).annotate(
        easiness=easiness_sql_case
    ).order_by('-created_at')
    prompt_labels = {}

    for prompt in prompts:
        labels = [pl.label for pl in PromptLabel.objects.filter(prompt=prompt)]
        prompt_labels[prompt.id] = labels

    return render(request, 'list_prompts.html', {
        'category': category,
        'prompts': prompts,
        'prompt_labels': prompt_labels.items(),
    })

@login_required(login_url='/login/')
def list_prompts_by_label(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    prompt_labels = PromptLabel.objects.filter(label=label)
    prompts = [pl.prompt for pl in prompt_labels]

    return render(request, 'list_prompts_by_label.html', {'label': label, 'prompts': prompts})

@login_required
def editor(request):
    categories = Category.objects.all()
    labels = Label.objects.all()

    if request.method == 'POST':
        is_public = False
        prompt_text = request.POST['prompt_text']
        category_id = request.POST['category']
        selected_labels = request.POST.getlist('labels')
        is_public_prompt_option = request.POST.get('is-public-prompt')

        if is_public_prompt_option and is_public_prompt_option.lower() == PrompVisibility.yes.value:
            is_public = True

        category = Category.objects.get(id=category_id)
        reading_score = textstat.flesch_reading_ease(prompt_text)
        prompt = Prompt(text=prompt_text, category=category, owner=request.user, is_public=is_public, flesch_reading_score=reading_score)
        # prompt.save()

        try:
            prompt.save()
        except IntegrityError as e:
            # load the same page with an error message
            return render(request, 'editor.html', {
                'categories': categories,
                'labels': labels,
                'selected_category': category_id,
                'error_message': 'A prompt with this text already exists. Please enter a different prompt.'
            })

        action.send(request.user, verb='created', target=prompt)

        for label_id in selected_labels:
            label = Label.objects.get(id=label_id)
            prompt_label = PromptLabel(prompt=prompt, label=label)
            prompt_label.save()

        return HttpResponseRedirect(reverse('list_prompts', args=[category_id]))
    category_id = request.GET.get("category_id")

    if category_id:
        category_id = int(category_id)

    return render(request, 'editor.html', {
        'categories': categories,
        'labels': labels,
        'selected_category': category_id
    })

@login_required(login_url='/login/')
def edit_prompt(request, prompt_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = Prompt.objects.get(pk=prompt_id)
            prompt.text = data.get('text', prompt.text)
            prompt.flesch_reading_score = textstat.flesch_reading_ease(prompt.text)

            try:
                prompt.save()
            except IntegrityError as e:
                error_message = 'A prompt with this text already exists. Please enter a different prompt.'
                return HttpResponseBadRequest(error_message)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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
    prompt = get_object_or_404(Prompt, id=prompt_id)
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
def activity_stream(request):
    # This version properly type casts SQL queries to SQLite, PostgreSQL databases
    public_prompts = Prompt.objects.filter(is_public=True)
    actions = Action.objects.annotate(
        target_object_id_as_integer=Cast('target_object_id', IntegerField())
    ).filter(
        Q(target_object_id_as_integer__in=public_prompts.values_list('id', flat=True), target_content_type=ContentType.objects.get_for_model(Prompt)),
        Q(verb="created") | Q(verb="made public")
    )

    return render(request, 'activity_stream.html', {'actions': actions})

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
            new_category = Category.objects.create(name=category_name, help_text=help_text)
            return JsonResponse({"status": "success", "category_id": new_category.pk})
    return JsonResponse({"status": "error"})


@login_required
def toggle_prompt_public(request, prompt_id):
    if request.method == 'POST':
        try:
            prompt = Prompt.objects.get(id=prompt_id, owner=request.user)
            prompt.is_public = not prompt.is_public
            prompt.save()

            if prompt.is_public:
                action.send(request.user, verb='made public', target=prompt)

            return JsonResponse({'success': True, 'is_public': prompt.is_public})
        except Prompt.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Prompt not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


# for apis

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Add the count of public prompts for each category
        for category in serializer.data:
            count = Prompt.objects.filter(category_id=category['id'], is_public=True).count()
            category['public_prompt_count'] = count

        return Response(serializer.data)