# matching/similarity_engine.py

from matching.lexical_matcher import compare_files_lexically
from matching.semantic_matcher import compute_semantic_similarity
import difflib

def compute_combined_similarity(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1:
        lines1 = f1.read().splitlines()
    with open(file2, 'r', encoding='utf-8') as f2:
        lines2 = f2.read().splitlines()

    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    score = matcher.ratio() * 100

    matched1 = []
    matched2 = []
    for block in matcher.get_matching_blocks():
        i, j, n = block
        if n > 0:
            for k in range(n):
                # Store (line_number, line_content)
                matched1.append((i + k + 1, lines1[i + k]))
                matched2.append((j + k + 1, lines2[j + k]))

    return score, matched1, matched2

if __name__ == "__main__":
    score, matched1, matched2 = compute_combined_similarity("test1.py", "test2.py")
    print("Score:", score)
    print("Matched1:", matched1)
    print("Matched2:", matched2)
