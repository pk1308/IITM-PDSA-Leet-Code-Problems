#!/bin/bash

# Function to check if a directory exists
check_directory() {
    local folder_path="$1"
    if [ ! -d "$folder_path" ]; then
        echo "Error: Directory '$folder_path' does not exist."
        exit 1
    fi
}

# Function to convert notebook files to markdown
convert_to_markdown() {
    local folder_path="$1"
    local notebook_files=()
    while IFS= read -r -d '' file; do
        # Get the relative path excluding the base directory
        relative_path=$(realpath --relative-to="$folder_path" "$file" 2>/dev/null)
        # Check if realpath succeeded (exit code 0)
        if [ $? -eq 0 ]; then
            notebook_files+=("$relative_path")
        else
            echo "Error: realpath failed for '$file'."
        fi
    done < <(find "$folder_path" -type f -name "*.ipynb" -print0)

    # Check if any notebook files were found
    if [ ${#notebook_files[@]} -gt 0 ]; then
        echo "Found notebook files:"
        for file in "${notebook_files[@]}"; do
            echo "Converting '$file' to markdown..."
            if jupyter nbconvert --to markdown "$folder_path/$file"; then
                echo "Converted '$file' to markdown successfully."
            else
                echo "Failed to convert '$file' to markdown."
            fi
        done
    else
        echo "No notebook files found in '$folder_path'."
    fi
}

# Function to update documents and deploy
update_and_deploy() {
    local python_script="driver/update_mydocs.py"
    local mkdocs_command="mkdocs gh-deploy"

    echo "Running Python script to update documents..."
    if run python3 "$python_script"; then
        echo "Python script executed successfully."
        echo "Deploying updated documents with mkdocs..."
        if run $mkdocs_command; then
            echo "Deployment successful."
        else
            echo "Failed to deploy documents with mkdocs."
        fi
    else
        echo "Failed to execute Python script."
    fi
}

# Function to execute commands and handle errors
run() {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "Error: Command '$*' failed with status $status."
        exit $status
    fi
    return $status
}

# Main function
main() {
    local folder_path="./docs"
    check_directory "$folder_path"
    convert_to_markdown "$folder_path"
    update_and_deploy
}

# Entry point
main
