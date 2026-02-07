"""
Configuration management using Pydantic
"""
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class ProjectConfig(BaseModel):
    """Project metadata"""
    name: str
    version: str
    description: str


class PathsConfig(BaseModel):
    """File paths configuration"""
    data_raw: Path = Path("data/raw")
    data_processed: Path = Path("data/processed")
    data_features: Path = Path("data/features")
    data_labels: Path = Path("data/labels")
    models: Path = Path("models")
    reports: Path = Path("reports")
    logs: Path = Path("logs")


class ModelConfig(BaseModel):
    """Model training configuration"""
    type: str = "xgboost"
    objective: str = "binary:logistic"
    eval_metric: str = "logloss"
    tuning: Dict[str, Any] = Field(default_factory=dict)
    calibration: Dict[str, Any] = Field(default_factory=dict)
    gating: Dict[str, Any] = Field(default_factory=dict)


class Config(BaseSettings):
    """Main configuration class"""
    
    project: Optional[ProjectConfig] = None
    paths: PathsConfig = PathsConfig()
    model: ModelConfig = ModelConfig()
    random_seed: int = 42
    
    # Config file paths
    asset_config_path: str = "configs/assets/nas100_m5.yaml"
    labeling_config_path: str = "configs/labeling/triple_barrier.yaml"
    walkforward_config_path: str = "configs/walkforward/wf_3m_2w.yaml"
    risk_config_path: str = "configs/risk/micro_account.yaml"
    execution_config_path: str = "configs/execution/human_in_loop.yaml"
    costs_config_path: str = "configs/costs/costs_default.yaml"
    
    # Loaded sub-configs
    _asset_config: Optional[Dict[str, Any]] = None
    _labeling_config: Optional[Dict[str, Any]] = None
    _walkforward_config: Optional[Dict[str, Any]] = None
    _risk_config: Optional[Dict[str, Any]] = None
    _execution_config: Optional[Dict[str, Any]] = None
    _costs_config: Optional[Dict[str, Any]] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @classmethod
    def from_yaml(cls, config_path: str = "configs/default.yaml") -> "Config":
        """Load config from YAML file"""
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)
    
    def load_sub_config(self, config_type: str) -> Dict[str, Any]:
        """Load a sub-configuration file"""
        config_path_attr = f"{config_type}_config_path"
        cache_attr = f"_{config_type}_config"
        
        if getattr(self, cache_attr) is not None:
            return getattr(self, cache_attr)
        
        config_path = getattr(self, config_path_attr)
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        setattr(self, cache_attr, config)
        return config
    
    @property
    def asset_config(self) -> Dict[str, Any]:
        return self.load_sub_config("asset")
    
    @property
    def labeling_config(self) -> Dict[str, Any]:
        return self.load_sub_config("labeling")
    
    @property
    def walkforward_config(self) -> Dict[str, Any]:
        return self.load_sub_config("walkforward")
    
    @property
    def risk_config(self) -> Dict[str, Any]:
        return self.load_sub_config("risk")
    
    @property
    def execution_config(self) -> Dict[str, Any]:
        return self.load_sub_config("execution")
    
    @property
    def costs_config(self) -> Dict[str, Any]:
        return self.load_sub_config("costs")
