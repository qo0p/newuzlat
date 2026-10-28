# Builds UzbekLatin.msi on Linux with msitools (wixl + msibuild). See build.sh.
FROM ubuntu:24.04
RUN apt-get update \
 && apt-get install -y --no-install-recommends wixl msitools python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /src/windows/installer
ENTRYPOINT ["python3", "make_msi.py"]
