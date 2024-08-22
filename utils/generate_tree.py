import os


def load_gitignore(base_path):
    """
    Load the .gitignore file and return a list of ignored patterns.

    :param base_path: The base path where the .gitignore file is located.
    :return: A list of ignored patterns.
    """
    gitignore_path = os.path.join(base_path, ".gitignore")
    if not os.path.isfile(gitignore_path):
        return []

    with open(gitignore_path, "r") as f:
        lines = f.readlines()

    ignore_patterns = [
        line.strip() for line in lines if line.strip() and not line.startswith("#")
    ]
    return ignore_patterns


def is_ignored(path, ignore_patterns):
    """
    Check if a given path matches any of the ignore patterns.

    :param path: The path to check.
    :param ignore_patterns: A list of ignore patterns.
    :return: True if the path should be ignored, False otherwise.
    """
    from fnmatch import fnmatch

    for pattern in ignore_patterns:
        if fnmatch(path, pattern) or fnmatch(path, os.path.join("*", pattern)):
            return True
    return False


def generate_tree(base_path, prefix="", ignore_patterns=None):
    """
    Generate a tree representation of the folder structure.

    :param base_path: The base path of the folder structure.
    :param prefix: The prefix for the current level of the tree (used for recursion).
    :param ignore_patterns: A list of patterns to ignore.
    :return: A string representing the tree structure.
    """
    if ignore_patterns is None:
        ignore_patterns = []

    tree_str = ""
    # Get a sorted list of the directory contents
    contents = sorted(os.listdir(base_path))
    # Separate files and directories
    files = [f for f in contents if os.path.isfile(os.path.join(base_path, f))]
    dirs = [d for d in contents if os.path.isdir(os.path.join(base_path, d))]

    # Filter out ignored files and directories
    files = [
        f for f in files if not is_ignored(os.path.join(base_path, f), ignore_patterns)
    ]
    dirs = [
        d for d in dirs if not is_ignored(os.path.join(base_path, d), ignore_patterns)
    ]

    # Print the directories
    for directory in dirs:
        tree_str += f"{prefix}├── {directory}\n"
        # Recurse into subdirectories with an updated prefix
        tree_str += generate_tree(
            os.path.join(base_path, directory), prefix + "│   ", ignore_patterns
        )

    # Print the files
    for file in files:
        tree_str += f"{prefix}└── {file}\n"

    return tree_str


def write_tree_to_markdown(base_path, output_file):
    """
    Write the tree structure of the given base path to a markdown file.

    :param base_path: The base path of the folder structure.
    :param output_file: The path to the output markdown file.
    """
    ignore_patterns = load_gitignore(base_path)
    # Add .git to the ignore patterns
    ignore_patterns.append(".git")
    ignore_patterns.append("site")
    ignore_patterns.append(".trunk")
    

    tree_str = generate_tree(base_path, ignore_patterns=ignore_patterns)
    with open(output_file, "w") as f:
        f.write("# Folder Structure\n\n")
        f.write("```\n")
        f.write(tree_str)
        f.write("```\n")


if __name__ == "__main__":

    # Example usage
    base_path = os.getcwd()
    output_file = "README.md"
    write_tree_to_markdown(base_path, output_file)
