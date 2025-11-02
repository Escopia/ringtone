from sklearn.cluster import KMeans
import numpy as np
from typing import Dict, List

class AIProfiler:
    @staticmethod
    def analyze_user_behavior(user_data: Dict) -> Dict:
        features = [
            user_data.get("total_uploads", 0),
            user_data.get("total_deliveries", 0),
            user_data.get("avg_track_duration", 0),
            user_data.get("total_revenue", 0),
            user_data.get("engagement_score", 0)
        ]
        
        score = sum(features) / len(features) if features else 0
        
        if score > 75:
            segment = "premium"
        elif score > 40:
            segment = "active"
        else:
            segment = "starter"
        
        return {
            "segment": segment,
            "score": score,
            "recommendations": AIProfiler._get_recommendations(segment)
        }
    
    @staticmethod
    def _get_recommendations(segment: str) -> List[str]:
        recommendations = {
            "premium": ["Consider bulk delivery", "Explore new markets"],
            "active": ["Increase upload frequency", "Try different stores"],
            "starter": ["Complete profile", "Upload first track"]
        }
        return recommendations.get(segment, [])
    
    @staticmethod
    def predict_revenue(historical_data: List[float]) -> float:
        if not historical_data or len(historical_data) < 2:
            return 0.0
        
        return sum(historical_data[-3:]) / min(3, len(historical_data))
