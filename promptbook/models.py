from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Prompt(models.Model):
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50] + '...' if len(self.text) > 50 else self.text

class Label(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PromptLabel(models.Model):
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)
    prompt = models.ForeignKey(Prompt, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"Label: {self.label.__str__()}, Prompt: {self.prompt.__str__()}" 
