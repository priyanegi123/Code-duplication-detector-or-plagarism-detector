# test_semantic_matcher.py

from matching.semantic_matcher import compute_semantic_similarity

file1 = 'test_files/sample1.py'
file2 = 'test_files/sample2.py'

score = compute_semantic_similarity(file1, file2)
print(f"🧠 Semantic Similarity Score: {score}%")
