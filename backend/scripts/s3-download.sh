#!/bin/bash

# Check if the base path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <base_path>"
    exit 1
fi

# Use the first argument as the base path
base_path="$1"

# Define the list of file suffixes
file_suffixes=(
    "-files.yml"
    "-original.wav"
    "-transcription_original.json"
    "-transcription_original.pdf"
    "-transcription_original.srt"
    "-translation_original_english.json"
    "-translation_original_english.pdf"
    "-translation_original_english.srt"
    ".json"
    ".mp4"
)

# Iterate through each suffix and construct the full path
for suffix in "${file_suffixes[@]}"; do
    file="${base_path}/${base_path}${suffix}"
    local_filename=$(basename "$file")
    echo "Downloading $file to $local_filename..."
    python src/debates.py s3-admin --prod --download "$file" --file "$local_filename"
    if [ $? -ne 0 ]; then
        echo "Failed to download $file"
        exit 1
    fi
done

echo "All files downloaded successfully."