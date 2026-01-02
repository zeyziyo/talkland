# Android Build Configuration Reference

This document serves as a reference for the correct configuration required to build the Android APK for TalkLand using Flet. It captures the state of the project files that resolved the build errors encountered on 2026-01-02.

## Key Build Rules
1. **Do NOT use `--include-packages`**: The `flet build apk` command dropped support for this flag. Use `requirements.txt` instead.
   - ❌ Incorrect: `flet build apk --include-packages flet_audio_recorder`
   - ✅ Correct: `flet build apk --verbose` (and ensure `requirements.txt` exists)
2. **`requirements.txt` is Mandatory**: Flet's build process looks for this file to install pure Python dependencies into the Android environment.
3. **Permissions**: Defined in `pyproject.toml` under `[tool.flet.android]`.

---

## 1. GitHub Actions Workflow (`.github/workflows/build-apk.yml`)
This workflow successfully builds the APK. Note the clean `flet build` command.

```yaml
name: Build Android APK & AAB

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    permissions:
      contents: read
      packages: write

    steps:
      - name: Free Disk Space
        uses: jlumbroso/free-disk-space@main
        with:
          tool-cache: false
          android: false
          dotnet: true
          haskell: true
          large-packages: true
          docker-images: true
          swap-storage: true

      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'
          cache: true

      - name: Install Dependencies
        run: |
          pip install .
          pip install flet

      - name: Restore Android keystore
        run: |
          echo "${{ secrets.ANDROID_KEYSTORE_BASE64 }}" | base64 --decode > upload-keystore.jks

      - name: Create key.properties
        run: |
          echo "storeFile=upload-keystore.jks" > key.properties
          echo "storePassword=${{ secrets.ANDROID_KEYSTORE_PASSWORD }}" >> key.properties
          echo "keyAlias=${{ secrets.ANDROID_KEY_ALIAS }}" >> key.properties
          echo "keyPassword=${{ secrets.ANDROID_KEY_PASSWORD }}" >> key.properties    

      - name: Move key.properties to android directory
        run: |
          mkdir -p android
          mv key.properties android/key.properties

      # APK 빌드
      - name: Flet Build APK
        run: |
          flet build apk --verbose

      # APK 업로드
      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: talkland-apk
          path: build/apk/*.apk
          if-no-files-found: error
```

## 2. Dependencies (`requirements.txt`)
Contains package requirements for the Android environment.

```text
flet>=0.80.0
flet-audio-recorder>=0.80.0
deep-translator
SpeechRecognition
```

## 3. Project Configuration (`pyproject.toml`)
Defines metadata and Android-specific permissions.

```toml
[project]
name = "talkland"
version = "0.1.0"
description = "TalkLand - Language Learning App"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "flet>=0.80.0",
    "flet-audio-recorder>=0.80.0",
    "deep-translator",
    "SpeechRecognition"
]

[tool.setuptools.packages.find]
include = ["app*"]


[tool.flet]
platforms = ["android"]

[tool.flet.android]
permissions = ["android.permission.RECORD_AUDIO", "android.permission.INTERNET"]
```
