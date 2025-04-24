FROM python:3.11-slim

# 1. Dépendances système minimales
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        git && \
    rm -rf /var/lib/apt/lists/*

# 2. Crée le dossier de travail
WORKDIR /app

# 3. Copie les dépendances Python
COPY requirements.txt .

# 4. Installe les packages
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copie le code source et les tests
COPY src ./src
COPY tests ./tests

# 6. Ajoute le code au PYTHONPATH
ENV PYTHONPATH=/app/src

# 7. Commande par défaut : exécute les tests
CMD ["pytest", "-q"]
