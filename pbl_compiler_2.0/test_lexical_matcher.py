from matching.lexical_matcher import compare_files_lexically

file1 = 'test_files/sample1.py'
file2 = 'test_files/sample2.py'

score = compare_files_lexically(file1, file2)
print(f"🧠 Lexical Similarity Score: {score:.2f}%")
