

# 开发者指北

这些步骤和说明旨在提供必要的操作指南，以便开发者能够轻松地熟悉该项目。

## 如何运行 PromptHub？

使用 Python 3.9 或更高版本在您的机器上运行此软件，并在您的 Python 环境中安装开发者依赖项，如下所示：

1. 安装 Python 依赖项
    >pip install -r requirements.txt
   
2. 初始化数据库表结构
   >python manage.py migrate
   
3. 创建超级用户（用于登录和管理） 

    运行以下命令创建超级用户：
    >python manage.py createsuperuser

4. 本地运行
   >python manage.py runserver
   
访问地址 http://127.0.0.1:8000 并输入之前创建的密码以进入 PromptHub 。


## 修改表结构

为了在数据库中修改表结构，您需要按照以下步骤操作：

1. **修改模型文件**：首先，在 `promptbook/models.py` 文件中进行必要的修改。
2. **生成迁移文件**：使用命令`python manage.py makemigrations`在 `promptbook/migrations` 目录下生成一个迁移文件
3. **应用迁移至数据库**：通过运行命令 `python manage.py migrate`，将迁移文件应用到数据库中。


## 多语言翻译 (i18n)

1. **添加翻译标记**：在HTML文件中加入翻译标记，如下所示：
   ```
   {% load i18 %}
   e.g. {% trans "Editor" %}
   e.g. {% blocktrans %}Editor{% endblocktrans %}
   ```
2. **生成翻译文件**：在 prompt-hub 目录下，执行以下命令生成翻译文件：
   ```
   # `prompt-hub`目录下
   python manage.py makemessages -l en --ignore venv 
   python manage.py makemessages -l zh_Hans --ignore venv 
   ```
3. **编译翻译文件**：最后，编译生成的翻译文件：
   ```
   # `prompt-hub`目录下
   python manage.py compilemessages --ignore venv 
   ```     

## API 支持Token认证

### 1. 生成 Token
    
您需要为每个用户生成一个独特的认证令牌。这可以通过以下几种方式完成：

- 管理命令
- Django管理后台
- 编写自定义视图或命令

Django REST Framework 提供了一个简便的管理命令来生成令牌：

> python manage.py drf_create_token <username>

### 2. 使用Token 

客户端在发送请求时，需要在请求头中包含令牌，以进行身份验证。格式如下：

> Authorization: Token <your_token_here>


