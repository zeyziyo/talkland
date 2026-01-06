# server.py
"""
TalkLand Flask Server

서버 기능:
1. HTML UI 서빙
2. 번역 API (/api/translate)
3. TTS API (/api/tts)
4. Edge TTS를 사용한 고품질 음성 생성
"""

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import asyncio
import tempfile
import os
import edge_tts
from pathlib import Path
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 접근 허용

# ===========================================
# Homepage
# ===========================================

@app.route('/')
def index():
    """HTML UI 서빙"""
    return render_template('index.html')

# 정적 파일 서빙 (PWA)
@app.route('/static/<path:filename>')
def serve_static(filename):
    """PWA 파일 서빙"""
    from flask import send_from_directory
    return send_from_directory('static', filename)

# ===========================================
# Translation API
# ===========================================

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """
    Google 번역 API
    
    Request JSON:
    {
        "text": "안녕하세요",
        "source_lang": "ko",
        "target_lang": "ja"
    }
    
    Response JSON:
    {
        "translated_text": "こんにちは"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'en')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        print(f"[Translation API] {source_lang} -> {target_lang}: '{text[:30]}...'")
        
        # Google Translator 사용
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        
        return jsonify({
            "translated_text": translated,
            "source_lang": source_lang,
            "target_lang": target_lang
        })
        
    except Exception as e:
        print(f"[Translation API] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ===========================================
# TTS API
# ===========================================

@app.route('/api/tts', methods=['POST'])
def generate_tts():
    """
    Edge TTS로 음성 생성 후 MP3 반환
    
    Request JSON:
    {
        "text": "안녕하세요",
        "voice": "ko-KR-Neural2-C",
        "rate": "+0%"
    }
    
    Response: MP3 binary data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get('text', '')
        voice = data.get('voice', 'ko-KR-SunHiNeural')
        rate = data.get('rate', '+0%')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        print(f"[TTS API] Generating speech: text='{text[:30]}...', voice={voice}")
        
        # Edge TTS로 MP3 생성 (비동기 함수 호출)
        mp3_path = asyncio.run(generate_speech(text, voice, rate))
        
        # MP3 파일 반환
        response = send_file(
            mp3_path,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='speech.mp3'
        )
        
        # 파일 전송 후 삭제
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                    print(f"[TTS API] Cleaned up temp file: {mp3_path}")
            except Exception as e:
                print(f"[TTS API] Cleanup error: {e}")
        
        return response
        
    except Exception as e:
        print(f"[TTS API] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


async def generate_speech(text: str, voice: str, rate: str = "+0%") -> str:
    """
    Edge TTS로 음성 생성
    
    Args:
        text: 음성으로 변환할 텍스트
        voice: 음성 코드 (e.g., 'ko-KR-Neural2-C')
        rate: 속도 (e.g., '+0%', '-20%')
    
    Returns:
        생성된 MP3 파일 경로
    """
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    
    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        temp_path = f.name
    
    # MP3 저장
    await communicate.save(temp_path)
    
    print(f"[TTS] Generated MP3: {temp_path}")
    return temp_path


# ===========================================
# Health Check
# ===========================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({
        "status": "ok",
        "service": "TalkLand TTS Server",
        "version": "1.0.0"
    })


# ===========================================
# Main
# ===========================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"[Server] Starting TalkLand TTS Server on port {port}")
    print(f"[Server] TTS API: http://localhost:{port}/api/tts")
    print(f"[Server] Health: http://localhost:{port}/api/health")
    
    # Production: gunicorn will handle this
    # Development: run with Flask's built-in server
    if os.getenv('RENDER'):
        # Render.com uses gunicorn, this won't run
        pass
    else:
        # Local development
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True
        )

