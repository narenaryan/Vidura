
```python

from client.prompthub import PromptHub, errors

try:
    prompts = PromptHub('http://localhost:8000', '25cee15690db575d123271ef7f408e6a1f9446b1', category='rmb-prod')
except errors.CategoryNotFoundError:
    print('Category not found')
    # do something
except errors.ConnectionError:
    print('Connection error')
    # do something

# 按照这个顺序来找可以适用的模型
prompts.set_preferred_models(['gpt-3.5', 'gpt-4-turbo', 'any'])

try:
    prompt = prompts.get(
        'MetaName',
        raise_if_missing_variables=True,
        k1='v1',
        k2='v2',
    )
    content = prompt.content
    model = prompt.model
    
except errors.PromptNotFoundError:
    print('Prompt not found')
    # do something
except errors.PromptMissingVariablesError as e:
    print('Prompt missing variables', e)
    # do something
except errors.NoValidModelError:
    print('No valid model')
    # do something

    
template = prompts.get_template('MetaName')
# 该Prompt适用的模型有哪些
valid_models = template.models


prompt = prompts.create(
    'MetaName',
    'text',
    models=['gpt-3.5', 'gpt-4-turbo'],
    labels = ['label1', 'label2'],
)


```
