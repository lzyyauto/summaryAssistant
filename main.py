import os
import re
from time import sleep

from config import MD_FILES_PATH, SUMMARY_PROMPT
from database import create_table, is_article_processed, save_article
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
    success_count = 0
    skip_count = 0
    error_count = 0

    for file, content in get_markdown_content(directory):
        try:
            print(f"\n正在处理文件: {file}")

            # 检查是否已处理
            if is_article_processed(file):
                print(f"文件 {file} 已处理过，跳过")
                skip_count += 1
                continue

            print("压缩文件内容...")
            compressed_content = compress_content(content)
            print(f"压缩前长度: {len(content)}, 压缩后长度: {len(compressed_content)}")

            print("发送到 OpenAI 进行分析...")
            full_prompt = f"{prompt}\n{compressed_content}"
            response = get_openai_response(full_prompt, file)

            if response:
                print("保存分析结果到数据库...")
                if save_article(file, response):
                    print(f"文件 {file} 处理完成")
                    success_count += 1
                else:
                    print(f"文件 {file} 保存失败")
                    error_count += 1
            else:
                print(f"文件 {file} 处理失败")
                error_count += 1

        except Exception as e:
            print(f"处理文件 {file} 时发生错误: {e}")
            error_count += 1
            continue

    print(f"\n处理完成！成功: {success_count}, 跳过: {skip_count}, 失败: {error_count}")


if __name__ == '__main__':
    process_md_files(MD_FILES_PATH, SUMMARY_PROMPT)
