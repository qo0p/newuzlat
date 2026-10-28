#!/bin/sh
# Build UzbekLatin.msi in Docker (works on Linux/macOS, or Windows with Docker Desktop).
set -e
cd "$(dirname "$0")"
docker build -q -t uzlat-msi-builder . >/dev/null
docker run --rm --user "$(id -u):$(id -g)" -v "$(cd .. && pwd)":/src/windows uzlat-msi-builder
