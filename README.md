Here's the modified README, restructured to match the auto‑debugger example while preserving all the original project details.

```markdown
# 🎵 Music Recommender + Study Bot

## Overview
A CLI tool that recommends songs from `data/songs.csv` based on genre, mood, energy, and tempo, and also provides an AI‑powered study assistant. The study assistant uses **retrieval‑augmented generation (RAG)** to ground quiz questions in provided notes, follows an **agentic plan‑act‑check** loop, and adapts its tone (friendly / professional) via a simulated specialized model. This solves the meaningful problem of building an explainable, reliable AI workflow that combines retrieval, planning, and self‑evaluation in one integrated system.

## Base Project
This project extends the **Module 3: Building an LLM-Powered Application** project, which originally demonstrated a single‑shot, rule‑based music recommender. The final project evolves it into a complete applied AI system by adding:

- Retrieval‑augmented generation (RAG) over study notes
- An agentic workflow with planning, acting, and self‑checking
- A simulated fine‑tuned model that changes output tone
- Reliability harness for consistency evaluation

## Core AI Feature
**Agentic Workflow with RAG** – The AI acts as a self‑guided study assistant. It first plans what information to retrieve, then searches notes for relevant passages, generates a quiz question grounded in those passages, and finally validates its own output. The entire workflow is observable and repeatable.

## System Architecture

![Architecture Diagram](recommendation_flowchart.mmd) *(Note: The `.mmd` file can be rendered as a diagram; see the original repository.)*

### Components & Data Flow
1. **CLI Interface** (`src/main.py`) – Accepts command‑line arguments: mode (`recommend`, `quiz`, `reliability`), query, tone, number of top results.
2. **Recommender** (`src/recommender.py`) – Loads songs, scores them by genre, mood, energy, and tempo, returns ranked recommendations with explanations.
3. **RAG & Agent Modules** (`src/rag.py`, `src/agent.py`) – Index study notes by paragraph, retrieve relevant passages based on keyword matching, and generate quiz questions using a simulated fine‑tuned model that changes wording based on the selected tone.
4. **Agentic Workflow** (`src/agent.py`) – Executes a plan‑act‑check loop:
   - **Plan**: Decides which topics to look for.
   - **Act**: Retrieves notes and generates a question.
   - **Check**: Verifies that the question references the retrieved notes.
5. **Reliability Harness** (`src/reliability.py`) – Repeats recommendations and quiz generation multiple times, then reports stability metrics (consistency of top results, similarity of generated questions).
6. **Data Stores** – `data/songs.csv` for music, `data/notes/` for study notes.

**Data flow**:  
User input → CLI → Mode selection →  
- **Recommend**: Recommender → scored songs → output.  
- **Quiz**: Agent plan → retrieve notes → generate question (with tone) → self‑check → output.  
- **Reliability**: Repeat recommendations and quiz generation → compute stability scores → output.

## Setup Instructions

### Prerequisites
- Python 3.8+
- No external API keys required (simulated LLM)

### Step‑by‑Step Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jbvillegas/ai110-module3show-musicrecommendersimulation-starter.git
   cd ai110-module3show-musicrecommendersimulation-starter
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Sample Interactions

Here are three examples of the system in action.

### Example 1: Song Recommendation
**Command**:
```bash
python -m src.main --mode recommend --top_k 3
```
**Output**:
```
Top 3 recommendations:
1. "Bohemian Rhapsody" (Score: 0.92)
   - genre match: rock
   - energy close
   - tempo close
2. "Stairway to Heaven" (Score: 0.88)
   ...
