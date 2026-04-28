from typing import Dict, List, Tuple

from .rag import FineTunedTextModel, load_notes_folder, search_notes


class AgenticStudyAgent:
    """An agentic study assistant that plans, acts, and checks its own work."""

    def __init__(self, notes_dir: str = "notes", tone: str = "friendly"):
        self.notes_dir = notes_dir
        self.tone = tone
        self.model = FineTunedTextModel(tone=tone, specialty="study assistant")
        self.corpus = load_notes_folder(notes_dir)

    def plan(self, topic: str) -> List[str]:
        return [
            f"Search notes for '{topic}'",
            "Generate a quiz question from the retrieved passages",
            "Verify the question references the notes and is clear",
        ]

    def act(self, topic: str) -> Tuple[str, List[Tuple[str, str]]]:
        retrieved = search_notes(topic, self.corpus, top_k=3)
        question = self.model.generate_question(topic, retrieved)
        return question, retrieved

    def self_check(self, question: str, retrieved_docs: List[Tuple[str, str]]) -> bool:
        if not question.strip():
            return False
        if not retrieved_docs:
            return False
        return topic_in_question(question, retrieved_docs)

    def run(self, topic: str) -> Dict[str, object]:
        plan = self.plan(topic)
        question, retrieved_docs = self.act(topic)
        valid = self.self_check(question, retrieved_docs)
        if not valid:
            question = self.model.generate_question(topic, retrieved_docs, fallback=True)
        return {
            "plan": plan,
            "question": question,
            "retrieved_docs": [title for title, _ in retrieved_docs],
            "valid": valid,
        }


def topic_in_question(question: str, retrieved_docs: List[Tuple[str, str]]) -> bool:
    lower_question = question.lower()
    for title, text in retrieved_docs:
        if title.lower() in lower_question:
            return True
        for token in title.lower().split():
            if token and token in lower_question:
                return True
    return False
