#!/bin/bash

# Check for required argument
if [ -z "$1" ]; then
  echo "Usage: $0 <search_directory>"
  exit 1
fi

# Set the directory to search from first argument
SEARCH_DIR="$1"

# Parent of SEARCH_DIR (i.e., Core-Model-v8-LINUX)
SEARCH_DIR_PARENT=$(dirname "$SEARCH_DIR")

# Find all .csproj files in the directory (recursively)
find "$SEARCH_DIR" -type f -name "*.csproj" | while read -r csproj_file; do
  echo "Updating OutputPaths in $csproj_file ..."

  # Compute the output path relative to this specific .csproj's directory so that
  # libraries/extensions whose .csproj lives in a src/ subdirectory get the right
  # number of ".." components regardless of their directory structure.
  csproj_dir=$(dirname "$csproj_file")
  rel_up=$(realpath --relative-to="$csproj_dir" "$SEARCH_DIR_PARENT")
  NEW_BASE_PATH="${rel_up//\//\\}\\build\\extensions"

  # Check if OutputPath exists in an unconditional PropertyGroup.
  # A conditional OutputPath (e.g. Debug-only) is ignored here because it won't
  # apply for Release builds, so we treat it as missing and insert an unconditional one.
  if ! xmlstarlet sel -t -v "//PropertyGroup[not(@Condition)]/OutputPath" "$csproj_file" 2>/dev/null | grep -q .; then
    echo " - OutputPath missing or only in conditional PropertyGroup(s); inserting $NEW_BASE_PATH"
    xmlstarlet ed -L \
      -s "//PropertyGroup[not(@Condition)][1]" \
      -t elem -n "OutputPath" -v "$NEW_BASE_PATH" \
      "$csproj_file"
    continue
  fi

  # Extract all current OutputPath values from unconditional PropertyGroups
  mapfile -t output_paths < <(xmlstarlet sel -t -v "//PropertyGroup[not(@Condition)]/OutputPath" -n "$csproj_file")

  for old_path in "${output_paths[@]}"; do
    # Construct new OutputPath value
    new_path="$NEW_BASE_PATH"

    echo " - Replacing: $old_path -> $new_path"

    # Update the OutputPath in the XML
    xmlstarlet ed -L \
      -u "//OutputPath[text()='$old_path']" \
      -v "$new_path" \
      "$csproj_file"
  done
done
