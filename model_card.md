
# 🎧 Model Card: VibeFinder 2.0

## Model Name
VibeFinder 2.0

## Goal / Task
Suggests songs that match a user's musical taste and provides explainable, reliable recommendations. Also acts as a study assistant by generating quiz questions grounded in project notes.

## Data Used
Uses a CSV file with song metadata (id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness, etc.). Study notes are stored as markdown files and used for retrieval-augmented quiz generation.

## Algorithm Summary
- **Music Recommendation:** Combines retrieval and rule-based scoring. Songs are filtered and ranked by genre, mood, energy, and tempo similarity to user preferences. Explanations are generated for each recommendation.
- **Agentic Study Assistant:** Uses a plan-act-check agent loop to generate quiz questions. Retrieves relevant notes, generates a question, and self-checks for grounding and clarity.
- **Reliability Harness:** Includes automated tests for recommendation stability and quiz consistency. Guardrails ensure only valid songs/genres are recommended and that outputs are deterministic for the same input.

## Observed Behavior / Biases
- Popular genres or high-energy songs may dominate results if the dataset is small.
- The system is robust to invalid input and produces consistent results for repeated queries.
- Quiz questions are always grounded in the provided notes, preventing hallucination.

## Evaluation Process
- Tested with multiple user profiles and edge cases.
- Ran automated tests for recommendation and quiz stability (same input yields same output).
- Evaluated system guardrails by providing invalid or out-of-domain input.

## Intended Use and Non-Intended Use
- For educational demos and learning about applied AI, retrieval, and agentic workflows.
- Not for real music streaming or commercial use.
- Not intended for generating real user playlists or ungrounded quiz content.

## Ideas for Improvement
- Expand the song and note datasets for more variety and realism.
- Add user feedback to refine recommendations over time.
- Experiment with machine learning or hybrid approaches for ranking.
- Enhance the UI for better user interaction and transparency.

## Personal Reflection

Biggest learning moment: The quality and reliability of recommendations depend not just on the scoring logic, but on disciplined data handling, retrieval, and evaluation. Adding agentic and RAG features made the system more explainable and robust, but also required careful testing and guardrails.

AI tools accelerated development, especially for code generation and test design, but still required human oversight for edge cases and integration. The most surprising aspect was how much small changes in input structure or retrieval logic could affect the user experience.

If I continued, I’d focus on richer data, more user controls, and deeper evaluation of both recommendation quality and system reliability.
