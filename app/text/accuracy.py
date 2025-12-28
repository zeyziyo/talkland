# app/text/accuracy.py
from __future__ import annotations
from typing import Iterable, Tuple, Optional


def accuracy(
    compare: Optional[Iterable[Tuple[str, bool]]]
) -> float:
    """
    단어 비교 결과로부터 정확도를 계산한다.

    - compare가 None 또는 비어 있으면 0.0
    """

    if not compare:
        return 0.0

    total = 0
    correct = 0

    for _, ok in compare:
        total += 1
        if ok:
            correct += 1

    return correct / total if total else 0.0
