import json

from .models import Category, Prompt, PromptLabel, Label
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from actstream import action
from actstream.models import Action

@login_required(login_url='/login/')
def list_categories(request):
    categories = Category.objects.all()
    category_colors = ['pastel-green', 'pastel-blue', 'pastel-yellow', 'pastel-pink']
    categories_with_colors = [(category, category_colors[i % len(category_colors)]) for i, category in enumerate(categories)]
    return render(request, 'list_categories.html', {'categories_with_colors': categories_with_colors})

@login_required(login_url='/login/')
def list_prompts(request, category_id):
    category = Category.objects.get(pk=category_id)
    # Show prompts that are either public or belong to the current user
    prompts = category.prompt_set.filter(Q(is_public=True) | Q(owner=request.user)).order_by('-created_at')

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
        prompt_text = request.POST['prompt_text']
        category_id = request.POST['category']
        selected_labels = request.POST.getlist('labels')

        category = Category.objects.get(id=category_id)
        prompt = Prompt(text=prompt_text, category=category, owner=request.user)
        prompt.save()
        action.send(request.user, verb='created', target=prompt)

        for label_id in selected_labels:
            label = Label.objects.get(id=label_id)
            prompt_label = PromptLabel(prompt=prompt, label=label)
            prompt_label.save()

        return HttpResponseRedirect(reverse('list_prompts', args=[category_id]))

    return render(request, 'editor.html', {'categories': categories, 'labels': labels})

# def login(request):
#     if request.user.is_authenticated:
#         return redirect('list_categories')

#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             auth_login(request, form.get_user())
#             return redirect('list_categories')
#     else:
#         form = AuthenticationForm(request)
#     return render(request, 'login.html', {'form': form})

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
        return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return redirect('login')

@csrf_exempt
@login_required(login_url='/login/')
def edit_prompt(request, prompt_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = Prompt.objects.get(pk=prompt_id)
            prompt.text = data.get('text', prompt.text)
            prompt.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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
    actions = Action.objects.all()
    return render(request, 'activity_stream.html', {'actions': actions})

@login_required(login_url='/login/')
def upload_avatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        if avatar:
            request.user.profile.avatar = avatar
            request.user.profile.save()
        return redirect('upload_avatar')

    return render(request, 'upload_avatar.html')

@login_required(login_url='/login/')
def create_category(request):
    if request.method == "POST":
        data = json.loads(request.body)
        category_name = data.get("name")
        if category_name:
            new_category = Category.objects.create(name=category_name)
            return JsonResponse({"status": "success", "category_id": new_category.pk})
    return JsonResponse({"status": "error"})