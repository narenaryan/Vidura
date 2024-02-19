from jinja2 import Environment
from jinja2 import meta

def find_used_variables(template_str):
    """
    分析Jinja2模板字符串，返回模板中使用的所有变量。

    :param template_str: Jinja2模板字符串
    :return: 模板中使用的变量集合
    """
    env = Environment()
    # 将模板字符串解析为AST
    parsed_content = env.parse(template_str)
    # 使用meta模块找到所有未声明的变量
    undeclared_variables = meta.find_undeclared_variables(parsed_content)
    print(type(undeclared_variables))
    return undeclared_variables

# 示例模板字符串
template_str = '''
Hello {{ name }}!
{% if age > 18 %}
You are an adult.
{% else %}
You are a minor.
{% endif %}
Your favorite color is {{ color }}.
'''

# 调用函数并打印结果
used_variables = find_used_variables(template_str)
print(used_variables)
