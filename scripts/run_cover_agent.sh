#!/bin/bash

test_file="$1"

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

relative_path=${test_file#"$project_root/tests/"}

dir_name=$(echo "$relative_path" | cut -d'/' -f1 | sed 's/_tests//')
file_name=$(basename "$relative_path" _test.py).py

source_file="$project_root/src/$dir_name/$file_name"

cover-agent \
  --source-file-path "$source_file" \
  --test-file-path "$test_file" \
  --code-coverage-report-path "$project_root/coverage.xml" \
  --test-command "pytest tests/" \
  --test-command-dir "$project_root" \
  --coverage-type "cobertura" \
  --desired-coverage 95 \
  --max-iterations 10
