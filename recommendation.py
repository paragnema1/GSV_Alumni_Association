from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Simulated data: [user_id, skill_vector]
users = {
    'student1': [1, 0, 0, 1, 1],
    'student2': [0, 1, 1, 0, 0],
    'alumni1': [1, 0, 1, 0, 1],
    'alumni2': [0, 1, 0, 1, 0]
}

def recommend_connections(user_id):
    if user_id not in users:
        return {'error': 'User not found'}

    user_vector = np.array(users[user_id]).reshape(1, -1)
    similarities = {}

    for other_user_id, other_vector in users.items():
        if other_user_id != user_id:
            other_vector = np.array(other_vector).reshape(1, -1)
            similarity = cosine_similarity(user_vector, other_vector)[0][0]
            similarities[other_user_id] = similarity

    # Sort by similarity score in descending order
    recommended_users = sorted(similarities, key=similarities.get, reverse=True)
    return {'recommendations': recommended_users}

# Example usage
if __name__ == '__main__':
    print(recommend_connections('student1'))
