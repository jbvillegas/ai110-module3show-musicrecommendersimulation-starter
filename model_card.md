# 🎧 Model Card: VibeFinder 1.0

## Model Name
VibeFinder 1.0

## Goal / Task
Suggests songs that match a user's musical taste. Predicts which songs a user will like based on genre, mood, energy, and tempo.

## Data Used
Uses a CSV file with 17 songs. Each song has: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness. Limited by small size and genre variety.

## Algorithm Summary
Scores each song by matching genre (+1 or +2), mood (+1), energy (closer is better), and tempo (closer is better). Adds up points for each match. Ranks songs by total score and recommends the top ones.

## Observed Behavior / Biases
Songs with popular genres or high energy often rank higher. If a genre is common in the data, those songs show up more. Rare or conflicting preferences get less relevant results. Same songs can repeat if the dataset is small.

## Evaluation Process
Tested with different user profiles (pop, lofi, rock, edge cases). Compared top results for each. Changed weights and features to see how rankings shift. Wrote reflections on what changed and why.

## Intended Use and Non-Intended Use
For classroom demos and learning about recommenders. Not for real music streaming or commercial use. Not for making real user playlists.

## Ideas for Improvement
- Add more songs and genres for better variety.
- Let users pick more than one favorite genre or mood.
- Tune weights or use machine learning for smarter scoring.

## Personal Reflection

Biggest learning moment: Realizing how much impact simple weights and feature choices have on recommendations. Even small changes in the scoring logic can shift results a lot.

AI tools helped speed up coding and gave ideas for edge cases and experiments. I still had to double-check logic, especially for math and when results looked odd. Sometimes, AI suggestions needed tweaks to fit my dataset or goals.

I was surprised that even a basic scoring system can make recommendations that "feel" personal, but also how quickly it can get stuck in a rut if the data or weights are off.

If I kept going, I'd add more data, let users pick multiple genres/moods, and maybe try a machine learning approach to learn weights from real user choices.
