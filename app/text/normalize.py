# app/text/normalize.py
from __future__ import annotations
import re
from typing import Optional


def normalize_spoken(text: Optional[str]) -> str:
    """
    STT 결과 텍스트를 비교용으로 정규화한다.

    처리 내용:
    - None 안전 처리
    - 소문자 변환
    - 특수문자 제거
    - 공백 정리

    이 함수는:
    - STT 구현과 무관
    - 플랫폼 독립
    - 순수 함수
    """

    if not text:
        return ""

    # 소문자
    text = text.lower()

    # 특수문자 제거 (알파벳, 숫자, 공백만 유지)
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # 공백 정리
    text = re.sub(r"\s+", " ", text).strip()

    return text
