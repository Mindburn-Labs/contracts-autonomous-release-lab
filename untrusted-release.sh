#!/usr/bin/env bash
set -euo pipefail
git tag -f autonomous-approved
git push --force origin autonomous-approved
