# 🔧 Makefile — Projet pinn-fisher-kpp

PYTHON := python
PYTHONPATH := src

# 📦 Tests unitaires
test:
	@echo "🔍 Running tests..."
	@PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest -q tests/

# 🧪 Plot de la solution FEM
plot-fem:
	@echo "📈 Plotting FEM solution..."
	@PYTHONPATH=$(PYTHONPATH) $(PYTHON) tests/test_fem_plot.py

# 🐳 Build image Docker
docker:
	@echo "🐳 Building Docker image..."
	docker build -t pinn-fisher-kpp:dev -f docker/Dockerfile .

# 🐚 Ouvrir un shell interactif dans Docker avec code monté
docker-shell:
	@echo "🚀 Entering Docker container..."
	docker run -it --rm -v $(PWD):/app -w /app pinn-fisher-kpp:dev bash

# 🧼 Nettoyage des fichiers temporaires
clean:
	@echo "🧹 Cleaning __pycache__ and *.pyc files..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -delete

# 🎯 Raccourci tout-en-un
all: test plot-fem
