import os
import shutil
from block_markdown import *

def copy_static(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        return
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    def recursion(source_dir, dest_dir):
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        directories = os.listdir(source_dir)
        for file in directories:
            full_path = os.path.join(source_dir, file)
            print(f"copying {full_path} -> {dest_dir}")
            if os.path.isfile(full_path):
                shutil.copy(full_path, dest_dir)
            else:
                subdir = os.path.join(dest_dir, file)
                recursion(full_path, subdir)
    recursion(source_dir, dest_dir)
    
def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("#"):
            counter = 0
            for c in line:
                if c == "#":
                    counter += 1
            if counter == 1:
                return line.replace("#", "").strip()
    raise Exception("There is no h1 header")
            
    
def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open (from_path, 'r') as file:
        from_content = file.read()
    with open (template_path, 'r') as file:
        template_content = file.read()
    title = extract_title(from_content)
    HTML_string = markdown_to_html_node(from_content).to_html()
    new_content = "".join(template_content.replace("{{ Title }}", f'{title}').replace("{{ Content }}", f'{HTML_string}'))
    with open(dest_path, 'w') as file:
        file.write(new_content)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    def recursion(dir_path_content, template_path, dest_dir_path):
        if not os.path.exists(dest_dir_path):
            os.mkdir(dest_dir_path)
        directories = os.listdir(dir_path_content)
        for file in directories:
            full_path = os.path.join(dir_path_content, file)
            if os.path.isfile(full_path):
                if file.endswith('.md'):
                    dest_path = file.replace('.md', '.html')
                    full_dest_path = os.path.join(dest_dir_path, dest_path)
                    generate_page(full_path, template_path, full_dest_path)
                else:
                    subdir = os.path.join(dest_dir_path, file)
                    recursion(full_path, template_path, subdir)
            else:
                subdir = os.path.join(dest_dir_path, file)
                recursion(full_path, template_path, subdir)
    recursion(dir_path_content, template_path, dest_dir_path)
                
                
def main():
    shutil.rmtree("./public")
    copy_static("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")
main()
