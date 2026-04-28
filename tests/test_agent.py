from src.agent import AgenticStudyAgent
from src.reliability import check_quiz_generation_consistency


def test_agent_can_load_notes_and_make_plan():
    agent = AgenticStudyAgent(notes_dir="notes", tone="professional")
    plan = agent.plan("music recommendation")

    assert isinstance(plan, list)
    assert "Search notes" in plan[0]


def test_agent_generates_a_quiz_question():
    agent = AgenticStudyAgent(notes_dir="notes", tone="professional")
    result = agent.run("music recommendation")

    assert result["question"].strip()
    assert isinstance(result["retrieved_docs"], list)
    assert result["retrieved_docs"]


def test_quiz_generation_consistency_is_deterministic():
    agent = AgenticStudyAgent(notes_dir="notes", tone="professional")
    metrics = check_quiz_generation_consistency(agent, "music recommendation", runs=3)

    assert metrics["stable"] is True
    assert metrics["questions"][0] == metrics["questions"][1] == metrics["questions"][2]
