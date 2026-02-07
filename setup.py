from setuptools import setup, find_packages

setup(
    name="aurum-edge",
    version="2.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.1.0",
        "numpy>=1.24.0,<2.0.0",
        "scikit-learn>=1.3.0",
        "xgboost>=2.0.0",
        "optuna>=3.4.0",
        "pydantic>=2.5.0",
        "pyyaml>=6.0.1",
        "loguru>=0.7.2",
        "pyarrow>=14.0.0",
    ],
)
