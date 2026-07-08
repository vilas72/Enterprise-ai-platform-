import math


class Similarity:
    """
    Utility class for vector similarity calculations.
    """

    @staticmethod
    def cosine_similarity(
        vector1: list[float],
        vector2: list[float],
    ) -> float:
        """
        Calculate cosine similarity between two vectors.
        """

        if len(vector1) != len(vector2):
            raise ValueError(
                "Vectors must have the same dimensions."
            )

        dot_product = sum(
            a * b
            for a, b in zip(vector1, vector2)
        )

        magnitude1 = math.sqrt(
            sum(a * a for a in vector1)
        )

        magnitude2 = math.sqrt(
            sum(b * b for b in vector2)
        )

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)