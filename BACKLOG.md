# Backlog

- Category和Prompt 都需要有一个code和name, P0
- prompt 需要支持 {}  {{}} 两种变量格式, P1
- 有的 text 不是完整的 prompt，只是其中一部分（model和outputformat无意义） partial_prompt
  - 将 template 和 prompt 分开？ P1
- 如果是JSON，则必须是gpt-3.5-turbo-0125,gpt-4-0125-preview,gpt-4-1106-preview
  - https://platform.openai.com/docs/guides/text-generation/json-mode , P0
- 搜索出来的结果，的样式跟list页面的样式复用，且可以直接打开编辑,P2
- 支持 copy Category（用于测试）,P0
- 支持查看 prompt的最后使用时间,P0
- 支持同一个prompt，对于不同的model，可以有不同的content，且有多版本，P1
- 可以查看prompt的历史版本，P0
- 可以查看prompt的调用历史，包含调用时间，调用model，调用结果，P0
- 可以根据prompt的调用历史，去测试不同的model，P0