```

### Example 2: Quiz Generation (Friendly Tone)
**Command**:
```bash
python -m src.main --mode quiz --query "music recommendation" --tone "friendly"
```
**Output**:
```
[PLAN] I will search notes for 'music recommendation' and related terms.
[ACT] Retrieved notes: 'recommendation_basics.txt', 'user_preferences.txt'
[ACT] Generated question: "Hey! Can you explain how genre and energy affect song recommendations?"
[CHECK] Validity: True (question references retrieved notes)
```

### Example 3: Reliability Check
**Command**:
```bash
python -m src.main --mode reliability
```
**Output**:
```
Reliability metrics (5 runs):
- Recommendation stability: 0.95 (top-3 identical across runs)
- Quiz consistency: average similarity 0.87
- Sample generated question: "What is the role of energy scoring in music recommendations?"
```

## Design Decisions & Trade‑offs

| Decision | Rationale | Trade‑off |
|----------|-----------|-----------|
| Keyword‑based retrieval (no vector DB) | Works without external APIs, deterministic | May miss semantically similar notes not sharing keywords |
| Simulated specialized model (tone switching) | Reproducible, no fine‑tuning cost | Not a real LLM; limited flexibility |
| Agentic plan‑act‑check loop | Makes reasoning observable, easier to debug | Slower than single‑shot generation |
| Rule‑based recommendation scoring | Explainable and fast | Cannot learn from user behavior |
| Reliability repeats only 5 times | Balances speed and statistical confidence | Might miss rare instability |

## Reliability & Testing

### Automated Test Harness
Run all tests with:
```bash
python -m pytest -q
```

The test suite includes 5 tests covering:
- Recommendation sorting and explanation generation
- Agent planning and question creation
- Retrieval‑driven quiz generation
- Reliability metrics computation

### Test Results
- **Tests passed**: 5/5
- **Recommendation stability**: >0.9 on repeated runs
- **Quiz generation validity**: 100% of questions pass the self‑check (reference retrieved notes)

### Confidence & Guardrails
- **Self‑check guardrail**: The agent verifies that the generated question contains phrases from the retrieved notes. If not, it flags the output.
- **Input validation**: CLI arguments are type‑checked and range‑checked (e.g., `--top_k` must be positive).
- **Consistency evaluation**: The reliability module computes similarity between multiple outputs and alerts if variance exceeds a threshold.

## Reflection & Ethics

### Limitations & Biases
- The keyword retriever may miss relevant material if users phrase queries differently.
- The simulated fine‑tuned model only changes tone superficially; it does not learn from data.
- The recommender over‑weights genre and energy, which may favour certain music styles.

### Potential Misuse & Prevention
- **Misuse**: Generating misleading or false quiz questions if notes contain inaccurate information.
- **Prevention**: The self‑check guardrail ensures questions are grounded in the provided notes. In a production system, we would also add human review for educational content.

### Surprising Findings
- During testing, the agentic loop sometimes produced better questions after the self‑check flagged a weak output, even though we don't automatically retry (the flag only warns). This suggests that a full retry loop could further improve quality.
- Simulating tone changes with simple string replacement worked well for demo purposes, but real fine‑tuning would be needed for serious applications.

### AI Collaboration Log
*See `model_card.md` for a detailed log of AI suggestions during development, including one helpful suggestion (using a plan‑act‑check structure) and one flawed suggestion (overly complex retrieval that chunked notes too aggressively).*

## Portfolio & Presentation

- **Loom Video Walkthrough**: [https://www.loom.com/share/3a78fc5356fe4367bf516aff0c1e3ada]
  Shows end‑to‑end runs for recommendation, quiz generation, and reliability check.
- **GitHub Repository**: [https://github.com/jbvillegas/ai110-module3show-musicrecommendersimulation-starter](https://github.com/jbvillegas/ai110-module3show-musicrecommendersimulation-starter)
- **Project Reflection Paragraph** (for portfolio):  
  *This project demonstrates my ability to integrate retrieval, agentic planning, and reliability into a practical AI system. By combining a rule‑based recommender with a RAG‑powered study assistant that self‑checks its outputs, I built a solution that is both transparent and robust. It showcases my skills in prompt engineering, workflow orchestration, and building for evaluation—key competencies for an AI engineer.*

## Usage (Command Reference)

```bash
# Recommend top 5 songs (default top_k=5)
python -m src.main --mode recommend

# Recommend top 3 songs
python -m src.main --mode recommend --top_k 3

# Generate a quiz question (friendly tone)
python -m src.main --mode quiz --query "collaborative filtering" --tone friendly

# Generate a quiz question (professional tone)
python -m src.main --mode quiz --query "energy scoring" --tone professional

# Run reliability evaluation
python -m src.main --mode reliability
```

## License

MIT License – see [LICENSE](LICENSE) file for details.
