import requests
from jinja2 import Template, Environment, meta
from typing import List, Dict, Any, Optional
from . import errors


def find_jinja2_variables(template_str):
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
    return undeclared_variables


class HTTPClient:
    def __init__(self):
        self.session = requests.Session()

    def request(self, method: str, url: str, headers: Optional[Dict[str, str]] = None,
                params: Optional[Dict[str, str]] = None, data=None) -> Any:
        try:
            response = self.session.request(method, url, headers=headers, params=params, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise errors.ConnectionError
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise errors.NotFoundError
            elif e.response.status_code == 401:
                raise errors.UnauthorizedError
            else:
                raise errors.PromptsHubError(e)


class Prompt:
    def __init__(self, name: str, content: str, output_format: str, model: Optional[str] = None):
        self.name = name
        self.content = content
        self.output_format = output_format
        self.model = model


class PromptTemplate:
    def __init__(self, name: str, text: str, output_format: str,
                 models: List[Dict[str, Any]], labels: List[Dict[str, Any]]):
        self.name = name
        self.text = text
        self.output_format = output_format
        self.models = models
        self.labels = labels


class PromptHub:

    def __init__(self, url: str, token: str, category: str):
        self.base_url = url
        self.headers = {'Authorization': f'Token {token}'}
        self.http_client = HTTPClient()

        self.category_name = None
        self.set_category(category)

        # 最好是 3.5，其次是 4，如果这两个都没有，则使用任意一个 Prompt 所适用的 Model
        self.preferred_models = ['gpt-3.5', 'gpt-4', 'any']

    def set_category(self, category: str) -> None:
        resp = self.get_request("/api/categories/", {'name': category})
        if not resp:
            raise errors.CategoryNotFoundError
        self.category_name = category

    def set_preferred_models(self, preferred_models: List[str]) -> None:
        self.preferred_models = [model.lower() for model in preferred_models]

    def get_request(self, uri: str, params=None) -> Any:
        url = f"{self.base_url}{uri}"
        response = self.http_client.request('GET', url, headers=self.headers, params=params)
        return response

    def post_request(self, uri: str, data=None) -> Any:
        url = f"{self.base_url}{uri}"
        response = self.http_client.request('POST', url, headers=self.headers, data=data)
        return response

    def get(self, prompt_name: str, raise_if_missing_variables: bool = True, **variables) -> Prompt:

        uri = f"/api/categories/{self.category_name}/prompts/"
        prompts = self.get_request(uri, {'name': prompt_name})
        if not prompts:
            raise errors.PromptNotFoundError
        prompt_data = prompts[0]
        template = Template(prompt_data['text'])
        missing_variables = [var for var in find_jinja2_variables(prompt_data['text']) if var not in variables]
        if missing_variables and raise_if_missing_variables:
            raise errors.PromptMissingVariablesError(missing_variables)

        content = template.render(**variables)
        model_names = [model['name'] for model in prompt_data['models']]
        model = self._get_valid_model(model_names)
        return Prompt(prompt_name, content, prompt_data['output_format'], model)

    def _get_valid_model(self, valid_model_names: List[str]) -> Optional[str]:
        # 从 Prompt 所适用的 Model 列表中获取一个自己最想要的 Model
        # Prompt's available models: all, gpt-4 （如果有all，则说明任何一个都可以）
        # Preferred models: gpt-3.5, gpt-4, any（优先级从高到低，如果有any，则说明可以使用任意一个）
        if 'all' in valid_model_names:
            return self.preferred_models[0]
        for preferred_model in self.preferred_models:
            if preferred_model == 'any':
                return valid_model_names[0] if valid_model_names else None
            if preferred_model in valid_model_names:
                return preferred_model
        if 'any' not in self.preferred_models:
            raise errors.NoValidModelError(f"Preferred models {self.preferred_models} "
                                           f"not found in Prompt's available models {valid_model_names}")
        return None

    def get_template(self, prompt_name: str) -> PromptTemplate:
        uri = f"/api/categories/{self.category_name}/prompts/"
        prompts = self.get_request(uri, {'name': prompt_name})
        if not prompts:
            raise errors.PromptNotFoundError
        prompt_data = prompts[0]
        return PromptTemplate(**prompt_data)

    def create_template(self, name: str, text: str, output_format: str = "str",
                        model_names: List[str] = None, label_names: List[str] = None) -> PromptTemplate:
        uri = f"/api/categories/{self.category_name}/prompts/"
        resp = self.post_request(
            uri,
            data={'name': name,
                  'text': text,
                  'output_format': output_format,
                  'model_names': model_names,
                  'label_names': label_names,
                  }
        )
        return PromptTemplate(**resp)
