[![Django CI](https://github.com/narenaryan/Vidura/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/narenaryan/Vidura/actions/workflows/django.yml)

<p align="center">
    <img src="https://raw.githubusercontent.com/narenaryan/Vidura/main/vidura-logo.png" width="500px"/>
</p>

Are you a ChatGPT prompt engineer?. Welcome to your all-in-one ChatGPT prompt management system. If you are saving emerging prompts on text editors, git, and on xyz, now goes the pain to add, tag, search and retrieve.

Prompts are nothing but thoughts out of our mind like communication. But, complex thougts easily eascape our memory. Moreover, connecting thoughts is harder. Vidura solves that problem for prompt engineers by streamlining their thoughts/prompts. 


This is a basic version for personal use, but if you want to preview more exciting features, like:

1. Rate your prompts by quality (prompt efficiency score)
2. API to import and export categories and prompts
3. Support for managing multiple types of prompts (ChatGPT, Stable Diffusion, Custom prompts)
4. Be part of a global prompt-engineering community,

visit: https://vidura.ai

Signup for free with your google account and start prompting in seconds. 😉

# Screenshots
## Categories view
<table><tr><td><img src="./screens/categories.png" alt="Categories"/></td></tr></table>

We simplified categories for you. You can request new categories and we will add it for you.

## Prompts view
<table><tr><td><img src="./screens/prompts.png" alt="Prompts"/></td></tr></table>

Each prompt will have a list of labels attached like "gpt-3", "simple", or "complex". User can click on a label on any prompt and visit all the prompts tagged with the given label name. 

## Edit Prompt view
<table><tr><td><img src="./screens/edit_prompt.png" alt="Editor"/></td></tr></table>

## Create new prompt using editor
<table><tr><td><img src="./screens/create_prompt.png" alt="Create Prompt"/></td></tr></table>

## Universal search
One can search matching categories and prompts in one place by using search bar.
<table><tr><td><img src="./screens/search.png" alt="Search"/></td></tr></table>

## Copy to Clipboard & Open ChatGPT from Vidura
Click the "Copy to clipboard" button and click the Chat GPT logo to open a new ChatGPT window. Hit Ctrl or Cmd(Mac OS) + v to paste your prompt into ChatGPT.

## Checkout cool prompts shared by community
To checkout all cool prompts shared by other users, head to homepage by clicking "Vidura" logo. By default, when a user creates a public prompt, it is shared to all others as a "community" labelled prompt in respective category.
<table><tr><td><img src="./screens/actstream.png" alt="Search"/></td></tr></table>

## How to run Vidura ?
You can run this software by installing Python 3.9 or above on your machine, and install developer dependencies on your Python environment like:

```bash
pip install -r requirements.txt
```

## Run db migrations
```bash
python manage.py migrate
```

## Create a super user
```bash
python manage.py createsuperuser
```
and enter required credentials to use for basic auth.

## Load fixture data
To load default categories and labels into System, run below command:

```bash
python manage.py loaddata promptbook/fixtures/init_data.yaml
```

## Run the server locally
```bash
python manage.py runserver
```

Access server at http://127.0.0.1:8000 and enter the credentials created before to launch Vidura dashboard.

**Note**: Vidura is a court minister and advisor from ancient Indian epic "Mahabharata". https://en.wikipedia.org/wiki/Vidura
