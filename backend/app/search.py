import faiss
import numpy as np


class VectorSearch:

    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.ids = []

    def add(self, vectors, ids):
        vectors = np.array(vectors).astype("float32")
        self.index.add(vectors)
        self.ids.extend(ids)

    def search(self, vector, k=1):
        vector = np.array([vector]).astype("float32")
        distances, indices = self.index.search(vector, k)

        results = []
        for idx in indices[0]:
            if idx < len(self.ids):
                results.append(self.ids[idx])

        return results
