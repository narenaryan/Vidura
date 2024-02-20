

<p align="center">
    <img src="https://prompt-hub.oss-cn-shanghai.aliyuncs.com/prompt-hub-logo11.png" width="200px"/>
</p>

# PromptHub: Your AI Prompt Management Tool

[中文文档](README_CN.md) 

## Introduction

In the world of AI application development, prompts are not just the bridge between human language and machine intelligence, but an indispensable component of modern intelligent applications. PromptHub is designed to provide developers with a simple, lightweight, and easily integrated management system to effectively manage, optimize, and expand your prompt applications, just like GitHub in the prompt domain.

## Features
- **User-Friendly API/SDK**: With a visual UI and straightforward API/SDK, PromptHub offers developers a seamless integration experience.
- **Decoupling Code and Prompts**: Focused on separating prompts from code logic, providing stable infrastructure support for production environments.
- **Support for Multiple Models**: Allows specifying the applicable AI models (e.g., GPT-4, GPT-3.5) to optimize costs according to needs.
- **Flexible Output Formats**: Supports customizing the output format of prompts (JSON or String) to meet the requirements of different scenarios.
- **One-Stop Management**: Centralize the management of prompts across multiple projects, improving efficiency.
- **Version Control**: Supports saving versions of prompts, convenient for A/B testing and quick rollbacks (planned).
- **Performance Optimization**: Utilizes models like GPT-4 to optimize the format and content of prompts, increasing accuracy while reducing token usage to save costs (planned). 
- **Multi-User Support**: Supports multi-user mode, allowing permission management based on projects (planned).
- **Integration with LLM**: Integration with large models such as GPT-4, Wenxin Yanyi, etc., to test the effect of prompts directly in PromptHub (planned).


# Screenshots



## Categories view
<table><tr><td><img src="./screens/categories.png" alt="Categories"/></td></tr></table>

We simplified categories for you. You can request new categories and we will add it for you.

## Prompts view
<table><tr><td><img src="./screens/prompts.png" alt="Prompts"/></td></tr></table>

Each prompt will have a list of labels attached like "gpt-3", "simple", or "complex". User can click on a label on any prompt and visit all the prompts tagged with the given label name. 

## Edit Prompt view
<table><tr><td><img src="./screens/edit_prompt.png" alt="Editor"/></td></tr></table>


## Universal search
One can search matching categories and prompts in one place by using search bar.
<table><tr><td><img src="./screens/search.png" alt="Search"/></td></tr></table>

## API

```json
{
    "Categories": "http://127.0.0.1:8000/api/categories/",
    "Prompts": "http://127.0.0.1:8000/api/categories/1/prompts/",
    "Labels": "http://127.0.0.1:8000/api/categories/1/labels/",
    "Models": "http://127.0.0.1:8000/api/categories/1/models/"
}
```

<table><tr><td><img src="./screens/api.png" alt="API"/></td></tr></table>


# QuickStart

## Client Usage

Install the package using pip（1.6KB）:

```shell    
pip install prompthub
```

```python
from prompthub import PromptHub
prompts = PromptHub('http://localhost:8000', 'your_token', category='rmb-prod')
prompt = prompts.get('your_prompt_name')
```

For more details, please refer to [Client Usage](client%2FREADME.md)


## Server Deployment

```bash
docker run -d -p 8000:8000 datamini/prompt-hub
```

Note:
1. Open http://127.0.0.1:8000/ in your browser. Default username and password: `admin/admin`
2. Use a local SQLite database

# Advanced Usage

## Docker Image

https://hub.docker.com/r/datamini/prompt-hub


## Use Docker Compose to deploy

```shell
version: '3.8'
services:
  prompt-hub:
    image: datamini/prompt-hub
    ports:
      - "8000:8000"
    environment:
      SUPERUSER_NAME: admin
      SUPERUSER_PASSWORD: admin
      SUPERUSER_EMAIL: x@x.x
      TIME_ZONE: Asia/Shanghai  
      DB_TYPE: mysql # mysql or postgresql or sqlite
      DB_HOST: 127.0.0.1
      DB_NAME: db01
      DB_USER: admin
      DB_PASS: admin
```

# For Developers

Please refer to [Developer Documentation](README4DEV.md)


## Acknowledgements
PromptHub is developed based on Vidura, and we express our deep gratitude to the Vidura team. PromptHub promises to be completely open source, as a way to give back to the community.

## Join Us

Whether you are a developer looking to improve work efficiency or a tech enthusiast interested in AI prompt management systems, PromptHub welcomes you.  lele@datamini.ai (i am from HangZhou, China)

