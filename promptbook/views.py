import json

from django.shortcuts import render
from .models import Category, Prompt, PromptLabel, Label
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def list_categories(request):
    categories = Category.objects.all()
    category_colors = ['pastel-green', 'pastel-blue', 'pastel-yellow', 'pastel-pink']
    categories_with_colors = [(category, category_colors[i % len(category_colors)]) for i, category in enumerate(categories)]
    return render(request, 'list_categories.html', {'categories_with_colors': categories_with_colors})


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

def list_prompts_by_label(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    prompt_labels = PromptLabel.objects.filter(label=label)
    prompts = [pl.prompt for pl in prompt_labels]

    return render(request, 'list_prompts_by_label.html', {'label': label, 'prompts': prompts})
