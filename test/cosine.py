import numpy as np
import sys

def calculate_cosine_similarity_numpy(vec1, vec2):
    """
    Calculates the cosine similarity between two vectors using NumPy.

    Args:
        vec1 (numpy.ndarray or list): The first vector.
        vec2 (numpy.ndarray or list): The second vector.

    Returns:
        float: The cosine similarity between the two vectors.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    magnitude_vec1 = np.linalg.norm(vec1)
    magnitude_vec2 = np.linalg.norm(vec2)

    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0  # Handle cases where one or both vectors are zero vectors

    cosine_sim = dot_product / (magnitude_vec1 * magnitude_vec2)
    return cosine_sim

# Example usage:
with open("./embedding_a.txt") as file:
    string = file.read()
    vectors_a = [
        float(x) for x in string.split('\n')[0].split(', ')
    ]



with open("./embedding_b.txt") as file:
    string = file.read()
    vectors_b = [
        float(x) for x in string.split('\n')[0].split(', ')
    ]

for i in range(len(vectors_a)):
    print(vectors_a[i]==vectors_b[i])