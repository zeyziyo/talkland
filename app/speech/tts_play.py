# app/speech/tts_play.py
import sys
import asyncio
import tempfile
import os
import pygame
import edge_tts

# Args: [text, lang, slow(optional)]
text = sys.argv[1]
lang = sys.argv[2] if len(sys.argv) > 2 else "ko"
slow = "slow" in sys.argv

# Voice Selection - Edge TTS voices for each language
VOICE_MAP = {
    "ko": "ko-KR-SunHiNeural",        # 한국어
    "en": "en-US-JennyNeural",        # English
    "es": "es-ES-AlvaroNeural",       # Español
    "ja": "ja-JP-NanamiNeural",       # 日本語
    "zh": "zh-CN-XiaoxiaoNeural",     # 中文
    "zh-CN": "zh-CN-XiaoxiaoNeural",  # 中文 (간체)
    "fr": "fr-FR-DeniseNeural",       # Français
    "de": "de-DE-KatjaNeural",        # Deutsch
}
voice = VOICE_MAP.get(lang, "en-US-JennyNeural")  # Default to English

# Pitch/Rate adjustment
rate = "-20%" if slow else "+0%"

async def main():
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    
    # Create temp file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        temp_path = f.name
    
    try:
        await communicate.save(temp_path)
        
        # Play with pygame
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        
    except Exception as e:
        print(f"TTS Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

if __name__ == "__main__":
    asyncio.run(main())
