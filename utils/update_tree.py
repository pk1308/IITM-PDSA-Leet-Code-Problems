import os
import fnmatch

def load_gitignore(gitignore_path='.gitignore'):
    ignore_patterns = []
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as file:
            ignore_patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return ignore_patterns

def is_ignored(path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def generate_tree(directory, prefix="", ignore_patterns=[]):
    tree_lines = []
    contents = sorted(os.listdir(directory))
    contents = [item for item in contents if not is_ignored(os.path.join(directory, item), ignore_patterns)]
    contents = [item for item in contents if item not in ['.git', 'site' , ".github", ".trunk"]]  # Always ignore .git and site directories
    pointers = ['├── '] * (len(contents) - 1) + ['└── ']

    for pointer, name in zip(pointers, contents):
        path = os.path.join(directory, name)
        tree_lines.append(prefix + pointer + name)
        if os.path.isdir(path):
            extension = '│   ' if pointer == '├── ' else '    '
            tree_lines.extend(generate_tree(path, prefix + extension, ignore_patterns))

    return tree_lines

def update_readme_with_tree(directory, readme_path="README.md", gitignore_path=".gitignore"):
    ignore_patterns = load_gitignore(gitignore_path)
    tree_lines = generate_tree(directory, ignore_patterns=ignore_patterns)
    tree_string = "\n".join(tree_lines)

    with open(readme_path, 'w') as readme_file:
        readme_file.write("# Project Directory Tree\n\n")
        readme_file.write("```\n")
        readme_file.write(tree_string)
        readme_file.write("\n```\n")

if __name__ == "__main__":
    directory_to_map = '.'  # Change this to the directory you want to map
    update_readme_with_tree(directory_to_map)
