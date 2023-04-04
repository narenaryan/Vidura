import json

from .models import Category, Prompt, PromptLabel, Label
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from actstream import action
from actstream.models import Action

@login_required
def list_categories(request):
    categories = Category.objects.all()
    category_colors = ['pastel-green', 'pastel-blue', 'pastel-yellow', 'pastel-pink']
    categories_with_colors = [(category, category_colors[i % len(category_colors)]) for i, category in enumerate(categories)]
    return render(request, 'list_categories.html', {'categories_with_colors': categories_with_colors})

@login_required
def list_prompts(request, category_id):
    category = Category.objects.get(pk=category_id)
    prompts = category.prompt_set.all()

    prompt_labels = {}
    for prompt in prompts:
        labels = [pl.label for pl in PromptLabel.objects.filter(prompt=prompt)]
        prompt_labels[prompt.id] = labels

    return render(request, 'list_prompts.html', {
        'category': category,
        'prompts': prompts,
        'prompt_labels': prompt_labels.items(),
    })

@login_required
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
        prompt = Prompt(text=prompt_text, category=category)
        prompt.save()
        action.send(request.user, verb='created', target=prompt)

        for label_id in selected_labels:
            label = Label.objects.get(id=label_id)
            prompt_label = PromptLabel(prompt=prompt, label=label)
            prompt_label.save()

        return HttpResponseRedirect(reverse('list_prompts', args=[category_id]))

    return render(request, 'editor.html', {'categories': categories, 'labels': labels})

def login(request):
    if request.user.is_authenticated:
        return redirect('list_categories')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('list_categories')
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

@csrf_exempt
@login_required
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

@login_required
def activity_stream(request):
    actions = Action.objects.all()
    return render(request, 'activity_stream.html', {'actions': actions})