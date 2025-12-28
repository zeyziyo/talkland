# app/text/compare.py
from __future__ import annotations
from typing import List, Tuple, Optional, Iterable

IGNORE_WORDS: dict[str, set[str]] = {
    "Beginner": {"a", "the", "to", "of"},
    "Intermediate": {"a", "the"},
    "Advanced": set(),
}


def compare_sentence(
    target: str,
    spoken: Optional[str],
    level: Optional[str],
) -> List[Tuple[str, bool]]:
    """
    목표 문장과 발화 문장을 단어 단위로 비교한다.

    - spoken / level 이 None이어도 안전
    - level에 따라 무시 단어 적용
    - 반환값: [(단어, 맞음 여부)]
    """

    spoken_text = spoken or ""
    safe_level = level if level in IGNORE_WORDS else "Beginner"

    target_words = target.lower().split()
    spoken_words = spoken_text.lower().split()

    ignore_words = IGNORE_WORDS[safe_level]

    result: list[tuple[str, bool]] = []

    for i, word in enumerate(target_words):
        if word in ignore_words:
            result.append((word, True))
            continue

        spoken_word = spoken_words[i] if i < len(spoken_words) else ""
        result.append((word, word == spoken_word))

    return result
