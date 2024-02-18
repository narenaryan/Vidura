# 修改表结构的方法 Modify table structure

1. modify `promptbook/models.py`
2. run `python manage.py makemigrations`, this step will generate a migration file in `promptbook/migrations` directory
3. run `python manage.py migrate`, this step will apply the migration file to the database


# 多语言翻译 i18n translation
1. 在HTML文件中添加翻译标识 add translation tag in html file
   ```
   {% load i18 %}
   e.g. {% trans "Editor" %}
   e.g. {% blocktrans %}Editor{% endblocktrans %}
   ```
2. 生成翻译文件 make messages files
   ```
   # `prompt-hub`目录下
   python manage.py makemessages -l en --ignore venv 
   python manage.py makemessages -l zh_Hans --ignore venv 
   ```
3. 编译翻译文件 compile messages
   ```
   # `prompt-hub`目录下
   python manage.py compilemessages --ignore venv 
   ```     

语言选择器已经在`base.html`中添加，可以在`base.html`中修改语言选择器的样式。
Language selector has been added in `base.html`, you can modify the style of language selector in `base.html`.

