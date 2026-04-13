# Reflection on Profile Comparisons

- High-Energy Pop vs. Chill Lofi: High-Energy Pop profile consistently surfaces songs like "Gym Hero" and "Sunrise City" because they match both genre and high energy. Chill Lofi profile shifts toward tracks like "Library Rain" and "Midnight Coding"—lower energy, lofi genre, and chill mood. This makes sense: the scoring logic rewards close matches to both genre and energy, so the output reflects the user's stated taste.

- Deep Intense Rock vs. High-Energy Pop: "Storm Runner" appears for Deep Intense Rock due to matching genre, mood, and high energy. High-Energy Pop sometimes includes "Storm Runner" but also features more pop songs. This shows the system can distinguish between genres when preferences are clear.

- Adversarial profiles (e.g., high energy + sad mood): Recommendations are less relevant or repetitive, often defaulting to songs with high energy even if mood doesn't match. This exposes a limitation: the system can't always find good matches for rare or conflicting preferences, so it falls back on the strongest weighted features.

- "Gym Hero" for Happy Pop: "Gym Hero" keeps showing up for happy pop profiles because it matches both the pop genre and high energy, which are heavily weighted in the scoring logic. If the dataset has few happy pop songs, the same track will dominate recommendations.
