from __future__ import annotations

import random

from dataclasses import dataclass


@dataclass(frozen=True)
class Word:
    term: str
    meaning: str


def normalize_answer(text: str) -> str:
    return " ".join(text.strip().lower().split())


def check_answer(word: Word, user_input: str) -> bool:
    return normalize_answer(user_input) == normalize_answer(word.meaning)


def draw_word(words: list[Word], rng: random.Random | None = None) -> Word:
    if not words:
        raise ValueError("Word list is empty")
    chooser = rng if rng is not None else random
    return chooser.choice(words)

REVIEW_TIMELINE = {}

def filter_ebbinghaus_words(words: list[Word], current_round: int) -> list[Word]:
    candidates = []
    for word in words:
        next_ready_round = REVIEW_TIMELINE.get(word.term, 0)
        if next_ready_round <= current_round:
            candidates.append(word)
            
    # 전부 복습해야 한다면 전체 단어 반환
    if not candidates:
        return words
    return candidates

def record_review_schedule(word: Word, is_correct: bool, current_round: int):
 	    # 정답 여부에 따라 다음 출제 타이밍을 예약
    if is_correct:
        # 맞췄다면 '3판 뒤'에 출제되도록 예약
        REVIEW_TIMELINE[word.term] = current_round + 3
    else:
        # 틀렸다면 '바로 다음 판'에 또 나오게 예약
        REVIEW_TIMELINE[word.term] = current_round + 1
