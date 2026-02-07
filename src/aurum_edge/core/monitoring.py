"""
Monitoring and health checks
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
from loguru import logger


@dataclass
class DataQualityReport:
    """Data quality metrics"""
    total_rows: int
    missing_values: Dict[str, int]
    duplicate_rows: int
    gaps: List[tuple]
    outliers: Dict[str, int]
    date_range: tuple
    passed: bool
    issues: List[str]


@dataclass
class ModelDecayReport:
    """Model performance decay metrics"""
    current_accuracy: float
    baseline_accuracy: float
    decay_pct: float
    current_sharpe: float
    baseline_sharpe: float
    passed: bool
    issues: List[str]


class Monitor:
    """System monitoring"""
    
    def __init__(self):
        self.alerts = []
    
    def check_data_quality(self, df: pd.DataFrame, min_rows: int = 1000) -> DataQualityReport:
        """Check data quality"""
        issues = []
        
        # Missing values
        missing = df.isnull().sum().to_dict()
        if any(v > 0 for v in missing.values()):
            issues.append(f"Missing values found: {missing}")
        
        # Duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            issues.append(f"Found {dup_count} duplicate rows")
        
        # Min rows
        if len(df) < min_rows:
            issues.append(f"Insufficient rows: {len(df)} < {min_rows}")
        
        passed = len(issues) == 0
        
        return DataQualityReport(
            total_rows=len(df),
            missing_values=missing,
            duplicate_rows=dup_count,
            gaps=[],
            outliers={},
            date_range=(df.index[0], df.index[-1]) if len(df) > 0 else (None, None),
            passed=passed,
            issues=issues
        )
    
    def check_model_decay(
        self,
        current_metrics: Dict,
        baseline_metrics: Dict,
        decay_threshold: float = 0.1
    ) -> ModelDecayReport:
        """Check if model performance has decayed"""
        issues = []
        
        current_acc = current_metrics.get('accuracy', 0)
        baseline_acc = baseline_metrics.get('accuracy', 0)
        
        if baseline_acc > 0:
            decay = (baseline_acc - current_acc) / baseline_acc
            if decay > decay_threshold:
                issues.append(f"Accuracy decay: {decay:.2%}")
        else:
            decay = 0
        
        passed = len(issues) == 0
        
        return ModelDecayReport(
            current_accuracy=current_acc,
            baseline_accuracy=baseline_acc,
            decay_pct=decay,
            current_sharpe=current_metrics.get('sharpe', 0),
            baseline_sharpe=baseline_metrics.get('sharpe', 0),
            passed=passed,
            issues=issues
        )
    
    def add_alert(self, alert_type: str, message: str):
        """Add an alert"""
        alert = {
            'timestamp': datetime.now(),
            'type': alert_type,
            'message': message
        }
        self.alerts.append(alert)
        logger.warning(f"ALERT [{alert_type}]: {message}")
