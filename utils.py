import os


def get_markdown_content(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                    yield file, content
