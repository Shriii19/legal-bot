"""
Database models for Legal Bot
"""
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
import json
import os

@dataclass
class Consultation:
    """Legal consultation record"""
    id: str
    query: str
    category: str
    urgency: str
    response: str
    ai_model: str
    timestamp: datetime
    user_ip: Optional[str] = None
    response_time: Optional[float] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'query': self.query,
            'category': self.category,
            'urgency': self.urgency,
            'response': self.response,
            'ai_model': self.ai_model,
            'timestamp': self.timestamp.isoformat(),
            'user_ip': self.user_ip,
            'response_time': self.response_time
        }

class ConsultationStorage:
    """Simple file-based storage for consultations"""
    
    def __init__(self, storage_file='consultations.json'):
        self.storage_file = storage_file
        self.consultations = self._load_consultations()
    
    def _load_consultations(self):
        """Load consultations from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_consultation(self, consultation: Consultation):
        """Save a consultation record"""
        self.consultations.append(consultation.to_dict())
        self._save_to_file()
    
    def _save_to_file(self):
        """Save consultations to file"""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.consultations, f, indent=2, ensure_ascii=False)
    
    def get_stats(self):
        """Get consultation statistics"""
        total = len(self.consultations)
        categories = {}
        urgency_levels = {}
        
        for consultation in self.consultations:
            cat = consultation.get('category', 'unknown')
            urg = consultation.get('urgency', 'normal')
            
            categories[cat] = categories.get(cat, 0) + 1
            urgency_levels[urg] = urgency_levels.get(urg, 0) + 1
        
        return {
            'total_consultations': total,
            'categories': categories,
            'urgency_levels': urgency_levels
        }
