"""Label schema validation"""
from typing import Dict
import pandas as pd

def validate_labels(df: pd.DataFrame) -> Dict:
    """Validate label distribution"""
    label_counts = df['label'].value_counts()
    total = len(df)
    
    distribution = {
        int(label): count / total
        for label, count in label_counts.items()
    }
    
    return {
        'distribution': distribution,
        'total_samples': total,
        'num_classes': len(label_counts)
    }
