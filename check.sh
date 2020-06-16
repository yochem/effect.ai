#!/usr/bin/env bash

src_files="$(dirname $(realpath $0))"/cap

red_echo() {
    echo
    echo -e "\033[0;31m$*\033[0m"
}

red_echo "Running autopep8..."
autopep8 --diff "$src_files"/*.py

red_echo "Running pylint..."
pylint -d C0103,C0114,C0115,C0116,W0102 "$src_files"

red_echo "Running mypy..."
mypy --disallow-untyped-defs --disallow-incomplete-defs "$src_files"

red_echo "Running darglint..."
darglint -m "{path}:{line}: {msg}" -v 2 "$src_files"
