import os
import re
from time import sleep

from config import MD_FILES_PATH, SUMMARY_PROMPT
from database import create_table, save_article
from openai_api import get_openai_response
from utils import get_markdown_content


def compress_content(content):
    # 删除多余空行和空格
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    content = content.strip()
    return content


def process_md_files(directory, prompt):
    print("开始创建数据表...")
    create_table()

    print(f"开始处理目录: {directory}")
    for file, content in get_markdown_content(directory):
        print(f"\n正在处理文件: {file}")

        print("压缩文件内容...")
        compressed_content = compress_content(content)
        print(f"压缩前长度: {len(content)}, 压缩后长度: {len(compressed_content)}")

        print("发送到 OpenAI 进行分析...")
        full_prompt = f"{prompt}\n{compressed_content}"
        response = get_openai_response(full_prompt, file)

        if response:
            print("保存分析结果到数据库...")
            # print(f"Response :\n{response}\n")
            save_article(file, response)
            print(f"文件 {file} 处理完成")
        else:
            print(f"文件 {file} 处理失败")


if __name__ == '__main__':
    process_md_files(MD_FILES_PATH, SUMMARY_PROMPT)
