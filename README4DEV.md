# Developer's Guide

These steps and instructions are intended to provide the necessary guidance for developers to become familiar with the project easily.

## How to run PromptHub ?

You can run this software by installing Python 3.9 or above on your machine, and install developer dependencies on your Python environment like:

1. Install Python Requirements

    > pip install -r requirements.txt
   
2. Run db migrations
    > python manage.py migrate
   
3. Create a super user
    > python manage.py createsuperuser

4. Run the server locally
    > python manage.py runserver
   
Access server at http://127.0.0.1:8000 and enter the credentials created before to launch PromptHub dashboard.



## Modifying Table Structure
To modify the table structure in the database, you need to follow these steps:

- **Modify Model File**: First, make the necessary changes in the `promptbook/models.py` file.
- **Generate Migration File**: Use the command `python manage.py makemigrations`, which will generate a migration file in the `promptbook/migrations` directory.
- **Apply Migration to Database**: Run the command `python manage.py migrate` to apply the migration file to the database.



## i18n Translation

1. **Add Translation Tags**: Add translation tags in the HTML file as shown below:
   ```
   {% load i18 %}
   e.g. {% trans "Editor" %}
   e.g. {% blocktrans %}Editor{% endblocktrans %}
   ```
2. **Generate Translation Files**: In the prompt-hub directory, execute the following commands to generate translation files:
   ```
   # `prompt-hub`目录下
   python manage.py makemessages -l en --ignore venv 
   python manage.py makemessages -l zh_Hans --ignore venv 
   ```
3. **Compile Translation Files**: Finally, compile the generated translation files:
   ```
   # `prompt-hub`目录下
   python manage.py compilemessages --ignore venv 
   ```     


## API Token Authentication

1. **Create Token**

    You need to generate a unique authentication token for each user. This can be accomplished in several ways:

   * Management command
   * Django admin
   * Writing custom views or commands
   
   Django REST Framework provides a convenient management command to generate tokens:

    >python manage.py drf_create_token <username>

2. **Use Token**

   When sending requests, clients need to include the token in the request header for authentication. The format is as follows:

    >Authorization: Token <your_token_here>

