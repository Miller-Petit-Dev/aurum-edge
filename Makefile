.PHONY: help setup test lint format clean validate-data build-features build-labels train backtest paper

# Variables
PYTHON := python3
VENV := venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
BLACK := $(VENV)/bin/black
RUFF := $(VENV)/bin/ruff

help: ## Muestra esta ayuda
	@echo "AURUM-EDGE v2 - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

setup: ## Instala dependencias y prepara entorno
	@echo "🔧 Instalando dependencias..."
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev]"
	@echo "🎣 Instalando pre-commit hooks..."
	$(VENV)/bin/pre-commit install
	@echo "📁 Creando estructura de carpetas..."
	@mkdir -p data/{raw,processed,features,labels}
	@mkdir -p reports/{experiments,daily,walkforward}
	@mkdir -p models logs
	@echo "✅ Setup completado. Ejecuta 'source venv/bin/activate' para activar el entorno."

test: ## Ejecuta todos los tests
	@echo "🧪 Ejecutando tests..."
	$(PYTEST) tests/ -v --tb=short

test-leakage: ## Test específico anti-leakage
	@echo "🔍 Verificando data leakage..."
	$(PYTEST) tests/test_leakage.py -v

test-splits: ## Test de splits temporales
	@echo "📊 Verificando splits temporales..."
	$(PYTEST) tests/test_splits.py -v

test-labels: ## Test de labels triple-barrier
	@echo "🏷️  Verificando labels..."
	$(PYTEST) tests/test_labels.py -v

test-quality: ## Test de calidad de datos
	@echo "✨ Verificando calidad de datos..."
	$(PYTEST) tests/test_data_quality.py -v

lint: ## Verifica calidad de código
	@echo "🔍 Verificando código con ruff..."
	$(RUFF) check src/ tests/
	@echo "🎨 Verificando formato con black..."
	$(BLACK) --check src/ tests/

format: ## Formatea código automáticamente
	@echo "🎨 Formateando código..."
	$(BLACK) src/ tests/
	$(RUFF) check --fix src/ tests/

validate-data: ## Valida datos raw
	@echo "✅ Validando datos raw..."
	$(PYTHON) -m aurum_edge.pipelines.build_dataset validate

build-dataset: ## Construye dataset limpio desde CSV raw
	@echo "📦 Construyendo dataset..."
	$(PYTHON) -m aurum_edge.pipelines.build_dataset

build-features: ## Genera features técnicos
	@echo "🔧 Generando features..."
	$(PYTHON) -m aurum_edge.pipelines.build_features

build-labels: ## Genera labels triple-barrier
	@echo "🏷️  Generando labels..."
	$(PYTHON) -m aurum_edge.pipelines.build_labels

train: ## Entrena modelo con Optuna + calibración
	@echo "🤖 Entrenando modelo..."
	$(PYTHON) -m aurum_edge.pipelines.train_model

backtest: ## Ejecuta walk-forward validation
	@echo "📈 Ejecutando backtest walk-forward..."
	$(PYTHON) -m aurum_edge.pipelines.run_walkforward

paper: ## Paper trading con human-in-the-loop
	@echo "📝 Iniciando paper trading..."
	$(PYTHON) -m aurum_edge.pipelines.run_paper

# Pipeline completo end-to-end
pipeline-full: build-dataset build-features build-labels train backtest ## Ejecuta pipeline completo
	@echo "✅ Pipeline completo ejecutado."

clean: ## Limpia archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
	@echo "✅ Limpieza completada."

clean-data: ## Limpia datos procesados (⚠️ cuidado)
	@echo "⚠️  ADVERTENCIA: Esto eliminará todos los datos procesados."
	@read -p "¿Continuar? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	rm -rf data/processed/* data/features/* data/labels/*
	@echo "✅ Datos procesados eliminados."

clean-models: ## Limpia modelos entrenados (⚠️ cuidado)
	@echo "⚠️  ADVERTENCIA: Esto eliminará todos los modelos."
	@read -p "¿Continuar? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	rm -rf models/*
	@echo "✅ Modelos eliminados."

install-mt5: ## Instala MetaTrader5 Python (solo fase 2)
	@echo "📦 Instalando MT5 Python library..."
	$(PIP) install -e ".[mt5]"
	@echo "✅ MT5 instalado."

dev-notebook: ## Inicia Jupyter notebook
	@echo "📓 Iniciando Jupyter..."
	$(VENV)/bin/jupyter notebook

dev-shell: ## Inicia IPython shell
	@echo "🐚 Iniciando IPython..."
	$(VENV)/bin/ipython

# Default target
.DEFAULT_GOAL := help
