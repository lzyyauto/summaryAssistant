import json
import os

import openai

from config import OPENAI_API_KEY, OPENAI_BASE_URL

openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_BASE_URL


def get_openai_response(prompt, file):
    try:
        messages = [{"role": "user", "content": f"{prompt}"}]

        # print(f"message: {messages}")

        response = openai.chat.completions.create(
            model="qwen2.5-72b-instruct",
            messages=messages,
            stream=False,  # 改为非流式
            temperature=0,
            presence_penalty=0,
            frequency_penalty=0,
            top_p=1)

        try:
            # 从返回结构中提取JSON字符串
            content = response.choices[0].message.content
            # 清理markdown格式
            json_str = content.replace('```json\n', '').replace('\n```',
                                                                '').strip()

            # 解析并重新格式化JSON
            response_json = json.loads(json_str)
            return json.dumps(response_json, ensure_ascii=False)

        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return ""
        except Exception as e:
            print(f"处理响应时出错: {e}")
            return ""

    except Exception as e:
        print(f"调用 OpenAI API 时出错: {e}")
        return ""
