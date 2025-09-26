# matching/semantic_matcher.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained model ONCE at module level
model = SentenceTransformer('all-MiniLM-L6-v2')

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def compute_semantic_similarity(file1_path, file2_path):
    # Use the already loaded model
    code1 = read_file(file1_path)
    code2 = read_file(file2_path)

    # Create embeddings
    embeddings = model.encode([code1, code2])

    # Compute cosine similarity
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    # Return as percentage
    return round(similarity * 100, 2)
