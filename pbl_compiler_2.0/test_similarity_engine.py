from matching.similarity_engine import compute_combined_similarity

# Provide the relative paths to the test files in 'test_files/' directory
file1 = "test_files/sample1.py"
file2 = "test_files/sample2.py"

# Run the comparison
score = compute_combined_similarity(file1, file2, lexical_weight=0.4)

print(f"✅ Combined Similarity Score: {score}%")
