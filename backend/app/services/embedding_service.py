import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional
from loguru import logger
from app.core.config import settings

class EmbeddingService:
    """Service for generating and comparing embeddings."""
    
    def __init__(self):
        """Initialize the embedding model."""
        try:
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info(f"Loaded embedding model: {settings.EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self.model = None
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for a given text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list of floats
        """
        if not self.model:
            logger.error("Embedding model not initialized")
            return None
        
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def generate_embeddings_batch(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        if not self.model:
            logger.error("Embedding model not initialized")
            return None
        
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return None
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1)
        """
        try:
            emb1 = np.array(embedding1).reshape(1, -1)
            emb2 = np.array(embedding2).reshape(1, -1)
            similarity = cosine_similarity(emb1, emb2)[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
    
    def rank_by_similarity(
        self,
        query_embedding: List[float],
        candidate_embeddings: List[List[float]]
    ) -> List[Dict[str, float]]:
        """
        Rank candidates by similarity to query.
        
        Args:
            query_embedding: Query embedding vector
            candidate_embeddings: List of candidate embedding vectors
            
        Returns:
            List of dictionaries with index and similarity score, sorted by score
        """
        try:
            query = np.array(query_embedding).reshape(1, -1)
            candidates = np.array(candidate_embeddings)
            
            similarities = cosine_similarity(query, candidates)[0]
            
            # Create list of (index, score) and sort by score
            ranked = [
                {"index": idx, "score": float(score)}
                for idx, score in enumerate(similarities)
            ]
            ranked.sort(key=lambda x: x["score"], reverse=True)
            
            return ranked
        except Exception as e:
            logger.error(f"Error ranking by similarity: {e}")
            return []

# Global embedding service instance
embedding_service = EmbeddingService()
