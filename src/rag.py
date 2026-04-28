import os
import re
from typing import Dict, List, Tuple


def load_notes_folder(notes_dir: str) -> Dict[str, str]:
    """Load all markdown notes from a folder into a retrieval corpus."""
    corpus: Dict[str, str] = {}
    if not os.path.isdir(notes_dir):
        return corpus
    for file_name in sorted(os.listdir(notes_dir)):
        if file_name.endswith(".md"):
            path = os.path.join(notes_dir, file_name)
            with open(path, "r", encoding="utf-8") as file:
                corpus[file_name] = file.read()
    return corpus


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def search_notes(query: str, corpus: Dict[str, str], top_k: int = 3) -> List[Tuple[str, str]]:
    """Retrieve the top-matching notes by keyword overlap."""
    query_terms = set(normalize_text(query).split())
    scored: List[Tuple[int, str, str]] = []
    for title, text in corpus.items():
        text_terms = set(normalize_text(text).split())
        score = sum(1 for term in query_terms if term in text_terms)
        score += 1 if title and any(term in normalize_text(title) for term in query_terms) else 0
        scored.append((score, title, text))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [(title, text) for score, title, text in scored if score > 0][:top_k]


def extract_snippet(text: str, max_chars: int = 240) -> str:
    sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]
    if sentences:
        snippet = sentences[0]
    else:
        snippet = text.strip()
    return snippet[:max_chars]


class FineTunedTextModel:
    """A simple specialized model simulation that uses a tone and a subject specialty."""

    def __init__(self, tone: str = "friendly", specialty: str = "study bot"):
        self.tone = tone
        self.specialty = specialty

    def generate_question(self, query: str, retrieved_docs: List[Tuple[str, str]], fallback: bool = False) -> str:
        if not retrieved_docs:
            return f"I couldn't find notes about '{query}', but I can help you study this topic." if fallback else "No notes found to generate a question."
        top_title, top_text = retrieved_docs[0]
        snippet = extract_snippet(top_text)
        if "recommend" in query.lower():
            return (
                f"Based on the notes in '{top_title}', what is the primary factor the music recommender uses when matching songs to a listener?"
            )
        if fallback:
            return (
                f"Reviewing '{top_title}', what would be the most important idea to remember about {query}?"
            )
        return (
            f"As a {self.tone} {self.specialty}, here's a question: "
            f"What does the note from '{top_title}' say is important when choosing songs for a listener?"
        )
