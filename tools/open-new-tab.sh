#!/usr/bin/env bash
set -e

if [ $# -lt 1 ]; then (>&2 echo "Usage: $0 path/to/file.md [project/root/]"; exit 1); fi

server_host="${SERVER_HOST:-127.0.0.1:5000}"
read rel_path < <(python3 \
  -c "from sys import argv; \
      from os import path; \
      print(path.relpath(argv[1], argv[2]))" \
  "${1%.md}" "${2:-.}/md")
google-chrome "http://$server_host/#/$rel_path" 2>/dev/null
