from django.shortcuts import render
from .models import Category, Prompt, PromptLabel
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def list_categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'list_categories.html', context)

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
