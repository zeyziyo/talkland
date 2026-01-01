# TalkLand (TalkLand)

A language learning app with speech recognition and translation.

## 🚨 IMPORTANT FOR AI AGENTS & DEVELOPERS 🚨

**Before making ANY changes, you MUST consult the `knowledge_base/` directory.**
Critical project constraints and architectural decisions are documented there.

### 📚 Knowledge Base
- **[Flet Android Guide](knowledge_base/flet_android_guide.md)**: Contains STRICT rules for Android deployment and Flet 0.80.0+ migration.
    - **CRITICAL**: We use Flet **0.80.0+**. `AudioRecorder` is NOT in `flet` core anymore. Use `flet-audio-recorder` package.
    - **CRITICAL**: Use `ft.app` for mobile entry point.
    - **CRITICAL**: For ANY Flet-related code, you MUST verify against the [Official Flet Documentation](https://docs.flet.dev/). Do not rely on training data or assumptions.

### 🛠️ Tech Stack
- **Framework**: Flet (>=0.80.0)
- **Audio**: `flet-audio-recorder` (>=0.80.0)
- **Speech-to-Text**: Google Speech Recognition
- **Translator**: `deep-translator`

### 🚀 Getting Started
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run locally (Desktop):
   ```bash
   flet run main.py
   ```
   *(Note: Desktop uses a different speech backend than Android. See `app/speech/` for details.)*

### 📱 Android Build
Refer to `knowledge_base/flet_android_guide.md` and `.github/workflows/build-apk.yml`.
