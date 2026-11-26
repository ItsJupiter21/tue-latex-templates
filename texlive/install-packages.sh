#!/usr/bin/env bash
# Installs only the TeX packages listed in packages.txt (plus the build tools), via dnf's
# tex(<file>) provides, so Fedora pulls in just the texlive-* packages that ship those files.
# One pkexec password dialog. Safe to re-run.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
files=$(grep -v '^\s*#' "$HERE/packages.txt" | tr -s ' \t' '\n' | grep -v '^$' | sed "s/.*/tex(&)/")
missing=()
for f in $files; do rpm -q --whatprovides "$f" >/dev/null 2>&1 || missing+=("$f"); done
for tool in latexmk biber texlive-chktex; do rpm -q "$tool" >/dev/null 2>&1 || missing+=("$tool"); done
if ((${#missing[@]} == 0)); then echo "all installed"; exit 0; fi
echo "installing: ${missing[*]}"
pkexec dnf install -y "${missing[@]}"
