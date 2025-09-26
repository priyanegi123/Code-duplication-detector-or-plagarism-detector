import tokenize
import io
from difflib import SequenceMatcher
from preprocessing.cleaner import clean_code_from_string


def tokenize_code(code):
    """
    Tokenizes Python code into a list of tokens (excluding comments, whitespace).
    """
    tokens = []
    reader = io.BytesIO(code.encode('utf-8')).readline
    try:
        for tok in tokenize.tokenize(reader):
            if tok.type not in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.ENCODING):
                tokens.append(tok.string)
    except tokenize.TokenError:
        pass  # ignore invalid token errors
    return tokens

def calculate_similarity(tokens1, tokens2):
    """
    Calculates lexical similarity using SequenceMatcher.
    """
    matcher = SequenceMatcher(None, tokens1, tokens2)
    return matcher.ratio()

def compare_files_lexically(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        raw_code1 = file1.read()
        raw_code2 = file2.read()

    code1 = clean_code_from_string(raw_code1)
    code2 = clean_code_from_string(raw_code2)

    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)

    similarity_ratio = calculate_similarity(tokens1, tokens2)
    return round(similarity_ratio * 100, 2)


# For testing this file directly
if __name__ == "__main__":
    file1 = "cleaned_output1.py"
    file2 = "cleaned_output2.py"
    score = compare_files_lexically(file1, file2)
    print(f"🔍 Lexical Similarity: {score}%")
