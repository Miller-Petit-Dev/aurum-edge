"""Model registry"""
import json
from pathlib import Path
from datetime import datetime

class ModelRegistry:
    """Track model versions and metadata"""
    
    def __init__(self, registry_dir='models/registry'):
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.registry_dir / 'registry.json'
        self.registry = self._load_registry()
    
    def _load_registry(self):
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        return {}
    
    def register_model(self, model_id: str, metadata: dict):
        """Register a new model"""
        self.registry[model_id] = {
            'registered_at': datetime.now().isoformat(),
            **metadata
        }
        self._save_registry()
    
    def _save_registry(self):
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def get_latest_model(self):
        """Get the most recent model"""
        if not self.registry:
            return None
        return max(self.registry.items(), key=lambda x: x[1]['registered_at'])
