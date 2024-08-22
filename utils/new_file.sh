#!/bin/bash

echo [$(date)]: "START"
echo "Creating base file..."

echo "Enter week number: "
read weekno

# Ensure weekno is not empty and is a number
if [[ -z $weekno || ! $weekno =~ ^[0-9]+$ ]]; then
	echo "Invalid week number! Exiting."
	exit 1
fi

# Create the week directory with a space before the week number if it doesn't exist
week_dir="docs/Week ${weekno}"
if [ -d "$week_dir" ]; then
	echo "Directory $week_dir already exists. Skipping directory creation."
else
	mkdir -p "$week_dir"
	echo "Directory $week_dir created."
fi

# Define the target file path
target_file="$week_dir/week${weekno}.md"

# Copy and rename the base checklist file if the target file does not exist
if [ -f "$target_file" ]; then
	echo "File $target_file already exists. Skipping file copy and rename."
else
	if cp driver/base_checklist.md "$week_dir/base_checklist.md"; then
		echo "File copied successfully."
	else
		echo "Error copying file!"
		exit 1 # Exit script with error code 1
	fi

	if mv "$week_dir/base_checklist.md" "$target_file"; then
		echo "File renamed successfully."
	else
		echo "Error renaming file!"
		exit 1 # Exit script with error code 1
	fi
fi

echo [$(date)]: "END"
