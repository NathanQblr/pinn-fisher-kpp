# 🛠️ Guide de Développement — Projet `pinn-fisher-kpp`

Ce document décrit la marche à suivre pour développer localement dans un environnement Dockerisé, de manière reproductible et propre.

---

## ⚙️ Prérequis

- Docker Desktop installé et lancé ([lien téléchargement](https://www.docker.com/products/docker-desktop))
- Projet cloné localement
- Fichiers présents :
  - `docker/Dockerfile`
  - `requirements.txt`
  - `src/`, `tests/`, etc.

---

## 🚀 Développement interactif (Méthode B)

### 1. Lancer un conteneur Docker interactif

Depuis la racine du projet (`pinn-fisher-kpp/`) :

```bash
docker build -t pinn-fisher-kpp:dev -f docker/Dockerfile .
docker run -it --rm -v $(pwd):/app -w /app pinn-fisher-kpp:dev bash
```

Tu entres alors dans un shell **dans le conteneur**, avec accès à tous tes fichiers.

---

### 2. Développer ton code

- Écris/modifie tes fichiers localement dans `src/`, `tests/`, etc.
- Les changements sont immédiatement visibles dans le conteneur (grâce au `-v $(pwd):/app`).
- Exemple : ajoute une fonction dans `src/utils/mon_module.py`

---

### 3. Lancer les tests ou du code manuellement

Dans le terminal Docker :

```bash
pytest                        # lance tous les tests unitaires
python src/pinn/train.py     # exécute un script spécifique
```

---

## ✅ Astuces utiles

### Rebuild image après changement dans `requirements.txt`

```bash
docker build -t pinn-fisher-kpp:dev -f docker/Dockerfile .
```

### Ajouter un test

Crée un fichier `tests/test_machin.py` :

```python
def test_truc():
    assert 1 + 1 == 2
```

Puis lance :

```bash
pytest
```

---

## 🔁 Workflow typique

1. `docker build -t pinn-fisher-kpp:dev -f docker/Dockerfile .`
2. `docker run -it --rm -v $(pwd):/app -w /app pinn-fisher-kpp:dev bash`
3. Développe / modifie tes fichiers
4. Lance `pytest` ou `python src/mon_script.py`
5. Quitte le conteneur (`exit`) et recommence au besoin

---

## 💡 Conseils

- **Garde le `Dockerfile` propre** : ne le modifie pas pour expérimenter.
- **Versionne bien ton code** avec Git (`dev` pour avancer, `main` pour les versions stables).
- **Ne versionne pas `.venv/` ou `.ipynb_checkpoints/`** → ajoute-les au `.gitignore`.
- **Utilise les tests pour valider tes fonctions** avant d'intégrer.
