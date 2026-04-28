# 🎵 Music Recommender + Study Bot

## Project Summary

This project extends the original Music Recommender Simulation with an AI-driven study assistant. It still recommends songs from `data/songs.csv` based on genre, mood, energy, and tempo, but now also includes:

- Retrieval-augmented generation (RAG) using notes before answer generation
- An agentic workflow that plans, acts, and checks its own work
- A simulated specialized model tone for the study assistant
- Reliability checks for recommendation and quiz output consistency

This makes the project a portfolio-ready example of a complete AI workflow, not just a rule-based recommender.

---

## Architecture Overview

The system is organized around three main components:

- `src/recommender.py`: loads songs, scores them, and returns ranked recommendations.
- `src/rag.py` + `src/agent.py`: loads notes, retrieves relevant passages, and generates quiz questions in a specialized tone.
- `src/reliability.py`: evaluates consistency and stability across repeated runs.

Data flow:

1. Input arrives through `src/main.py` as a selected mode.
2. Recommendation mode scores songs and returns top matches.
3. Quiz mode searches notes first, then generates a question grounded in those notes.
4. Reliability mode repeats output generation and reports stability metrics.

---

## Setup Instructions

1. Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run recommendations:

   ```bash
   python -m src.main --mode recommend
   ```

4. Run the RAG-powered study bot:

   ```bash
   python -m src.main --mode quiz --query "music recommendation" --tone "friendly"
   ```

5. Run reliability evaluation:

   ```bash
   python -m src.main --mode reliability
   ```

---

## Sample Interactions

### Recommendation Example

```bash
python -m src.main --mode recommend --top_k 3
```

Expected output includes top songs with scores and reason summaries like:

- genre match
- energy closeness
- tempo closeness

### Quiz Generation Example

```bash
python -m src.main --mode quiz --query "music recommendation" --tone "professional"
```

Expected output includes:

- the agent plan
- retrieved note titles
- a quiz question grounded in the retrieved notes
- a validity check result

### Reliability Example

```bash
python -m src.main --mode reliability
```

Expected output includes metrics for:

- recommendation stability
- quiz generation consistency
- an example generated question

---

## Design Decisions

- I used a lightweight keyword-based retriever so the RAG flow works without external APIs.
- The study assistant is modeled as a simulated specialized model in `src/rag.py`, which changes wording based on a selected tone.
- The agent uses a visible plan-act-check loop in `src/agent.py`, making the workflow auditable and easier to test.
- Reliability is measured by repeating outputs and checking whether results remain stable.

Trade-offs:

- The specialized model is simulated rather than a real fine-tuned LLM, so it is reproducible but not as flexible.
- The recommendation logic remains rule-based, keeping it explainable but not learned from user behavior.

---

## Testing Summary

Automated tests cover:

- recommendation sorting and explanations
- agent planning and question generation
- retrieval-driven quiz generation
- reliability checks for repeated outputs

Run tests with:

```bash
python -m pytest -q
```

Current status: 5 tests passed.

---

## Reflection

This project taught me how retrieval and planning can be integrated into a small but meaningful AI workflow. It also reinforced that reliability matters: repeated runs are important to detect drift or unstable behavior.

Limitations:

- The note retriever is keyword-based and may miss semantically relevant material.
- The recommender still favors songs with strong genre or energy matches.
- The system is designed for demonstration rather than real streaming service use.

Ethics and responsibility:

I kept the project focused on safe domains like music and studying, and I added validation checks so the AI workflow is less likely to produce unpredictable outputs.
