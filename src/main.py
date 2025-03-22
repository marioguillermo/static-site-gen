import os
import shutil

from markdown_blocks import markdown_to_html_node


def copy_static_to_public(source='static', destination='public'):
    # Step 1: Delete all contents of the destination directory
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Cleared destination directory: {destination}")

    # Step 2: Recreate the empty destination directory
    os.makedirs(destination, exist_ok=True)

    # Step 3: Recursive copy
    def recursive_copy(src, dest):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)

            if os.path.isdir(src_path):
                os.makedirs(dest_path, exist_ok=True)
                recursive_copy(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")

    # Start the recursive copy
    recursive_copy(source, destination)


def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):  # Make sure it's exactly one '#' followed by a space
            return line[2:].strip()  # Remove '# ' and strip the rest
    raise ValueError("No H1 header found in markdown.")


def clear_public_directory(path='public'):
    if os.path.exists(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print(f"Cleared all contents in '{path}'")
    else:
        print(f"Directory '{path}' does not exist.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Step 1: Read the markdown content
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Step 2: Read the template content
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Step 3: Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Step 4: Extract title
    title = extract_title(markdown_content)

    # Step 5: Fill in the template
    final_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    # Step 6: Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Step 7: Write the final HTML to the destination
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, _, files in os.walk(dir_path_content):
        for filename in files:
            if filename.endswith('.md'):
                from_path = os.path.join(root, filename)

                # Determine the relative path from the content root
                relative_path = os.path.relpath(from_path, dir_path_content)

                # Change .md to .html
                relative_html_path = os.path.splitext(relative_path)[0] + '.html'

                # Create full destination path
                dest_path = os.path.join(dest_dir_path, relative_html_path)

                # Generate the page
                generate_page(from_path, template_path, dest_path)

if __name__ == '__main__':
    clear_public_directory("public")
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")


